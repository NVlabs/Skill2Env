#!/usr/bin/env python3
"""
Fetch gene data from NCBI using the Datasets API.

This script provides access to the NCBI Datasets API for retrieving
comprehensive gene information including metadata and sequences.
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from typing import Optional, Dict, Any, List


DATASETS_API_BASE = "https://api.ncbi.nlm.nih.gov/datasets/v2/gene"


def get_taxon_id(taxon_name: str) -> Optional[str]:
    """
    Convert taxon name to NCBI taxon ID.

    Args:
        taxon_name: Common or scientific name (e.g., "human", "Homo sapiens")

    Returns:
        Taxon ID as string, or None if not found
    """
    # Common mappings
    common_taxa = {
        'human': '9606',
        'homo sapiens': '9606',
        'mouse': '10090',
        'mus musculus': '10090',
        'rat': '10116',
        'rattus norvegicus': '10116',
        'zebrafish': '7955',
        'danio rerio': '7955',
        'fruit fly': '7227',
        'drosophila melanogaster': '7227',
        'c. elegans': '6239',
        'caenorhabditis elegans': '6239',
        'yeast': '4932',
        'saccharomyces cerevisiae': '4932',
        'arabidopsis': '3702',
        'arabidopsis thaliana': '3702',
        'e. coli': '562',
        'escherichia coli': '562',
    }

    taxon_lower = taxon_name.lower().strip()
    return common_taxa.get(taxon_lower)


def fetch_gene_by_id(gene_id: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch gene data by Gene ID.

    Args:
        gene_id: NCBI Gene ID
        api_key: Optional NCBI API key

    Returns:
        Gene data as dictionary
    """
    url = f"{DATASETS_API_BASE}/id/{gene_id}"

    headers = {}
    if api_key:
        headers['api-key'] = api_key

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 404:
            print(f"Gene ID {gene_id} not found", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {}


def fetch_gene_by_symbol(symbol: str, taxon: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch gene data by gene symbol and taxon.

    Args:
        symbol: Gene symbol (e.g., "BRCA1")
        taxon: Organism name or taxon ID
        api_key: Optional NCBI API key

    Returns:
        Gene data as dictionary
    """
    # Convert taxon name to ID if needed
    taxon_id = get_taxon_id(taxon)
    if not taxon_id:
        # Try to use as-is (might already be a taxon ID)
        taxon_id = taxon

    url = f"{DATASETS_API_BASE}/symbol/{symbol}/taxon/{taxon_id}"

    headers = {}
    if api_key:
        headers['api-key'] = api_key

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        if e.code == 404:
            print(f"Gene symbol '{symbol}' not found for taxon {taxon}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {}


def fetch_multiple_genes(gene_ids: List[str], api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch data for multiple genes by ID.

    The Datasets v2 API accepts comma-separated Gene IDs on the GET
    /gene/id/{ids} path (there is no POST /gene/id body endpoint).

    Args:
        gene_ids: List of Gene IDs
        api_key: Optional NCBI API key

    Returns:
        Combined gene data as dictionary
    """
    url = f"{DATASETS_API_BASE}/id/{','.join(gene_ids)}"

    headers = {}
    if api_key:
        headers['api-key'] = api_key

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {}


def display_gene_info(data: Dict[str, Any], verbose: bool = False) -> None:
    """
    Display gene information in human-readable format.

    Parses the Datasets v2 response, which wraps each gene under
    ``reports[].gene`` (NOT a top-level ``genes`` list).

    Args:
        data: Gene data dictionary from API
        verbose: Show detailed information
    """
    reports = data.get('reports')
    if not reports:
        print("No gene data found in response")
        return

    for report in reports:
        gene_info = report.get('gene', {})

        print(f"Gene ID: {gene_info.get('gene_id', 'N/A')}")
        print(f"Symbol: {gene_info.get('symbol', 'N/A')}")
        print(f"Description: {gene_info.get('description', 'N/A')}")

        # Organism (v2 uses tax_id / taxname / common_name)
        if 'taxname' in gene_info:
            print(f"Organism: {gene_info['taxname']}")

        if gene_info.get('chromosomes'):
            print(f"Chromosome(s): {', '.join(gene_info['chromosomes'])}")

        # Cytogenetic map location
        for loc in gene_info.get('map_locations', []):
            if loc.get('map_type') == 'Cytogenetic':
                print(f"Map Location: {loc.get('map_value', 'N/A')}")
                break

        # Nomenclature
        if 'nomenclature_authority' in gene_info:
            auth = gene_info['nomenclature_authority']
            print(f"Nomenclature: {auth.get('authority', 'N/A')} "
                  f"({auth.get('identifier', 'N/A')})")

        # Synonyms
        if gene_info.get('synonyms'):
            print(f"Synonyms: {', '.join(gene_info['synonyms'])}")

        if verbose:
            if 'type' in gene_info:
                print(f"Type: {gene_info['type']}")

            print(f"Transcripts: {gene_info.get('transcript_count', 'N/A')}, "
                  f"Proteins: {gene_info.get('protein_count', 'N/A')} "
                  f"(use the product_report endpoint for RefSeq accessions)")

            if gene_info.get('swiss_prot_accessions'):
                print(f"UniProt/Swiss-Prot: "
                      f"{', '.join(gene_info['swiss_prot_accessions'])}")

            if gene_info.get('ensembl_gene_ids'):
                print(f"Ensembl: {', '.join(gene_info['ensembl_gene_ids'])}")

            # Genomic locations: annotations[].genomic_locations[].genomic_range
            locations = []
            for ann in gene_info.get('annotations', []):
                assembly = ann.get('assembly_name', 'N/A')
                for gl in ann.get('genomic_locations', []):
                    accession = gl.get('genomic_accession_version', 'N/A')
                    rng = gl.get('genomic_range', {})
                    locations.append(
                        f"  {assembly} {accession}: "
                        f"{rng.get('begin', 'N/A')}-{rng.get('end', 'N/A')} "
                        f"({rng.get('orientation', 'N/A')})"
                    )
            if locations:
                print("\nGenomic Locations:")
                print('\n'.join(locations))

            # Gene Ontology terms
            go = gene_info.get('gene_ontology') or {}
            go_lines = []
            for category in ('molecular_functions', 'biological_processes',
                             'cellular_components'):
                for term in (go.get(category) or [])[:5]:
                    go_lines.append(
                        f"  [{category.split('_')[0]}] "
                        f"{term.get('go_id', '')} {term.get('name', '')}".rstrip()
                    )
            if go_lines:
                print("\nGene Ontology (first few per category):")
                print('\n'.join(go_lines))

        print()


def main():
    parser = argparse.ArgumentParser(
        description='Fetch gene data from NCBI Datasets API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fetch by Gene ID
  %(prog)s --gene-id 672

  # Fetch by gene symbol and organism
  %(prog)s --symbol BRCA1 --taxon human

  # Fetch multiple genes
  %(prog)s --gene-id 672,7157,5594

  # Get JSON output
  %(prog)s --symbol TP53 --taxon "Homo sapiens" --output json

  # Verbose output with details
  %(prog)s --gene-id 672 --verbose
        """
    )

    parser.add_argument('--gene-id', '-g', help='Gene ID(s), comma-separated')
    parser.add_argument('--symbol', '-s', help='Gene symbol')
    parser.add_argument('--taxon', '-t', help='Organism name or taxon ID (required with --symbol)')
    parser.add_argument('--output', '-o', choices=['pretty', 'json'], default='pretty',
                       help='Output format (default: pretty)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed information')
    parser.add_argument('--api-key', '-k', help='NCBI API key')

    args = parser.parse_args()

    if not args.gene_id and not args.symbol:
        parser.error("Either --gene-id or --symbol must be provided")

    if args.symbol and not args.taxon:
        parser.error("--taxon is required when using --symbol")

    # Fetch data
    if args.gene_id:
        gene_ids = [id.strip() for id in args.gene_id.split(',')]
        if len(gene_ids) == 1:
            data = fetch_gene_by_id(gene_ids[0], api_key=args.api_key)
        else:
            data = fetch_multiple_genes(gene_ids, api_key=args.api_key)
    else:
        data = fetch_gene_by_symbol(args.symbol, args.taxon, api_key=args.api_key)

    if not data:
        sys.exit(1)

    # Output
    if args.output == 'json':
        print(json.dumps(data, indent=2))
    else:
        display_gene_info(data, verbose=args.verbose)


if __name__ == '__main__':
    main()
