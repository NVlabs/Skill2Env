import pandas as pd
import os
from typing import List, Dict, Optional, Union

# Default data path
DATA_PATH = os.environ.get(
    "PRIMEKG_DATA_PATH", os.path.join(os.path.dirname(__file__), "..", "data", "kg.csv")
)


def _load_kg():
    """Internal helper to load the KG efficiently."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"PrimeKG data not found at {DATA_PATH}. Please ensure the file is downloaded."
        )
    # For very large files, we might want to use a database or specialized graph library.
    # For now, we'll use pandas for simplicity but with low_memory=True.
    return pd.read_csv(DATA_PATH, low_memory=True)


def search_nodes(name_query: str, node_type: Optional[str] = None) -> List[Dict]:
    """
    Search for nodes in PrimeKG by name and optionally type.

    Args:
        name_query: String to search for in node names.
        node_type: Optional type of node (e.g., 'gene/protein', 'drug', 'disease').

    Returns:
        List of matching nodes with their metadata.
    """
    kg = _load_kg()

    # Check both x and y columns for unique nodes
    x_nodes = kg[["x_id", "x_type", "x_name", "x_source"]].drop_duplicates()
    x_nodes.columns = ["id", "type", "name", "source"]

    y_nodes = kg[["y_id", "y_type", "y_name", "y_source"]].drop_duplicates()
    y_nodes.columns = ["id", "type", "name", "source"]

    nodes = pd.concat([x_nodes, y_nodes]).drop_duplicates()

    mask = nodes["name"].str.contains(name_query, case=False, na=False)
    if node_type:
        mask &= nodes["type"] == node_type

    results = nodes[mask].head(20).to_dict(orient="records")
    return results


def get_neighbors(
    node_id: Union[str, int], relation_type: Optional[str] = None
) -> List[Dict]:
    """
    Get all direct neighbors of a specific node.

    Args:
        node_id: The ID of the node (e.g., NCBI Gene ID or ChEMBL ID).
        relation_type: Optional filter for specific relationship types.

    Returns:
        List of neighbors and the relationship metadata.
    """
    kg = _load_kg()
    node_id = str(node_id)

    mask_x = kg["x_id"].astype(str) == node_id
    mask_y = kg["y_id"].astype(str) == node_id

    if relation_type:
        mask_x &= kg["relation"] == relation_type
        mask_y &= kg["relation"] == relation_type

    neighbors_x = kg[mask_x][
        ["relation", "display_relation", "y_id", "y_type", "y_name", "y_source"]
    ]
    neighbors_x.columns = [
        "relation",
        "display_relation",
        "neighbor_id",
        "neighbor_type",
        "neighbor_name",
        "neighbor_source",
    ]

    neighbors_y = kg[mask_y][
        ["relation", "display_relation", "x_id", "x_type", "x_name", "x_source"]
    ]
    neighbors_y.columns = [
        "relation",
        "display_relation",
        "neighbor_id",
        "neighbor_type",
        "neighbor_name",
        "neighbor_source",
    ]

    results = pd.concat([neighbors_x, neighbors_y]).to_dict(orient="records")
    return results


def find_paths(
    start_node_id: Union[str, int],
    end_node_id: Union[str, int],
    max_depth: int = 2,
) -> List[List[Dict]]:
    """
    Find paths between two nodes (e.g., Drug -> shared target -> Disease) up to
    ``max_depth`` hops. Used for graph-based drug-repurposing hypotheses, where a
    depth-2 path drug -> gene/protein -> disease is candidate evidence for a new
    indication.

    Args:
        start_node_id: PrimeKG ``x_id``/``y_id`` of the start node (e.g. a drug).
        end_node_id: PrimeKG ``x_id``/``y_id`` of the end node (e.g. a disease).
        max_depth: 1 (direct edge only) or 2 (one intermediate node). Depth > 2 is
            not supported here — for deeper traversal use a real graph library
            (e.g. networkx) on the same kg.csv.

    Returns:
        List of paths; each path is a list of edge dicts (one per hop).
    """
    kg = _load_kg()
    start_node_id = str(start_node_id)
    end_node_id = str(end_node_id)
    x_str = kg["x_id"].astype(str)
    y_str = kg["y_id"].astype(str)

    paths: List[List[Dict]] = []

    # Depth 1: a direct edge between start and end (either orientation).
    direct = kg[
        ((x_str == start_node_id) & (y_str == end_node_id))
        | ((y_str == start_node_id) & (x_str == end_node_id))
    ]
    for _, row in direct.iterrows():
        paths.append([row.to_dict()])

    if max_depth >= 2:
        # Edges incident to the start node; the "other" endpoint is the intermediate.
        start_edges = kg[(x_str == start_node_id) | (y_str == start_node_id)]
        for _, e1 in start_edges.iterrows():
            mid_id = (
                str(e1["y_id"])
                if str(e1["x_id"]) == start_node_id
                else str(e1["x_id"])
            )
            if mid_id in (start_node_id, end_node_id):
                continue  # skip self-loops and the depth-1 case (already covered)

            # Edges connecting the intermediate node to the end node.
            mid_to_end = kg[
                ((x_str == mid_id) & (y_str == end_node_id))
                | ((y_str == mid_id) & (x_str == end_node_id))
            ]
            for _, e2 in mid_to_end.iterrows():
                paths.append([e1.to_dict(), e2.to_dict()])

    return paths


def get_disease_context(disease_name: str) -> Dict:
    """
    Analyze the local graph around a disease: associated genes, drugs, and phenotypes.
    """
    results = search_nodes(disease_name, node_type="disease")
    if not results:
        return {"error": "Disease not found"}

    disease_id = results[0]["id"]
    neighbors = get_neighbors(disease_id)

    # PrimeKG node types: phenotypes are "effect/phenotype" (NOT "phenotype").
    # Disease nodes are grouped, so one disease name can map to several MONDO x_id/
    # y_id values sharing a node_index; this uses the first match's id.
    summary = {
        "disease_info": results[0],
        "associated_genes": [
            n for n in neighbors if n["neighbor_type"] == "gene/protein"
        ],
        "associated_drugs": [n for n in neighbors if n["neighbor_type"] == "drug"],
        "phenotypes": [
            n for n in neighbors if n["neighbor_type"] == "effect/phenotype"
        ],
        "related_diseases": [n for n in neighbors if n["neighbor_type"] == "disease"],
    }
    return summary
