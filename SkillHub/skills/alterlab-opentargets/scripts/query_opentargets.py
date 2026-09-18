#!/usr/bin/env python3
"""
Open Targets Platform GraphQL Query Helper

This script provides reusable functions for querying the Open Targets Platform
GraphQL API. Use these functions to retrieve target, disease, drug, and
association data.

Verified against Open Targets data version 26.03 (API meta apiVersion 26.03.1).
The schema changes between releases; if a field errors, introspect the live
schema at the GraphQL browser (see references/api_reference.md).

Dependencies: requests. Run with uv: `uv run --with requests scripts/query_opentargets.py`
"""

import requests
from typing import Dict, List, Optional, Any


# API endpoint
BASE_URL = "https://api.platform.opentargets.org/api/v4/graphql"


def execute_query(query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Execute a GraphQL query against the Open Targets Platform API.

    Args:
        query: GraphQL query string
        variables: Optional dictionary of variables for the query

    Returns:
        Dictionary containing the API response data

    Raises:
        Exception if the API request fails or returns errors
    """
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    try:
        response = requests.post(BASE_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            raise Exception(f"GraphQL errors: {data['errors']}")

        return data.get("data", {})

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


def search_entities(query_string: str, entity_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Search for targets, diseases, or drugs by name or identifier.

    Args:
        query_string: Search term (e.g., "BRCA1", "alzheimer", "aspirin")
        entity_types: Optional list to filter by entity type ["target", "disease", "drug"]

    Returns:
        List of search results with id, name, entity type, and description
    """
    # NOTE: Pagination requires both `index` and `size` (both non-null).
    query = """
      query search($queryString: String!, $entityNames: [String!]) {
        search(queryString: $queryString, entityNames: $entityNames, page: {index: 0, size: 10}) {
          hits {
            id
            entity
            name
            description
          }
        }
      }
    """

    variables = {"queryString": query_string}
    if entity_types:
        variables["entityNames"] = entity_types

    result = execute_query(query, variables)
    return result.get("search", {}).get("hits", [])


def get_target_info(ensembl_id: str, include_diseases: bool = False) -> Dict[str, Any]:
    """
    Retrieve comprehensive information about a target gene.

    Args:
        ensembl_id: Ensembl gene ID (e.g., "ENSG00000157764")
        include_diseases: Whether to include top associated diseases

    Returns:
        Dictionary with target information including tractability, safety, expression
    """
    disease_fragment = """
      associatedDiseases(page: {index: 0, size: 10}) {
        rows {
          disease {
            id
            name
          }
          score
          datatypeScores {
            id
            score
          }
        }
      }
    """ if include_diseases else ""

    query = f"""
      query targetInfo($ensemblId: String!) {{
        target(ensemblId: $ensemblId) {{
          id
          approvedSymbol
          approvedName
          biotype
          functionDescriptions

          tractability {{
            label
            modality
            value
          }}

          safetyLiabilities {{
            event
            effects {{
              direction
              dosing
            }}
            biosamples {{
              tissueLabel
            }}
          }}

          geneticConstraint {{
            constraintType
            score
            exp
            obs
          }}

          {disease_fragment}
        }}
      }}
    """

    result = execute_query(query, {"ensemblId": ensembl_id})
    return result.get("target", {})


def get_disease_info(efo_id: str, include_targets: bool = False) -> Dict[str, Any]:
    """
    Retrieve information about a disease.

    Args:
        efo_id: Disease identifier. Open Targets has migrated many diseases to
            MONDO IDs (e.g. Alzheimer disease is "MONDO_0004975", not
            "EFO_0000249"). The `disease(efoId:)` argument accepts EFO, MONDO,
            HP, Orphanet, etc. IDs. Resolve the current ID via search_entities().
        include_targets: Whether to include top associated targets

    Returns:
        Dictionary with disease information
    """
    target_fragment = """
      associatedTargets(page: {index: 0, size: 10}) {
        rows {
          target {
            id
            approvedSymbol
            approvedName
          }
          score
          datatypeScores {
            id
            score
          }
        }
      }
    """ if include_targets else ""

    query = f"""
      query diseaseInfo($efoId: String!) {{
        disease(efoId: $efoId) {{
          id
          name
          description
          therapeuticAreas {{
            id
            name
          }}
          synonyms {{
            terms
          }}
          {target_fragment}
        }}
      }}
    """

    result = execute_query(query, {"efoId": efo_id})
    return result.get("disease", {})


def get_target_disease_evidence(ensembl_id: str, efo_id: str,
                                  datasource_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Retrieve evidence linking a target to a disease.

    Args:
        ensembl_id: Ensembl gene ID
        efo_id: Disease identifier (EFO/MONDO/etc.)
        datasource_ids: Optional filter by data SOURCE id, e.g.
            ["gwas_catalog", "clinvar", "chembl"]. The API filters by data
            source, not by broad data type; to keep only genetic_association
            evidence, either pass its sources (gwas_catalog, gene_burden,
            clinvar, gene2phenotype, genomics_england, orphanet, uniprot_*,
            clingen) or fetch all rows and filter client-side on `datatypeId`.

    Returns:
        List of evidence records with scores and sources
    """
    query = """
      query evidences($ensemblId: String!, $efoId: String!, $datasourceIds: [String!]) {
        disease(efoId: $efoId) {
          evidences(ensemblIds: [$ensemblId], datasourceIds: $datasourceIds, size: 100) {
            rows {
              datasourceId
              datatypeId
              score
              targetFromSourceId
              studyId
              literature
              cohortPhenotypes
            }
          }
        }
      }
    """

    variables = {"ensemblId": ensembl_id, "efoId": efo_id}
    if datasource_ids:
        variables["datasourceIds"] = datasource_ids

    result = execute_query(query, variables)
    return result.get("disease", {}).get("evidences", {}).get("rows", [])


def get_known_drugs_for_disease(efo_id: str) -> Dict[str, Any]:
    """
    Get drugs and clinical candidates known to be used for a disease.

    As of recent releases the `knownDrugs` field was replaced by
    `drugAndClinicalCandidates`. Each row carries the drug (with its mechanisms
    of action and targeted genes), the maximum clinical stage reached for this
    indication, and the underlying clinical trial reports.

    Args:
        efo_id: Disease identifier (EFO/MONDO/etc.)

    Returns:
        Dictionary with `count` and `rows` of drug-indication records. Clinical
        stage is an enum string (e.g. "APPROVAL", "PHASE_3", "PHASE_2",
        "PHASE_1", "UNKNOWN").
    """
    query = """
      query drugCandidates($efoId: String!) {
        disease(efoId: $efoId) {
          drugAndClinicalCandidates {
            count
            rows {
              maxClinicalStage
              drug {
                id
                name
                drugType
                maximumClinicalStage
                mechanismsOfAction {
                  rows {
                    actionType
                    mechanismOfAction
                    targets {
                      id
                      approvedSymbol
                    }
                  }
                }
              }
              clinicalReports {
                trialPhase
                clinicalStage
                trialOverallStatus
              }
            }
          }
        }
      }
    """

    result = execute_query(query, {"efoId": efo_id})
    return result.get("disease", {}).get("drugAndClinicalCandidates", {})


def get_drug_info(chembl_id: str) -> Dict[str, Any]:
    """
    Retrieve information about a drug.

    Args:
        chembl_id: ChEMBL identifier (e.g., "CHEMBL25")

    Returns:
        Dictionary with drug information
    """
    query = """
      query drugInfo($chemblId: String!) {
        drug(chemblId: $chemblId) {
          id
          name
          synonyms
          drugType
          maximumClinicalStage
          drugWarnings {
            toxicityClass
            description
            year
            country
          }
          mechanismsOfAction {
            rows {
              actionType
              mechanismOfAction
              targetName
              targets {
                id
                approvedSymbol
              }
            }
          }
          indications {
            rows {
              disease {
                id
                name
              }
              maxClinicalStage
            }
          }
        }
      }
    """

    result = execute_query(query, {"chemblId": chembl_id})
    return result.get("drug", {})


def get_target_associations(ensembl_id: str, min_score: float = 0.0) -> List[Dict[str, Any]]:
    """
    Get all disease associations for a target, filtered by minimum score.

    Args:
        ensembl_id: Ensembl gene ID
        min_score: Minimum association score (0-1) to include

    Returns:
        List of disease associations with scores
    """
    query = """
      query targetAssociations($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
          associatedDiseases(page: {index: 0, size: 100}) {
            count
            rows {
              disease {
                id
                name
              }
              score
              datatypeScores {
                id
                score
              }
            }
          }
        }
      }
    """

    result = execute_query(query, {"ensemblId": ensembl_id})
    associations = result.get("target", {}).get("associatedDiseases", {}).get("rows", [])

    # Filter by minimum score
    return [assoc for assoc in associations if assoc.get("score", 0) >= min_score]


# Example usage
if __name__ == "__main__":
    # Example 1: Search for a gene
    print("Searching for BRCA1...")
    results = search_entities("BRCA1", entity_types=["target"])
    for result in results[:3]:
        print(f"  {result['name']} ({result['id']})")

    # Example 2: Get target information
    if results:
        ensembl_id = results[0]['id']
        print(f"\nGetting info for {ensembl_id}...")
        target_info = get_target_info(ensembl_id, include_diseases=True)
        print(f"  Symbol: {target_info.get('approvedSymbol')}")
        print(f"  Name: {target_info.get('approvedName')}")

        # Show top diseases
        diseases = target_info.get('associatedDiseases', {}).get('rows', [])
        if diseases:
            print(f"\n  Top associated diseases:")
            for disease in diseases[:3]:
                print(f"    - {disease['disease']['name']} (score: {disease['score']:.2f})")

    # Example 3: Search for a disease
    print("\n\nSearching for Alzheimer's disease...")
    disease_results = search_entities("alzheimer", entity_types=["disease"])
    if disease_results:
        efo_id = disease_results[0]['id']
        print(f"  Found: {disease_results[0]['name']} ({efo_id})")

        # Get known drugs / clinical candidates
        print(f"\n  Drugs and clinical candidates for {disease_results[0]['name']}:")
        drugs = get_known_drugs_for_disease(efo_id)
        for row in drugs.get('rows', [])[:5]:
            print(f"    - {row['drug']['name']} (max stage: {row.get('maxClinicalStage')})")
