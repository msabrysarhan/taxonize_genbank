from ete3 import NCBITaxa

def get_full_lineage(taxid):
    ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(taxid)
    names = ncbi.get_taxid_translator(lineage)
    full_lineage_names = [names[taxid].replace(" ", "_") for taxid in lineage]
    return ";".join(full_lineage_names)



def parse_nodes_dmp(nodes_file):
    # Create a dictionary to store taxid-to-parent mapping
    taxid_to_parent = {}

    # Parse nodes.dmp file
    with open(nodes_file, 'r') as f:
        for line in f:
            fields = line.strip().split('\t|\t')
            taxid, parent_taxid = int(fields[0]), int(fields[1])
            taxid_to_parent[taxid] = parent_taxid

    return taxid_to_parent

def parse_names_dmp(names_file):
    # Create a dictionary to store taxid-to-name mapping
    taxid_to_name = {}

    # Parse names.dmp file
    with open(names_file, 'r') as f:
        for line in f:
            fields = line.strip().split('\t|\t')
            taxid = int(fields[0])
            name = fields[1]
            name_type = fields[3].strip()
            if name_type == "scientific name":
                taxid_to_name[taxid] = name

    return taxid_to_name

def get_full_lineage(taxid, taxid_to_parent, taxid_to_name):
    lineage = []
    while taxid != 1:  # 1 is the root taxid (root of all life)
        lineage.append((taxid, taxid_to_name.get(taxid, 'Unknown')))
        taxid = taxid_to_parent.get(taxid)
    lineage.append((1, 'root'))  # Add the root taxid to the lineage
    lineage.reverse()
    return lineage

# Example usage:
nodes_file = '/home/msarhan/test_taxonize_PlantITS/nodes.dmp'
names_file = '/home/msarhan/test_taxonize_PlantITS/names.dmp'
taxid_to_parent = parse_nodes_dmp(nodes_file)
taxid_to_name = parse_names_dmp(names_file)
taxid = 9606  # Example taxid for Homo sapiens
lineage = get_full_lineage(taxid, taxid_to_parent, taxid_to_name)

for taxid, name in lineage:
    print(f"TaxID: {taxid}, Name: {name}")
