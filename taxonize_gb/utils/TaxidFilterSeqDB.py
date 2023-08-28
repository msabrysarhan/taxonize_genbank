import argparse
import gzip
from tqdm import tqdm  # Import tqdm for loading bars


def filter_fasta_by_acc2taxid(fasta_path, filtered_acc2taxid_path, filtered_fasta_path):
    filtered_acc2taxid_dict = {}
    with gzip.open(filtered_acc2taxid_path, "rt") as filtered_acc2taxid_file:
        for line in filtered_acc2taxid_file:
            acc, taxid = line.strip().split("\t")
            filtered_acc2taxid_dict[acc] = taxid

    with gzip.open(fasta_path, "rt") as fasta_file, \
         gzip.open(filtered_fasta_path, "wt") as filtered_fasta_file:

        current_sequence = []
        current_acc = None

        for line in tqdm(fasta_file, desc="Processing FASTA", unit=" lines"):
            line = line.strip()

            if line.startswith(">"):
                if current_sequence and current_acc in filtered_acc2taxid_dict:
                    filtered_fasta_file.write(f">{current_acc}\n")
                    filtered_fasta_file.write("\n".join(current_sequence) + "\n")

                current_sequence = []
                current_acc = line[1:].split()[0]
            else:
                current_sequence.append(line)

        if current_sequence and current_acc in filtered_acc2taxid_dict:
            filtered_fasta_file.write(f">{current_acc}\n")
            filtered_fasta_file.write("\n".join(current_sequence) + "\n")

    print("Filtered FASTA file written:", filtered_fasta_path)
'''
def filter_fasta_by_acc2taxid(fasta_path, filtered_acc2taxid_path, filtered_fasta_path):
    filtered_acc2taxid_dict = {}
    with gzip.open(filtered_acc2taxid_path, "rt") as filtered_acc2taxid_file:
        for line in tqdm(filtered_acc2taxid_file, desc="Processing filtered acc2taxid", unit=" lines"):
            acc, taxid = line.strip().split("\t")
            filtered_acc2taxid_dict[acc] = taxid

    with gzip.open(fasta_path, "rt") as fasta_file, \
         gzip.open(filtered_fasta_path, "wt") as filtered_fasta_file:

        current_sequence = ""
        write_sequence = False
        current_acc = None

        for line in tqdm(fasta_file, desc="Processing FASTA", unit=" lines"):
            line = line.strip()

            if line.startswith(">"):
                if current_sequence and write_sequence:
                    filtered_fasta_file.write(f">{line}\n{current_sequence}\n")
                current_sequence = ""
                current_acc = line[1:].split()[0]
                print(current_acc)
                taxid = filtered_acc2taxid_dict.get(current_acc)
                write_sequence = (taxid is not None)
            else:
                if write_sequence:
                    current_sequence += line

        if current_sequence and write_sequence:
            filtered_fasta_file.write(f">{current_acc}\n{current_sequence}\n")

    print("Filtered FASTA file written:", filtered_fasta_path)
'''
def main():
    parser = argparse.ArgumentParser(description="Filter FASTA file based on filtered acc2taxid.")
    parser.add_argument("--fasta", required=True, help="Path to input FASTA file (gzipped)")
    parser.add_argument("--filteredAcc2taxid", required=True, help="Path to filtered acc2taxid file (gzipped)")
    parser.add_argument("--filteredFasta", required=True, help="Path to output filtered FASTA file")
    args = parser.parse_args()

    filter_fasta_by_acc2taxid(args.fasta, args.filteredAcc2taxid, args.filteredFasta)

if __name__ == "__main__":
    main()
