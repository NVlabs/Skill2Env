#!/usr/bin/env python3
"""
ClinPGx API Query Helper Script

Provides ready-to-use functions for querying the ClinPGx database API.
Includes rate limiting, error handling, and caching functionality.

ClinPGx API: https://api.clinpgx.org/
Rate limit: 2 requests per second
License: Creative Commons Attribution-ShareAlike 4.0 International
"""

import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# API Configuration
# ClinPGx resources are addressed by ClinPGx accession IDs in the path
# (e.g. gene CYP2D6 = PA128, CYP2C9 = PA126), not by symbols/rsIDs. Resolve a
# symbol or rsID via the collection endpoints with params (e.g. ?symbol=CYP2D6).
#
# Query-param convention (verified against the live API):
#   - genes are matched by `relatedGenes.symbol` (the `.name` form fails)
#   - chemicals/drugs are matched by `relatedChemicals.name` (the `.symbol`
#     form returns status:"fail" / "No results matching criteria")
#
# Response envelope: every response is a JSON object of the form
#   {"status": "success"|"fail", "data": [...] | {"errors": [...]}}
# so the payload is NEVER a bare list — read it via `payload["data"]`. The
# helpers below unwrap this for you (see `unwrap`).
BASE_URL = "https://api.clinpgx.org/v1/data/"
RATE_LIMIT_DELAY = 0.5  # 500ms delay = 2 requests/second


def unwrap(payload: Optional[Dict]) -> Optional[Any]:
    """
    Unwrap the ClinPGx {"status", "data"} response envelope.

    Returns the inner `data` on success, or None when the request failed,
    returned no results, or the payload was empty/malformed.
    """
    if not isinstance(payload, dict):
        return None
    if payload.get("status") == "fail":
        return None
    return payload.get("data")


def rate_limited_request(url: str, params: Optional[Dict] = None, delay: float = RATE_LIMIT_DELAY) -> requests.Response:
    """
    Make API request with rate limiting compliance.

    Args:
        url: API endpoint URL
        params: Query parameters
        delay: Delay in seconds between requests (default 0.5s for 2 req/sec)

    Returns:
        Response object
    """
    response = requests.get(url, params=params)
    time.sleep(delay)
    return response


def safe_api_call(url: str, params: Optional[Dict] = None, max_retries: int = 3) -> Optional[Dict]:
    """
    Make API call with error handling and exponential backoff retry.

    Args:
        url: API endpoint URL
        params: Query parameters
        max_retries: Maximum number of retry attempts

    Returns:
        JSON response data or None on failure
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                time.sleep(RATE_LIMIT_DELAY)
                return response.json()
            elif response.status_code == 429:
                # Rate limit exceeded
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"Rate limit exceeded. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            elif response.status_code == 404:
                print(f"Resource not found: {url}")
                return None
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts")
                return None
            time.sleep(1)

    return None


def cached_query(cache_file: str, query_func, *args, **kwargs) -> Any:
    """
    Cache API results to avoid repeated queries.

    Args:
        cache_file: Path to cache file
        query_func: Function to call if cache miss
        *args, **kwargs: Arguments to pass to query_func

    Returns:
        Cached or freshly queried data
    """
    cache_path = Path(cache_file)

    if cache_path.exists():
        print(f"Loading from cache: {cache_file}")
        with open(cache_path) as f:
            return json.load(f)

    print(f"Cache miss. Querying API...")
    result = query_func(*args, **kwargs)

    if result is not None:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Cached to: {cache_file}")

    return result


# Core Query Functions

def get_gene_info(gene_symbol: str) -> Optional[List[Dict]]:
    """
    Resolve a pharmacogene symbol to its ClinPGx record(s).

    The path form /gene/{id} expects a ClinPGx accession ID (e.g. CYP2D6 = PA128),
    so to look up by symbol we query the collection endpoint with ?symbol=.

    Args:
        gene_symbol: Gene symbol (e.g., "CYP2D6", "TPMT")

    Returns:
        List of matching gene records (read the accession ID from result['id'])

    Example:
        >>> genes = get_gene_info("CYP2D6")
        >>> print(genes[0]['symbol'], genes[0]['id'])
    """
    url = f"{BASE_URL}gene"
    return unwrap(safe_api_call(url, {"symbol": gene_symbol}))


def get_gene_by_id(gene_id: str) -> Optional[Dict]:
    """
    Retrieve a gene record directly by its ClinPGx accession ID.

    Args:
        gene_id: ClinPGx gene accession ID (e.g., "PA128" for CYP2D6)

    Returns:
        Gene information dictionary
    """
    url = f"{BASE_URL}gene/{gene_id}"
    return unwrap(safe_api_call(url))


def get_drug_info(drug_name: str) -> Optional[List[Dict]]:
    """
    Search for drug/chemical information by name.

    Args:
        drug_name: Drug name (e.g., "warfarin", "codeine")

    Returns:
        List of matching drugs

    Example:
        >>> drugs = get_drug_info("warfarin")
        >>> for drug in drugs:
        >>>     print(drug['name'], drug['id'])
    """
    url = f"{BASE_URL}chemical"
    params = {"name": drug_name}
    return unwrap(safe_api_call(url, params))


def get_gene_drug_pairs(gene: Optional[str] = None, drug: Optional[str] = None) -> Optional[List[Dict]]:
    """
    Derive gene-drug relationships from guideline annotations.

    The public ClinPGx API has no single gene-drug-pair endpoint; pairs are
    derived from guideline annotations (or the /report/pair report endpoint when
    both object accession IDs are known).

    Args:
        gene: Gene symbol (optional)
        drug: Drug name / symbol (optional)

    Returns:
        List of guideline annotations matching the gene and/or drug

    Example:
        >>> # Guideline annotations related to CYP2D6
        >>> anns = get_gene_drug_pairs(gene="CYP2D6")
        >>>
        >>> # Guideline annotations related to codeine
        >>> anns = get_gene_drug_pairs(drug="codeine")
    """
    url = f"{BASE_URL}guidelineAnnotation"
    params = {}
    if gene:
        params["relatedGenes.symbol"] = gene
    if drug:
        params["relatedChemicals.name"] = drug

    return unwrap(safe_api_call(url, params))


def get_pair_report(first_obj_id: str, second_obj_id: str,
                    result_type: str = "guidelineAnnotation") -> Optional[Any]:
    """
    Fetch a pair report for two ClinPGx objects via the report endpoint.

    Endpoint: /report/pair/{firstObjId}/{secondObjId}/{resultType}

    Args:
        first_obj_id: Accession ID of the first object (e.g. gene "PA128")
        second_obj_id: Accession ID of the second object (e.g. chemical "PA449088")
        result_type: Report result type (e.g. "guidelineAnnotation")

    Returns:
        Pair report data
    """
    url = f"https://api.clinpgx.org/v1/report/pair/{first_obj_id}/{second_obj_id}/{result_type}"
    return unwrap(safe_api_call(url))


def get_cpic_guidelines(gene: Optional[str] = None, drug: Optional[str] = None) -> Optional[List[Dict]]:
    """
    Retrieve CPIC clinical practice guidelines.

    Args:
        gene: Gene symbol (optional)
        drug: Drug name (optional)

    Returns:
        List of CPIC guidelines

    Example:
        >>> # Get all CPIC guidelines
        >>> guidelines = get_cpic_guidelines()
        >>>
        >>> # Get guideline for specific gene-drug
        >>> guideline = get_cpic_guidelines(gene="CYP2C19", drug="clopidogrel")
    """
    url = f"{BASE_URL}guidelineAnnotation"
    params = {"source": "CPIC"}
    if gene:
        params["relatedGenes.symbol"] = gene
    if drug:
        params["relatedChemicals.name"] = drug

    return unwrap(safe_api_call(url, params))


def get_alleles(gene: str) -> Optional[List[Dict]]:
    """
    Star-allele definitions, functions, and population frequencies.

    NOTE: The public ClinPGx API does NOT expose an /allele resource. Canonical
    star-allele definitions and frequencies are maintained by PharmVar
    (https://www.pharmvar.org/). Allele-level clinical implications are surfaced
    through guideline annotations; this helper returns the guideline annotations
    related to the gene so callers do not rely on a non-existent endpoint.

    Args:
        gene: Gene symbol (e.g., "CYP2D6")

    Returns:
        List of guideline annotations related to the gene

    Example:
        >>> # For canonical allele data use PharmVar: https://www.pharmvar.org/gene/CYP2D6
        >>> anns = get_alleles("CYP2D6")
    """
    url = f"{BASE_URL}guidelineAnnotation"
    params = {"relatedGenes.symbol": gene}
    return unwrap(safe_api_call(url, params))


def get_clinical_annotations(
    gene: Optional[str] = None,
    drug: Optional[str] = None,
    evidence_level: Optional[str] = None
) -> Optional[List[Dict]]:
    """
    Retrieve curated literature annotations for gene-drug interactions.

    Served by the summaryAnnotation collection (use variantAnnotation /
    dataAnnotation for variant- or data-level annotations). The level-of-evidence
    filter field is unverified against the OpenAPI spec; confirm before relying
    on it.

    Args:
        gene: Gene symbol (optional)
        drug: Drug name / symbol (optional)
        evidence_level: Filter by level of evidence (1A, 1B, 2A, 2B, 3, 4)

    Returns:
        List of summary annotations

    Example:
        >>> # Get summary annotations related to CYP2D6
        >>> annotations = get_clinical_annotations(gene="CYP2D6")
    """
    url = f"{BASE_URL}summaryAnnotation"
    params = {}
    if gene:
        params["relatedGenes.symbol"] = gene
    if drug:
        params["relatedChemicals.name"] = drug
    if evidence_level:
        params["levelOfEvidence"] = evidence_level

    return unwrap(safe_api_call(url, params))


def get_drug_labels(drug: str, source: Optional[str] = None) -> Optional[List[Dict]]:
    """
    Retrieve pharmacogenomic drug label information.

    Args:
        drug: Drug name
        source: Regulatory source (e.g., "FDA", "EMA")

    Returns:
        List of drug labels with PGx information

    Example:
        >>> # Get all labels for warfarin
        >>> labels = get_drug_labels("warfarin")
        >>>
        >>> # Get only FDA labels
        >>> fda_labels = get_drug_labels("warfarin", source="FDA")
    """
    url = f"{BASE_URL}label"
    params = {"relatedChemicals.name": drug}
    if source:
        params["source"] = source

    return unwrap(safe_api_call(url, params))


def search_variants(rsid: Optional[str] = None) -> Optional[List[Dict]]:
    """
    Resolve a genetic variant by rsID.

    The path form /variant/{id} expects a ClinPGx accession ID, so to look up by
    rsID we query the collection endpoint with ?symbol=. Read the accession ID
    from result['id'] to fetch the full record directly.

    Args:
        rsid: dbSNP rsID (e.g., "rs4244285")

    Returns:
        List of matching variant records

    Example:
        >>> variants = search_variants(rsid="rs4244285")
        >>> # full record: get_variant_by_id(variants[0]['id'])
    """
    url = f"{BASE_URL}variant"
    return unwrap(safe_api_call(url, {"symbol": rsid}))


def get_variant_by_id(variant_id: str) -> Optional[Dict]:
    """
    Retrieve a variant record directly by its ClinPGx accession ID.

    Args:
        variant_id: ClinPGx variant accession ID

    Returns:
        Variant information dictionary
    """
    url = f"{BASE_URL}variant/{variant_id}"
    return unwrap(safe_api_call(url))


def get_pathway_info(pathway_id: Optional[str] = None, drug: Optional[str] = None) -> Optional[Any]:
    """
    Retrieve pharmacokinetic/pharmacodynamic pathway information.

    Args:
        pathway_id: ClinPGx pathway ID (optional)
        drug: Drug name (optional)

    Returns:
        Pathway information or list of pathways

    Example:
        >>> # Get specific pathway
        >>> pathway = get_pathway_info(pathway_id="PA146123006")
        >>>
        >>> # Get all pathways for a drug
        >>> pathways = get_pathway_info(drug="warfarin")
    """
    if pathway_id:
        url = f"{BASE_URL}pathway/{pathway_id}"
        return unwrap(safe_api_call(url))

    url = f"{BASE_URL}pathway"
    params = {}
    if drug:
        params["relatedChemicals.name"] = drug

    return unwrap(safe_api_call(url, params))


# Utility Functions

def export_to_dataframe(data: List[Dict], output_file: Optional[str] = None):
    """
    Convert API results to pandas DataFrame for analysis.

    Args:
        data: List of dictionaries from API
        output_file: Optional CSV output file path

    Returns:
        pandas DataFrame

    Example:
        >>> pairs = get_gene_drug_pairs(gene="CYP2D6")
        >>> df = export_to_dataframe(pairs, "cyp2d6_pairs.csv")
        >>> print(df.head())
    """
    try:
        import pandas as pd
    except ImportError:
        print("pandas not installed. Install with: pip install pandas")
        return None

    df = pd.DataFrame(data)

    if output_file:
        df.to_csv(output_file, index=False)
        print(f"Data exported to: {output_file}")

    return df


def batch_gene_query(gene_list: List[str], delay: float = 0.5) -> Dict[str, List[Dict]]:
    """
    Resolve multiple gene symbols in batch with rate limiting.

    Args:
        gene_list: List of gene symbols
        delay: Delay between requests (default 0.5s)

    Returns:
        Dictionary mapping each gene symbol to its list of matching records

    Example:
        >>> genes = ["CYP2D6", "CYP2C19", "CYP2C9", "TPMT"]
        >>> results = batch_gene_query(genes)
        >>> for gene, recs in results.items():
        >>>     print(f"{gene}: {recs[0]['id'] if recs else 'not found'}")
    """
    results = {}

    print(f"Querying {len(gene_list)} genes with {delay}s delay between requests...")

    for gene in gene_list:
        print(f"Fetching: {gene}")
        data = get_gene_info(gene)
        if data:
            results[gene] = data
        time.sleep(delay)

    print(f"Completed: {len(results)}/{len(gene_list)} successful")
    return results


def find_actionable_gene_drug_pairs(source: str = "CPIC") -> Optional[List[Dict]]:
    """
    Find clinically actionable gene-drug relationships via guideline annotations.

    There is no geneDrugPair endpoint (and no cpicLevel parameter) in the public
    API. Actionable pairs are derived from guideline annotations; inspect each
    returned annotation's relatedGenes / relatedChemicals to enumerate pairs.

    Args:
        source: Guideline source to filter on (e.g. "CPIC", "DPWG")

    Returns:
        List of guideline annotations from the requested source

    Example:
        >>> actionable = find_actionable_gene_drug_pairs(source="CPIC")
        >>> for ann in actionable:
        >>>     print(ann.get("name"))
    """
    url = f"{BASE_URL}guidelineAnnotation"
    params = {"source": source}
    return unwrap(safe_api_call(url, params))


# Example Usage
if __name__ == "__main__":
    print("ClinPGx API Query Examples\n")

    # Example 1: Get gene information
    print("=" * 60)
    print("Example 1: Get CYP2D6 gene information")
    print("=" * 60)
    cyp2d6 = get_gene_info("CYP2D6")
    if cyp2d6:
        rec = cyp2d6[0]
        print(f"Gene: {rec.get('symbol')}")
        print(f"ID: {rec.get('id')}")
        print(f"Name: {rec.get('name')}")
        print()

    # Example 2: Search for a drug
    print("=" * 60)
    print("Example 2: Search for warfarin")
    print("=" * 60)
    warfarin = get_drug_info("warfarin")
    if warfarin:
        for drug in warfarin[:1]:  # Show first result
            print(f"Drug: {drug.get('name')}")
            print(f"ID: {drug.get('id')}")
        print()

    # Example 3: Derive gene-drug relationship from guideline annotations
    print("=" * 60)
    print("Example 3: Guideline annotations for CYP2C19 + clopidogrel")
    print("=" * 60)
    pair = get_gene_drug_pairs(gene="CYP2C19", drug="clopidogrel")
    if pair:
        print(f"Found {len(pair)} guideline annotation(s)")
        if len(pair) > 0:
            print(f"First: {pair[0].get('name')}")
        print()

    # Example 4: Get CPIC guidelines
    print("=" * 60)
    print("Example 4: Get CPIC guidelines for CYP2C19")
    print("=" * 60)
    guidelines = get_cpic_guidelines(gene="CYP2C19")
    if guidelines:
        print(f"Found {len(guidelines)} guideline(s)")
        for g in guidelines[:2]:  # Show first 2
            print(f"  - {g.get('name')}")
        print()

    # Example 5: Allele-related guideline annotations for a gene
    # (canonical allele definitions/frequencies: https://www.pharmvar.org/gene/CYP2D6)
    print("=" * 60)
    print("Example 5: CYP2D6 allele-related guideline annotations")
    print("=" * 60)
    alleles = get_alleles("CYP2D6")
    if alleles:
        print(f"Found {len(alleles)} guideline annotation(s)")
        for ann in alleles[:3]:  # Show first 3
            print(f"  - {ann.get('name')}")
        print()

    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)
