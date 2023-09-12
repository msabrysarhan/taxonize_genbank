import gzip
from Bio import SeqIO
from tqdm import tqdm


# Filter fasta by list of keywords

def filter_fasta_by_keywords(fasta_file, search_words, output_file):
    """
    This function filter fasta file based on given keywords.

    Args:
        fasta_file (string): path to input fasta file.
        search_words (list): list of keywords given by the user.
    Returns:
        output_file (string): path to the output filtered fasta file.
    """
    with gzip.open(fasta_file, "rt") as input_fasta:
        with gzip.open(output_file, 'wt') as output_fasta:

            # Use tqdm to wrap the loop for the loading bar
            for record in tqdm(SeqIO.parse(input_fasta, "fasta"), desc="Processing sequences", unit="seq"):
                header = record.description
                sequence = str(record.seq)

                # Check if all search words are present in the header
                if all(word in header for word in search_words):
                    output_fasta.write(f">{header}\n{sequence}\n")

    print(f"The filtered sequences are wrritten to {output_file}")


# Filter fasta by acc2taxid table
def filter_fasta_by_acc2taxid(input_fasta, output_fasta, table_file):
    """
    This function filter fasta file based on accession number to taxids file
    from the NCBI databases.

    Args:
        input_fasta (string): path to input fasta file.
        table_file (string): path to accession to taxids file - 
        this file should contain 4 columns (accession, version, taxid, gi).
    Returns:
        output_fasta (string): path to the output filtered fasta file.
    """
    values_to_filter = set()
    with gzip.open(table_file, "rt") as table:
        for line in tqdm(table,  desc="Processing accessions", unit="lines"):
            value = line.strip().split()[1]
            values_to_filter.add(value)

    with gzip.open(input_fasta, "rt") as input_handle:
        with gzip.open(output_fasta, 'wt') as output_handle:

            # Use tqdm to wrap the loop for the loading bar
            for record in tqdm(SeqIO.parse(input_handle, "fasta"), desc="Processing sequences", unit="seq"):
                header = record.description
                sequence = str(record.seq)
                identifier = header.split()[0]

                if identifier in values_to_filter:
                    output_handle.write(f">{header}\n{sequence}\n")
    print(f"The filtered sequences are wrritten to {output_fasta}")


# Filter fasta by list of keywords and acc2taxid

def filter_fasta_by_acc2taxid_and_keywords(input_fasta, output_fasta, table_file, search_words):
    """
    This function filter fasta file based on given keywords and taxid table.

    Args:
        input_fasta (string): path to input fasta file.
        search_words (list): list of keywords given by the user.
        table_file (string): path to two-column table file (taxids and names).
    Returns:
        output_fasta (string): path to the output filtered fasta file.
    """
    values_to_filter = set()
    with gzip.open(table_file, "rt") as table:
        for line in tqdm(table,  desc="Processing accessions", unit="lines"):
            value = line.strip().split()[1]
            values_to_filter.add(value)

    with gzip.open(input_fasta, "rt") as input_handle:
        with gzip.open(output_fasta, 'wt') as output_handle:

            # Use tqdm to wrap the loop for the loading bar
            for record in tqdm(SeqIO.parse(input_handle, "fasta"), desc="Processing sequences", unit="seq"):
                header = record.description
                sequence = str(record.seq)
                identifier = header.split()[0]

                if identifier in values_to_filter and all(word in header for word in search_words):
                    output_handle.write(f">{header}\n{sequence}\n")
    print(f"The filtered sequences are wrritten to {output_fasta}")



def filter_acc2taxid_by_table(acc2taxid_path, acc2taxid_path2, taxidList_path, filtered_acc2taxid_path):
    """
    This function filter accession number to taxids mapping file for the taxids included in 
     another file containing taxids and scientific names.
     In case of protein databases, there are two mapping files, one for the NCBI accessions 
     and one for the PDB accessions.
     While in case of nucleotide databases, there are two files, one for the genbank accessions,
     and one for the whole genome shotgun accessions (WGS).

    Args:
        acc2taxid_path (string): path to 1st input mapping file.
        acc2taxid_path2 (string): path to 2nd input mapping file.
        taxidList_path (string): path to two-column table file (taxids and names).
    Returns:
        filtered_acc2taxid_path (string): path to the output filtered mapping file.
    """
    target_taxids = set()
    
    with open(taxidList_path, "r") as taxid_list_file:
        for line in taxid_list_file:
            taxid = line.strip().split()[0]
            target_taxids.add(taxid)

    with gzip.open(acc2taxid_path, "rt") as acc2taxid_file, \
        gzip.open(filtered_acc2taxid_path, "wt") as filtered_acc2taxid_file:
        filtered_acc2taxid_file.write("accession\taccession.version\ttaxid\tgi\n")
        

        for line in tqdm(acc2taxid_file, desc="Processing acc2taxid", unit=" lines"):
            ver, acc, taxid, gi = line.strip().split("\t")
            if taxid in target_taxids:
                filtered_acc2taxid_file.write(f"{ver}\t{acc}\t{taxid}\t{gi}\n")

        with gzip.open(acc2taxid_path2, "rt") as acc2taxid_file2:
            for line in tqdm(acc2taxid_file2, desc="Processing acc2taxid", unit=" lines"):
                ver, acc, taxid, gi = line.strip().split("\t")
                if taxid in target_taxids:
                    filtered_acc2taxid_file.write(f"{ver}\t{acc}\t{taxid}\t{gi}\n")

    print("Filtered acc2taxid file written:", filtered_acc2taxid_path)
