import gzip
from collections import defaultdict
from tqdm import tqdm  # Import tqdm for loading bars
from ete3 import NCBITaxa
# Function to retrieve full lineage using taxid (replace this with your actual function)
def get_full_lineage(taxid):
    ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(taxid)
    names = ncbi.get_taxid_translator(lineage)
    full_lineage_names = [names[taxid].replace(" ", "_") for taxid in lineage]
    return ";".join(full_lineage_names)


def parse_acc2taxonomy(acc2tax_file):
    acc2tax = {}
    with gzip.open(acc2tax_file, 'rt') as f:
        for line in tqdm(f, desc="Reading accessions"):
            fields = line.strip().split('\t')
            acc2tax[fields[1]] = fields[2]
    return acc2tax

def main(fasta_file, acc2tax_file, output_file):
    acc2tax = parse_acc2taxonomy(acc2tax_file)

    with gzip.open(fasta_file, 'rt') as fasta, open(output_file, 'w') as output:
        for line in tqdm(fasta, desc="Processing FASTA"):
            if line.startswith('>'):
                accession = line.strip().split()[0][1:]  # Extract accession from the header
                if accession in acc2tax:
                    taxid = acc2tax[accession]
                    lineage = get_full_lineage(taxid)
                    output.write(f"{accession}\t{taxid}\t{lineage}\n")

if __name__ == "__main__":
    fasta_file = "/home/msarhan/test_taxonize_PlantITS/taxid33090_nt.fasta.gz"  # Replace with your input FASTA file
    acc2tax_file = "/home/msarhan/test_taxonize_PlantITS/taxid33090_nt.accession2taxid.gz"  # Replace with your input acc2taxonomy file
    output_file = "/home/msarhan/test_taxonize_PlantITS/taxid33090_nt.taxonomy.tsv"  # Replace with the desired output file name
    
    main(fasta_file, acc2tax_file, output_file)
