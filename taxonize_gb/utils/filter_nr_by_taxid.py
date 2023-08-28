"""
Script Name: filter_nr_by_taxid.py
Description: This script filters nr database based on a given taxid.
Author: Mohamed S. Sarhan
Contact: mohamed.sarhan@eurac.edu; m.sabrysarhan@gmail.com
Date Created: August 18, 2023
Version: 1.0
"""
import os
import argparse
import hashlib
import tarfile
import subprocess
import gzip
import networkx as nx
from tqdm import tqdm

databases = {
    "nr" : ["https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz", "https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nr.gz.md5"],
    "taxdb" : ["https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz", "https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz.md5"],
    "protacc2taxid" : ["https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz","https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/prot.accession2taxid.gz.md5"]
}


def check_out_directory(directory_name):
    if not os.path.exists(directory_name):
        try:
            os.mkdir(directory_name)
            print(f"Out directory '{directory_name}' created successfully.")
        except OSError as e:
            print(f"Failed to create directory '{directory_name}': {e}")
    else:
        print(f"Directory '{directory_name}' already exists.")

def list_files_with_extension(directory, extension):
    files = {}
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            file_base = os.path.splitext(filename)[0]
            file_path = os.path.abspath(os.path.join(directory, filename))
            absolute_path = os.path.abspath(file_path)
            files[file_base] = absolute_path
    return files

def check_nr_db(nr, out):
    print("\nChecking the protein nr database")
    # First, we need to check whether the nr database is provided or not
    # If not, we need to download it.
    if nr == False:
        print("No nr database provided.\n")
        print("The latest nr database will be downloaded from the NCBI")
        try:
            # download the nr compressed fasta file
            nr_url = databases["nr"][0]
            #wget.download(nr_url, os.path.join(out, os.path.basename(nr_url)), bar=wget.bar_adaptive)
            wget_command = ['wget', '-c', nr_url, '-O', os.path.join(out, os.path.basename(nr_url))]
            # Execute the wget command
            try:
                subprocess.run(wget_command, check=True)
                print("Download completed or resumed successfully.")
            except subprocess.CalledProcessError as e:
                print("Error:", e)


            # download the nr md5 compressed file
            md5_url = databases["nr"][1]
            wget_command = ['wget', '-c', md5_url, '-O', os.path.join(out, os.path.basename(md5_url))]
            # Execute the wget command
            try:
                subprocess.run(wget_command, check=True)
                print("Download completed or resumed successfully.")
            except subprocess.CalledProcessError as e:
                print("Error:", e)



            #wget.download(md5_url, os.path.join(out, os.path.basename(md5_url)), bar=wget.bar_adaptive)

            # read the expected md5
            with open(os.path.join(out, os.path.basename(md5_url)), "r") as f:
                expected_md5 = f.readline().strip().split(" ")[0]

            # calculate MD5 hash of the decompressed file
            nr_md5 = hashlib.md5()
            with open(os.path.join(out, os.path.basename(nr_url)), "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    nr_md5.update(chunk)

            # compare the calculated MD5 with the expected MD5
            if nr_md5.hexdigest() == expected_md5:
                print(f"The latest version of the nr database has been downloaded successfully to {out}")
                return os.path.join(out, os.path.basename(nr_url))
            else:
                print("MD5 checksum does not match. File might be corrupted.")

        except Exception as e:
            print("\nDownload failed:", e)


    # If the nr is provided, then print the path and continue to the next step.
    elif nr != False:
        print(f"nr database is provided in {nr}")
        return nr

def check_taxdb(taxdb, out):
    print("\nChecking the taxonomy database")
    # This function checks whether there is a taxdb is provided or not
    # if not, the latest version will be downloaded
    # The function will also untar the gzipped file to the out directory
    if taxdb == False:
        print("No taxdb database provided.")
        print("The latest version of taxonomy database will be downloaded from the NCBI")
        try:
            # download the taxdb compressed fasta file
            taxdb_url = databases["taxdb"][0]
            wget_command = ['wget', '-c', taxdb_url, '-O', os.path.join(out, os.path.basename(taxdb_url))]
            subprocess.run(wget_command, check=True)

            #wget.download(taxdb_url, os.path.join(out, os.path.basename(taxdb_url)), bar=wget.bar_adaptive)
            print("\nNCBI taxonomy database download complete.")

            # download the taxdb md5 compressed file
            md5_url = databases["taxdb"][1]
            wget_command = ['wget', '-c', md5_url, '-O', os.path.join(out, os.path.basename(md5_url))]
            subprocess.run(wget_command, check=True)
            #wget.download(md5_url, os.path.join(out, os.path.basename(md5_url)), bar=wget.bar_adaptive)
            print("\nNCBI taxonomy database MD5 download complete.")
            print("We will check the integerity of the downloaded database.")
            
            # read the expected md5
            with open(os.path.join(out, os.path.basename(md5_url)), "r") as f:
                expected_md5 = f.readline().strip().split(" ")[0]

            # calculate MD5 hash of the decompressed file

            taxdb_md5 = hashlib.md5()
            with open(os.path.join(out, os.path.basename(taxdb_url)), "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    taxdb_md5.update(chunk)

            print(expected_md5)
            print(taxdb_md5.hexdigest())

            # compare the calculated MD5 with the expected MD5
            if taxdb_md5.hexdigest() == expected_md5:
                print(f"The latest version of the taxdb database has been downloaded successfully to {out}")

                print(f"Extracting taxdb files to {out}")
                with tarfile.open(os.path.join(out, os.path.basename(taxdb_url)), 'r:gz') as tar:
                    tar.extractall(path=out)
                    print(f"Extraction of taxdb files to {out} is complete")
                    return list_files_with_extension(out, "dmp")

            else:
                print("MD5 checksum does not match. File might be corrupted.")

        except Exception as e:
            print("\nDownload failed:", e)

    # If the taxdb is provided, then print the path and continue to the next step.
    elif taxdb != False:
        print(f"taxdb database is provided in {taxdb}")
        print(f"Extracting taxdb files to {out}")
        with tarfile.open(taxdb, 'r:gz') as tar:
            tar.extractall(path=out)
            print(f"Extraction of taxdb files to {out} is complete")
            return list_files_with_extension(out, "dmp")

def check_acc2taxid(acc2taxid, out):
    print("\nChecking the protein accession to taxonomy ID mapping file")
    # This function checks whether there is a acc2taxid is provided or not
    # if not, the latest version will be downloaded
    if acc2taxid == False:
        print("No acc2taxid database provided.")
        print("The latest version of protein acc2taxid database will be downloaded from the NCBI")
        try:
            # download the acc2taxid compressed fasta file
            acc2taxid_url = databases["protacc2taxid"][0]
            wget_command = ['wget', '-c', acc2taxid_url, '-O', os.path.join(out, os.path.basename(acc2taxid_url))]
            subprocess.run(wget_command, check=True)
            #wget.download(acc2taxid_url, os.path.join(out, os.path.basename(acc2taxid_url)), bar=wget.bar_adaptive)
            print("\nprotein accession2taxid database download complete.")

            # download the acc2taxid md5 compressed file
            md5_url = databases["protacc2taxid"][1]
            wget_command = ['wget', '-c', md5_url, '-O', os.path.join(out, os.path.basename(md5_url))]
            subprocess.run(wget_command, check=True)
            #wget.download(md5_url, os.path.join(out, os.path.basename(md5_url)), bar=wget.bar_adaptive)
            print("\nprotein accession2taxid database MD5 download complete.")
            print("We will check the integerity of the downloaded database.")
            
            # read the expected md5
            with open(os.path.join(out, os.path.basename(md5_url)), "r") as f:
                expected_md5 = f.readline().strip().split(" ")[0]

            # calculate MD5 hash of the decompressed file
            acc2taxid_md5 = hashlib.md5()            
            with open(os.path.join(out, os.path.basename(acc2taxid_url)), "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    acc2taxid_md5.update(chunk)

            # compare the calculated MD5 with the expected MD5
            if acc2taxid_md5.hexdigest() == expected_md5:
                print(f"The latest version of the acc2taxid database has been downloaded successfully to {out}")
                return os.path.join(out, os.path.basename(acc2taxid_url))
            
            else:
                print("MD5 checksum does not match. File might be corrupted.")

        except Exception as e:
            print("\nDownload failed:", e)

    # If the acc2taxid is provided, then print the path and continue to the next step.
    elif acc2taxid != False:
        print(f"acc2taxid database is provided in {acc2taxid}")
        return acc2taxid

def read_nodes_dmp(nodes_dmp_path):
    taxid_to_parent = {}
    rank_map = {}

    with open(nodes_dmp_path, "r") as nodes_file:
        lines = nodes_file.readlines()
        for line in tqdm(lines, desc="Reading nodes.dmp", unit=" lines"):
            line_parts = line.strip().split("|")
            taxid = line_parts[0].strip()
            parent_taxid = line_parts[1].strip()
            rank = line_parts[2].strip()

            taxid_to_parent[taxid] = parent_taxid
            rank_map[taxid] = rank

    return taxid_to_parent, rank_map

def read_names_dmp(names_dmp_path):
    taxid_to_name = {}

    with open(names_dmp_path, "r") as names_file:
        lines = names_file.readlines()
        for line in tqdm(lines, desc="Reading names.dmp", unit=" lines"):
            line_parts = line.strip().split("|")
            taxid = line_parts[0].strip()
            name = line_parts[1].strip()
            name_type = line_parts[3].strip()

            if name_type == "scientific name":
                taxid_to_name[taxid] = name

    return taxid_to_name

def build_taxonomic_graph(taxid_to_parent):
    G = nx.DiGraph()
    for child_taxid, parent_taxid in taxid_to_parent.items():
        G.add_edge(parent_taxid, child_taxid)
    return G

def get_all_subtaxids(taxonomic_graph, input_taxid):
    sub_taxids = nx.descendants(taxonomic_graph, input_taxid)
    sub_taxids.add(input_taxid)
    return sub_taxids

def filter_acc2taxid(acc2taxid_path, taxidList_path, filtered_acc2taxid_path):
    target_taxids = set()
    
    with open(taxidList_path, "r") as taxid_list_file:
        for line in taxid_list_file:
            taxid = line.strip().split()[0]
            target_taxids.add(taxid)

    with gzip.open(acc2taxid_path, "rt") as acc2taxid_file, \
         gzip.open(filtered_acc2taxid_path, "wt") as filtered_acc2taxid_file:

        for line in tqdm(acc2taxid_file, desc="Processing acc2taxid", unit=" lines"):
            ver, acc, taxid, gi = line.strip().split("\t")
            if taxid in target_taxids:
                #filtered_acc2taxid_file.write(f"{acc}\t.\t{taxid}\t.\n")
                filtered_acc2taxid_file.write(f"{acc}\t{taxid}\n")

    print("Filtered acc2taxid file written:", filtered_acc2taxid_path)

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

def main():
    parser = argparse.ArgumentParser(description="Filter NCBI nr protein database based on a given taxid.")
    parser.add_argument("--nr", required=False, help="Path to nr gzipped fasta file (if not provided, the latest version will be downloaded from the NCBI", default=False)
    parser.add_argument("--taxdb", required=False, help="Path to nr gzipped taxonomy database from the NCBI (if not provided, the latest version will be downloaded from the NCBI", default=False)
    parser.add_argument("--acc2taxid", required=False, help="Path to nr gzipped protein accession number to taxid mapping file from the NCBI (if not provided, the latest version will be downloaded from the NCBI", default=False)
    parser.add_argument("--taxid", required=False, help="Target taxonomy ID to filter for", default=1)
    parser.add_argument("--out", required=False, help="Path to output directory where the results are to be stored.", default=".")
    args = parser.parse_args()

 
    check_out_directory(args.out)
    nr_fasta = check_nr_db(args.nr, args.out)
    accession2taxid = check_acc2taxid(args.acc2taxid, args.out)

    taxdb_dict = check_taxdb(args.taxdb, args.out)

    taxid_to_parent, rank_map = read_nodes_dmp(taxdb_dict["nodes"])
    taxid_to_name = read_names_dmp(taxdb_dict["names"])

    input_taxid = args.taxid
    taxonomic_graph = build_taxonomic_graph(taxid_to_parent)

    sub_taxids = get_all_subtaxids(taxonomic_graph, str(input_taxid))

    filtered_taxdb = os.path.join(args.out, "filtered_taxid_"+str(args.taxid)+".tsv")

    with open(filtered_taxdb, "w") as out_file:
        out_file.write("TaxID\tScientific Name\n")

        for taxid in tqdm(sub_taxids, desc="Writing taxids to file", unit=" taxids"):
            name = taxid_to_name.get(taxid, "Unknown")
            out_file.write(f"{taxid}\t{name}\n")

    print(f"Filtered {args.taxid} nodes written to", filtered_taxdb)

    filteredAcc2taxid = os.path.join(args.out, f"taxid{args.taxid}_prot.accession2taxid.gz")

    filter_acc2taxid(accession2taxid, filtered_taxdb, filteredAcc2taxid)

    filteredFasta = os.path.join(args.out, f"taxid{args.taxid}_nr.fasta.gz")
    filter_fasta_by_acc2taxid(nr_fasta, filteredAcc2taxid, filteredFasta)


    #filter_fasta_by_acc2taxid(nr_fasta, filteredAcc2taxid, filteredFasta)
    # --onlydownload --removetemp 

    # filter_fasta_by_acc2taxid(args.fasta, args.filteredAcc2taxid, args.filteredFasta)
    

if __name__ == "__main__":
    main()


