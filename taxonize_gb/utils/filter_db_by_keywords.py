import argparse
from filter_utils import filter_fasta_by_keywords, filter_fasta_by_acc2taxid_and_keywords


def main():
    parser = argparse.ArgumentParser(description="filter gzipped fasta file by keywords", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--db_path", required=True, help="gzipped fasta file which you would like to filter.", default=False)
    parser.add_argument("--acc2taxid", required=False, help="gzipped accession number to taxonomy ID mapping file", default=False)
    parser.add_argument("--keywords", required=True, help="list of keywords you want to search for, comma-separated, 'complete genome',chloroplast", default=False)
    parser.add_argument("--out", required=True, help="Path to output directory where the results are to be stored.", default=False)
    args = parser.parse_args()

    input_file = args.db_path
    output_file = args.out
    keywords = [word.strip() for word in args.keywords.split(",")]
    print("Received keywords:", keywords)

    if args.acc2taxid == False:
        filter_fasta_by_keywords(input_file, keywords, output_file)
    else:
        filter_fasta_by_acc2taxid_and_keywords(input_file, output_file, args.acc2taxid, keywords)

if __name__ == "__main__":
    main()
