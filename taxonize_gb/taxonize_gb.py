#!/usr/bin/env python3
"""
Script Name: taxonize_gb.py
Description: This script filters db (nt/nr) database based on a given taxid and optionally keywords.
Author: Mohamed S. Sarhan
Affiliation: Institute for Biomedicine, Eurac Research, Bolzano 39100, Italy
Contact: mohamed.sarhan@eurac.edu; m.sabrysarhan@gmail.com
Date Created: August 21, 2023
Version: 1.0
"""
# Python modules to be imported and used in this script
from taxonize_gb.utils.get_db import databases, download_db, check_out_directory
from taxonize_gb.utils.filter_utils import filter_acc2taxid_by_table, filter_fasta_by_acc2taxid_and_keywords, filter_fasta_by_acc2taxid
import os 
import argparse
import tarfile
import gzip
import networkx as nx
from tqdm import tqdm


def check_input(input_param, input_db, out):
    """
    This function checks the input paramters provided by the user.
     
    If the input parameter is given by the user the function returns
    a string of the path the user provided, and if not, it will recall
    the function 'download_db' to download that database from the 
    genebank to the specified output directory and will return the 
    path of the downloaded file in the output directory. 
    
    Args:
        input_parm (string): relative or absolute path to a database file.
        input_db (string): database name as spicieifed in the help.
        out (string): reltive or absolute path to the directory spicified by the user.
    
    Returns:
        A string of either the path provided by the user or the path of the
        downloaded database.
    """
    if input_param == False:
        return download_db(input_db, out)
    elif input_param != False:
        print(f"database is provided in {input_param}")
        return input_param


def check_db(db):
    """"
    This function checks which NCBI FASTA database the user specified as input. 
    Whatever the user specifies, it will return the name of the database in 
    lowercase letters.

    Raises:
        If the user provided any database name other than nt ot nr, it will 
        return an error message and exit.
    """
    if str(db).lower() == "nt" or str(db).lower() == "nucleotide":
        print("You have chosen NCBI non-redundant nucleotide database (nt)")
        return "nt"
    elif str(db).lower() == "nr" or str(db).lower() == "protein":
        print("You have chosen NCBI non-redundant protein database (nr)")
        return "nr"
    else:
        print(f" {db} is not a valid option, please use either 'nt' or 'nr'")
        exit


def list_files_with_extension(directory, extension):
    """"
    This function lists all files with a given extension in a
    directory and store them in a dictionary.

    Args:
        directory (string): relative or absolute path to a directory.
        extension (string): extension of the files (with or without '.').
    
    Returns:
        A dictionary of all files having that extension in the given directory.
        The keys are the file names without the extensions, and the values are
        the absolute path to those files.
    """
    files = {}
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            file_base = os.path.splitext(filename)[0]
            file_path = os.path.abspath(os.path.join(directory, filename))
            absolute_path = os.path.abspath(file_path)
            files[file_base] = absolute_path
    return files


def check_taxdb(taxdb, out):
    """
    This function takes the path to the NCBI taxonomy database as input
    and untar it to the output directory provided by the user, then 
    returns a dictionary of its components (i.e., files end with .dmp). 
    """
    with tarfile.open(taxdb) as tar:
        tar.extractall(path=out)
        print(f"Extraction of taxdb files to {out} is complete")
        return list_files_with_extension(out, "dmp")


def read_nodes_dmp(nodes_dmp_path):
    """
    This function reads the nodes.dmp file of the NCBI taxonomy database.
    Then it creates a dictionry of taxids as keys and parent taxids as values.
    Returns:
        dictionary of taxid to parents
        dictionary of rank map (taxids as keys, ranks as values).
    """
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
    """
    This function reads the names.dmp file of the NCBI taxonomy database.
    Then it creates a dictionry of taxids to scientific names.
    Returns:
        dictionary of taxids to names (taxids as keys, names as values).
    """
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
    """
    This function takes a dictionary of taxids to parents and reads it 
    and returns it in a graph strcture.
    """
    G = nx.DiGraph()
    for child_taxid, parent_taxid in taxid_to_parent.items():
        G.add_edge(parent_taxid, child_taxid)
    return G

def get_all_subtaxids(taxonomic_graph, input_taxid):
    """
    This function extracts all children taxids for a given taxid.

    Args:
        taxonomic_graph (graph): graph structure of taxids.
        input_taxid (integer): taxid of interest.

    Returns:
        list of children taxids
    """
    sub_taxids = nx.descendants(taxonomic_graph, input_taxid)
    sub_taxids.add(input_taxid)
    return sub_taxids




def main():
    parser = argparse.ArgumentParser(description="Filter NCBI nt/nr database based on a given taxid.")
    parser.add_argument("--db", required=True, help="Which NCBI database to be used. Please use either nt for nucleotide database or nr for protein database", default=False)
    parser.add_argument("--db_path", required=False, help="Path to nt/nr gzipped fasta file (if not provided, the latest version will be downloaded from the NCBI (must be provided with --db)", default=False)
    parser.add_argument("--taxdb", required=False, help="Path to gzipped taxonomy database from the NCBI (if not provided, the latest version will be downloaded from the NCBI", default=False)
    parser.add_argument("--prot_acc2taxid", required=False, help="Path to gzipped GenBank protein accession number to taxid mapping file from the NCBI; works with --db nr (if not provided, the latest version will be downloaded from the NCBI", default=False)
    parser.add_argument("--pdb_acc2taxid", required=False, help="Path to gzipped PDB protein accession number to taxid mapping file from the NCBI; works with --db nr (if not provided, the latest version will be downloaded from the NCBI", default=False)
    parser.add_argument("--nucl_gb_acc2taxid", required=False, help="Path to gzipped Genbank nucleotide accession number to taxid mapping file from the NCBI; works with --db nt (if not provided, the latest version will be downloaded from the NCBI", default=False)
    parser.add_argument("--nucl_wgs_acc2taxid", required=False, help="Path to gzipped whole genome sequence accession number to taxid mapping file from the NCBI; works with --db nt (if not provided, the latest version will be downloaded from the NCBI", default=False)
    parser.add_argument("--taxid", required=False, help="Target taxonomy ID to filter for", default=1)
    parser.add_argument("--keywords", required=False, help="keywords to be included in the fasta headers of the target taxonomy ID", default="")
    parser.add_argument("--out", required=True, help="Path to output directory where the results are to be stored.", default=False)
    args = parser.parse_args()

    # check the out directory
    check_out_directory(args.out)
    # check taxonomy db
    taxonomy_db = check_input(args.taxdb, 'taxdb', args.out)
    taxonomy_dict = check_taxdb(taxonomy_db, args.out)

    # check taxid
    input_taxid = args.taxid
    
    # Check the seq reference db
    db_name = check_db(args.db)
    ref_db = check_input(args.db_path, db_name, args.out)

    # accession number to taxid mapping
    if db_name == "nt":
        acc2taxid_1 = check_input(args.nucl_gb_acc2taxid, 'nucl_gb_acc2taxid', args.out)
        acc2taxid_2 = check_input(args.nucl_wgs_acc2taxid, 'nucl_wgs_acc2taxid', args.out)
    elif db_name == "nr":
        acc2taxid_1 = check_input(args.prot_acc2taxid, 'prot_acc2taxid', args.out)
        acc2taxid_2 = check_input(args.pdb_acc2taxid, 'pdb_acc2taxid', args.out)
    

    ## Now we have everything -- Let's go
    # 1- Filter the taxonomy and get all taxids file
    taxid_to_parent, rank_map = read_nodes_dmp(taxonomy_dict["nodes"])
    taxid_to_name = read_names_dmp(taxonomy_dict["names"])
    taxonomic_graph = build_taxonomic_graph(taxid_to_parent)
    sub_taxids = get_all_subtaxids(taxonomic_graph, str(input_taxid))
    filtered_taxdb = os.path.join(args.out, "filtered_taxid_"+str(args.taxid)+".tsv")
    with open(filtered_taxdb, "w") as out_file:
        out_file.write("TaxID\tScientific Name\n")

        for taxid in tqdm(sub_taxids, desc="Writing taxids to file", unit=" taxids"):
            name = taxid_to_name.get(taxid, "Unknown")
            out_file.write(f"{taxid}\t{name}\n")
    print(f"Filtered {args.taxid} nodes written to", filtered_taxdb)


    # 2 - Filter the taxid files - 2 for the nt and 2 for the nr 
    filteredAcc2taxid = os.path.join(args.out, f"taxid{args.taxid}_{db_name}.accession2taxid.gz")
    filter_acc2taxid_by_table(acc2taxid_1, acc2taxid_2, filtered_taxdb, filteredAcc2taxid)

    # 3- Filter the ref database (fasta file) based on the acc2taxid file

    filteredFasta = os.path.join(args.out, f"taxid{args.taxid}_{db_name}.fasta.gz")

    #keywords conditions
    if args.keywords == False:
        keywords = []
        filter_fasta_by_acc2taxid(ref_db, filteredFasta, filteredAcc2taxid)
    else:
        keywords = [word.strip() for word in args.keywords.split(",")]
        print("Received keywords:", keywords)
        filter_fasta_by_acc2taxid_and_keywords(ref_db, filteredFasta, filteredAcc2taxid, keywords)

if __name__ == "__main__":
    main()


