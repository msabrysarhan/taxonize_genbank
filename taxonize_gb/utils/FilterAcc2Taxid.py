import argparse
import gzip
from tqdm import tqdm  # Import tqdm for loading bars

def filter_acc2taxid(acc2taxid_path, taxidList_path, filtered_acc2taxid_path):
    target_taxids = set()
    with open(taxidList_path, "r") as taxid_list_file:
        for line in taxid_list_file:
            taxid = line.strip().split()[0]
            target_taxids.add(taxid)

    with gzip.open(acc2taxid_path, "rt") as acc2taxid_file, \
         gzip.open(filtered_acc2taxid_path, "wt") as filtered_acc2taxid_file:

        for line in tqdm(acc2taxid_file, desc="Processing acc2taxid", unit=" lines"):
            _, acc, taxid, _ = line.strip().split("\t")
            if taxid in target_taxids:
                #filtered_acc2taxid_file.write(f"{acc}\t.\t{taxid}\t.\n")
                filtered_acc2taxid_file.write(f"{acc}\t{taxid}\n")

    print("Filtered acc2taxid file written:", filtered_acc2taxid_path)

def main():
    parser = argparse.ArgumentParser(description="Filter acc2taxid file based on taxidList.")
    parser.add_argument("--acc2taxid", required=True, help="Path to acc2taxid file (gzipped 4-column)")
    parser.add_argument("--taxidList", required=True, help="Path to taxidList file (two-column)")
    parser.add_argument("--filteredAcc2taxid", required=True, help="Path to output filtered acc2taxid file")
    args = parser.parse_args()

    filter_acc2taxid(args.acc2taxid, args.taxidList, args.filteredAcc2taxid)

if __name__ == "__main__":
    main()
