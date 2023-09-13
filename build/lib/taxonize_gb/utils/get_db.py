#!/usr/bin/env python3
"""
Script Name: get_db.py
Description: This script downloads any given db from the genbank.
Author: Mohamed S. Sarhan
Affiliation: Institute for Biomedicine, Eurac Research, Bolzano 39100, Italy
Contact: mohamed.sarhan@eurac.edu; m.sabrysarhan@gmail.com
Date Created: August 21, 2023
Version: 1.0
"""
# Python modules to be imported and used in this script
import os 
import argparse
import hashlib
import subprocess

# Reference NCBI databases, to be downloaded in case they are not provided in the input paramters
databases = {
    "taxdb" : ["https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz", "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz.md5"],
    "nr" : ["https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz", "https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz.md5"],
    "prot_acc2taxid" : ["https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz","https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz.md5"],
    "nt" : ["https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz", "https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz.md5"],
    "nucl_gb_acc2taxid" : ["https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz", "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz.md5"],
    "nucl_wgs_acc2taxid" : ["https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_wgs.accession2taxid.gz", "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_wgs.accession2taxid.gz.md5"],
    "pdb_acc2taxid" : ["https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/pdb.accession2taxid.gz","https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/pdb.accession2taxid.gz.md5"]
}
def check_out_directory(directory_name):
    """
    This function is to create the output directory in case it is not yet created.
    """
    if not os.path.exists(directory_name):
        try:
            os.mkdir(directory_name)
            print(f"Out directory '{directory_name}' created successfully.")
        except OSError as e:
            print(f"Failed to create directory '{directory_name}': {e}")
    else:
        print(f"Directory '{directory_name}' already exists.")


def download_db(db, out):
    """
    This function download NCBI databases to a specified output directory.
    It downloads the database and its MD5 hashes and checkes the file integrity
    after download, then returns the downloaded path. 

    Args:
        db (string): names of the database to be downloaded. It must be present 
        in the dictionary 'databases'
        out (string): output directory where the output is to be stored.

    Returns:
        path to the downloaded database path.
    """
    if db in databases:
        print(f"The {db} will bw downloaded to {out}")
        try:
            db_url = databases[db][0]
            wget_command = ['wget', '-c', db_url, '-O', os.path.join(out, os.path.basename(db_url))]
            subprocess.run(wget_command, check=True)

            db_md5 = databases[db][1]
            wget_command = ['wget', '-c', db_md5, '-O', os.path.join(out, os.path.basename(db_md5))]
            subprocess.run(wget_command, check=True)
            with open(os.path.join(out, os.path.basename(db_md5)), "r") as f:
                expected_md5 = f.readline().strip().split(" ")[0]

            downloaded_md5 = hashlib.md5()            
            with open(os.path.join(out, os.path.basename(db_url)), "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    downloaded_md5.update(chunk)

            # compare the calculated MD5 with the expected MD5
            if downloaded_md5.hexdigest() == expected_md5:
                print(f"The {db} has been downloaded to {out}")
                path = os.path.join(out, os.path.basename(db_url))
                return path
            
            else:
                print("MD5 checksum does not match. File might be corrupted.")            

        except Exception as e:
            print("\nDownload failed:", e)
    else:
        print(f"{db} is not included in our database set.")
        exit


def main():
    parser = argparse.ArgumentParser(description="Download NCBI databases.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--db_name", required=True, help="Which NCBI database to be downloaded.\n"
                        "Possible values are the following:\n"
                        "'taxdb': The NCBI taxonomy dump database files.\n"
                        "'nr': The non-redundant protein database.\n"
                        "'nt': The non-redundant nucleotide database.\n"
                        "'prot_acc2taxid': GenBank protein accession number to taxonomy ID mapping file.\n"
                        "'pdb_acc2taxid': Protein Database (PDB) accession number to taxonomy ID mapping file.\n" 
                        "'nucl_gb_acc2taxid': Nucleotide (GenBank, GB) accession number to taxonomy ID mapping file.\n"
                        "'nucl_wgs_acc2taxid': Nucleotide (Whole Genome Shotgun, WGS) accession number to taxonomy ID mapping file.\n", default=False)
    parser.add_argument("--out", required=True, help="Path to output directory where the results are to be stored.", default=False)
    args = parser.parse_args()

    check_out_directory(args.out)
    download_db(args.db_name, args.out)

if __name__ == "__main__":
    main()