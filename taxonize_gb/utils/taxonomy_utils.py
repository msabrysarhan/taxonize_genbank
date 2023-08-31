from ete3 import NCBITaxa

def get_full_lineage(taxid):
    ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(taxid)
    names = ncbi.get_taxid_translator(lineage)
    full_lineage_names = [names[taxid].replace(" ", "_") for taxid in lineage]
    return ";".join(full_lineage_names)




