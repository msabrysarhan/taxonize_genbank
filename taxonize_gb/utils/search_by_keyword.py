from Bio import SeqIO
import gzip
from tqdm import tqdm  # Import tqdm for the loading bar

def search_fasta(fasta_file, search_words, output_file):
    matching_sequences = []

    with gzip.open(fasta_file, "rt") as input_fasta:
        with gzip.open(output_file, 'wt') as output_fasta:

            # Use tqdm to wrap the loop for the loading bar
            for record in tqdm(SeqIO.parse(input_fasta, "fasta"), desc="Processing sequences", unit="seq"):
                header = record.description
                sequence = str(record.seq)

                # Check if all search words are present in the header
                if all(word in header for word in search_words):
                    output_fasta.write(f">{header}\n{sequence}\n")
                    matching_sequences.append((header, sequence))
                    # No need to print header, it's already shown in the tqdm loading bar

    return output_file

def main():
    fasta_file = "/home/msarhan/Feces2Food/databases/NR_nucleotides/nt.gz"
    search_words = ["mitochondrion", "complete genome"]  # Add the words you want to search for
    output_file = "/home/msarhan/Feces2Food/tests/db_test/test2_mito.fasta.gz"

    matching_sequences = search_fasta(fasta_file, search_words, output_file)

    # for header, sequence in matching_sequences:
    #     print("Header:", header)
    #     print("Sequence:", sequence)
    #     print("=" * 40)

if __name__ == "__main__":
    main()
