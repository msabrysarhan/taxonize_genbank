# Description: This module contains functions to filter fasta files based on keywords and accession to taxid mapping files.
from Bio import SeqIO
import io
import isal.igzip as gzip 
import csv
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
import isal.igzip as gzip  # Faster than Python's gzip
from Bio import SeqIO
from tqdm import tqdm

def filter_fasta_by_acc2taxid(input_fasta, output_fasta, table_file, chunk_size=10**6):
    """
    Efficiently filters a FASTA file based on an accession-to-taxid table.

    Args:
        input_fasta (str): Path to input FASTA file (gzipped).
        output_fasta (str): Path to output filtered FASTA file (gzipped).
        table_file (str): Path to an accession-to-taxid file (gzipped, 4-column format).
        chunk_size (int, optional): Number of sequences processed per chunk. Default is 1 million.
    """

    # Load accessions to filter into a set for fast lookup
    values_to_filter = set()
    with gzip.open(table_file, "rt") as table:
        for line in tqdm(table, desc="Loading accessions", unit=" lines"):
            parts = line.strip().split()
            if len(parts) > 1:
                values_to_filter.add(parts[1])  # Extract the second column (accession version)

    # Process FASTA file in chunks
    with gzip.open(input_fasta, "rt") as input_handle, gzip.open(output_fasta, "wt") as output_handle:
        writer = SeqIO.FastaIO.FastaWriter(output_handle, wrap=60)
        buffer = []  # Store records before batch writing

        for record in tqdm(SeqIO.parse(input_handle, "fasta"), desc="Processing sequences", unit=" seq"):
            header = record.description
            identifier = header.split()[0]

            # Filter by accession
            if identifier in values_to_filter:
                buffer.append(record)

            # Write in chunks to improve I/O efficiency
            if len(buffer) >= chunk_size:
                writer.write_file(buffer)
                buffer.clear()

        # Write remaining sequences
        if buffer:
            writer.write_file(buffer)

    print(f"The filtered sequences are written to {output_fasta}")



# Filter fasta by list of keywords and acc2taxid

def filter_fasta_by_acc2taxid_and_keywords(input_fasta, output_fasta, table_file, search_words, chunk_size=10**6):
    """
    Efficiently filters a FASTA file based on keywords and a taxid table.

    Args:
        input_fasta (str): Path to input FASTA file (gzipped).
        output_fasta (str): Path to output filtered FASTA file (gzipped).
        table_file (str): Path to a two-column table file (accessions and taxids).
        search_words (list): List of keywords for filtering.
        chunk_size (int, optional): Number of sequences processed per chunk. Default is 1 million.
    """

    # Load accessions to filter into a set for fast lookup
    values_to_filter = set()
    with gzip.open(table_file, "rt") as table:
        for line in tqdm(table, desc="Loading accessions", unit=" lines"):
            parts = line.strip().split()
            if len(parts) > 1:
                values_to_filter.add(parts[1])  # Extract second column (accession)

    # Process FASTA file in chunks
    with gzip.open(input_fasta, "rt") as input_handle, gzip.open(output_fasta, "wt") as output_handle:
        writer = SeqIO.FastaIO.FastaWriter(output_handle, wrap=60)
        buffer = []  # Store records before batch writing

        for record in tqdm(SeqIO.parse(input_handle, "fasta"), desc="Processing sequences", unit=" seq"):
            header = record.description
            identifier = header.split()[0]

            # Filter by accession & keywords
            if identifier in values_to_filter and all(word in header for word in search_words):
                buffer.append(record)

            # Write in chunks to improve I/O efficiency
            if len(buffer) >= chunk_size:
                writer.write_file(buffer)
                buffer.clear()

        # Write remaining sequences
        if buffer:
            writer.write_file(buffer)

    print(f"The filtered sequences are written to {output_fasta}")





def filter_acc2taxid_by_table(acc2taxid_path, acc2taxid_path2, taxidList_path, filtered_acc2taxid_path, chunk_size=10**6):
    """
    Efficiently filters large accession-to-taxid mapping files using chunked processing.

    Args:
        acc2taxid_path (str): Path to the 1st input mapping file.
        acc2taxid_path2 (str): Path to the 2nd input mapping file.
        taxidList_path (str): Path to the file containing taxids to filter.
        filtered_acc2taxid_path (str): Path to the output filtered mapping file.
        chunk_size (int, optional): Number of lines to process in each chunk. Default is 1 million.
    """

    # Load target taxids into a set for fast lookup
    target_taxids = set()
    with open(taxidList_path, "r") as taxid_list_file:
        for line in taxid_list_file:
            taxid = line.strip().split()[0]  # Extract taxid (first column)
            target_taxids.add(taxid)

    # Open output file with gzip writing
    with gzip.open(filtered_acc2taxid_path, "wt") as filtered_acc2taxid_file:
        writer = csv.writer(filtered_acc2taxid_file, delimiter="\t", lineterminator="\n")
        writer.writerow(["accession", "accession.version", "taxid", "gi"])  # Write header

        def process_file(file_path):
            """Process a file in chunks and filter relevant taxids."""
            with gzip.open(file_path, "rt") as acc2taxid_file:
                buffer = []  # Temporary storage for batch writes
                for line in tqdm(acc2taxid_file, desc=f"Processing {file_path}", unit=" lines"):
                    parts = line.strip().split("\t")
                    if len(parts) == 4:  # Ensure correct format
                        ver, acc, taxid, gi = parts
                        if taxid in target_taxids:
                            buffer.append([ver, acc, taxid, gi])

                    # Write in chunks to avoid excessive I/O operations
                    if len(buffer) >= chunk_size:
                        writer.writerows(buffer)
                        buffer.clear()

                # Write remaining lines in the buffer
                if buffer:
                    writer.writerows(buffer)

        # Process both input files
        process_file(acc2taxid_path)
        process_file(acc2taxid_path2)

    print(f"Filtered acc2taxid file written: {filtered_acc2taxid_path}")


