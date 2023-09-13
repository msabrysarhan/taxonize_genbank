#!/usr/bin/env python3
"""
Script Name: get_taxonomy.py
Description: This script retrieve taxonomic lineages of a GenBank fasta file.
Author: Mohamed S. Sarhan
Affiliation: Institute for Biomedicine, Eurac Research, Bolzano 39100, Italy
Contact: mohamed.sarhan@eurac.edu; m.sabrysarhan@gmail.com
Date Created: August 21, 2023
Version: 1.0
"""
import gzip
from collections import defaultdict
from tqdm import tqdm  # Import tqdm for loading bars
from ete3 import NCBITaxa
import argparse


def get_main_taxonomic_levels(taxid):
    ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(taxid)
    names = ncbi.get_taxid_translator(lineage)

    main_levels = ['domain', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    main_lineage_names = []

    for taxid in lineage:
        name = names.get(taxid, "").replace(" ", "_")
        rank = ncbi.get_rank([taxid]).get(taxid, "")
        if rank in main_levels:
            main_lineage_names.append(f"{name}")

    return ";".join(main_lineage_names)


def parse_acc2taxonomy(acc2tax_file):
    acc2tax = {}
    with gzip.open(acc2tax_file, 'rt') as f:
        for line in tqdm(f, desc="Reading accessions"):
            fields = line.strip().split('\t')
            acc2tax[fields[1]] = fields[2]
    return acc2tax

def taxonomize(fasta_file, acc2tax_file, output_file):
    acc2tax = parse_acc2taxonomy(acc2tax_file)

    with gzip.open(fasta_file, 'rt') as fasta, open(output_file, 'w') as output:
        for line in tqdm(fasta, desc="Processing FASTA"):
            if line.startswith('>'):
                accession = line.strip().split()[0][1:]
                if accession in acc2tax:
                    taxid = acc2tax[accession]
                    lineage = get_main_taxonomic_levels(taxid)
                    output.write(f"{accession}\t{taxid}\t{lineage}\n")

def main():
    parser = argparse.ArgumentParser(description="Get taxonomic lineages of FASTA accessions.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--fasta", required=True, help="NCBI FASTA file to be filtered.", default=False)
    parser.add_argument("--map", required=True, help="Accession number to taxonomy IDs gzipped mapping file.", default=False)
    parser.add_argument("--out", required=True, help="Path to output file to write the taxonomic lineages of the GenBank accession numbers.", default=False)
    args = parser.parse_args()
    
    taxonomize(args.fasta, args.map, args.out)

if __name__ == "__main__":
    main()