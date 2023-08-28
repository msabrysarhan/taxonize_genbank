import argparse
import networkx as nx
from tqdm import tqdm  # Import tqdm for loading bars

def read_nodes_dmp(nodes_dmp_path):
    taxid_to_parent = {}
    rank_map = {}

    with open(nodes_dmp_path, "r") as nodes_file:
        lines = nodes_file.readlines()
        for line in tqdm(lines, desc="Reading nodes.dmp", unit=" lines"):
            line_parts = line.strip().split("|")
            taxid = line_parts[0].strip()
            parent_taxid = line_parts[1].strip()
            rank = line_parts[2].strip()

            taxid_to_parent[taxid] = parent_taxid
            rank_map[taxid] = rank

    return taxid_to_parent, rank_map

def read_names_dmp(names_dmp_path):
    taxid_to_name = {}

    with open(names_dmp_path, "r") as names_file:
        lines = names_file.readlines()
        for line in tqdm(lines, desc="Reading names.dmp", unit=" lines"):
            line_parts = line.strip().split("|")
            taxid = line_parts[0].strip()
            name = line_parts[1].strip()
            name_type = line_parts[3].strip()

            if name_type == "scientific name":
                taxid_to_name[taxid] = name

    return taxid_to_name

def build_taxonomic_graph(taxid_to_parent):
    G = nx.DiGraph()
    for child_taxid, parent_taxid in taxid_to_parent.items():
        G.add_edge(parent_taxid, child_taxid)
    return G

def get_all_subtaxids(taxonomic_graph, input_taxid):
    sub_taxids = nx.descendants(taxonomic_graph, input_taxid)
    sub_taxids.add(input_taxid)
    return sub_taxids

def main():
    parser = argparse.ArgumentParser(description="Generate a table of TaxIDs and corresponding names.")
    parser.add_argument("--nodes", required=True, help="Path to nodes.dmp")
    parser.add_argument("--names", required=True, help="Path to names.dmp")
    parser.add_argument("--taxid", required=True, help="Input TaxID to start from")
    parser.add_argument("--out", required=True, help="Output file for the table")
    args = parser.parse_args()

    taxid_to_parent, rank_map = read_nodes_dmp(args.nodes)
    taxid_to_name = read_names_dmp(args.names)

    input_taxid = args.taxid
    taxonomic_graph = build_taxonomic_graph(taxid_to_parent)

    sub_taxids = get_all_subtaxids(taxonomic_graph, str(input_taxid))  # Ensure input_taxid is a string

    with open(args.out, "w") as out_file:
        out_file.write("TaxID\tScientific Name\n")

        for taxid in tqdm(sub_taxids, desc="Writing taxids to file", unit=" taxids"):
            name = taxid_to_name.get(taxid, "Unknown")
            out_file.write(f"{taxid}\t{name}\n")

    print("Output written to", args.out)

if __name__ == "__main__":
    main()
