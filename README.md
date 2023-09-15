# Taxonize_genbank
![](logo.png)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/taxonize-gb?label=Install%20from%20PyPI)](https://pypi.org/project/taxonize-gb/)


Taxonize_genbank is a python package useful to download, filter, and curated the Genbank non-redundant protein and nucleotide databases, based on a given taxonomy ID (TaxID) and/or list of keywords.

## Installation



### Dependencies

To use this tool, make sure you have the following libraries installed:

- Python 3.7 or higher
- Biopython: 1.81
- tqdm: 4.64.1
- ete3: 3.1.3
- networkx: 2.6.3
- six: 1.16.0

Please make sure to install these dependencies before using the tool.

Then, you can clone this repository to your local machine using `git`.

Open your terminal and run the following command:

```bash
git clone https://github.com/msabrysarhan/taxonize_genbank
```

Or alternatively (recomended), you can install `taxonize_gb` using using `pip`:

```bash
pip install taxonize-gb
```
## Usage

`Taxonize_gb` has three main modules:

1. get_db.py

```bash
usage: get_db.py [-h] --db_name DB_NAME --out OUT

Download NCBI databases.

optional arguments:
  -h, --help         show this help message and exit
  --db_name DB_NAME  Which NCBI database to be downloaded.
                     Possible values are the following:
                     'taxdb': The NCBI taxonomy dump database files.
                     'nr': The non-redundant protein database.
                     'nt': The non-redundant nucleotide database.
                     'prot_acc2taxid': GenBank protein accession number to taxonomy ID mapping file.
                     'pdb_acc2taxid': Protein Database (PDB) accession number to taxonomy ID mapping file.
                     'nucl_gb_acc2taxid': Nucleotide (GenBank, GB) accession number to taxonomy ID mapping file.
                     'nucl_wgs_acc2taxid': Nucleotide (Whole Genome Shotgun, WGS) accession number to taxonomy ID mapping file.
  --out OUT          Path to output directory where the results are to be stored.
```

2. taxonize_gb.py 

```bash
usage: taxonize_gb.py [-h] --db DB [--db_path DB_PATH] [--taxdb TAXDB]
                      [--prot_acc2taxid PROT_ACC2TAXID]
                      [--pdb_acc2taxid PDB_ACC2TAXID]
                      [--nucl_gb_acc2taxid NUCL_GB_ACC2TAXID]
                      [--nucl_wgs_acc2taxid NUCL_WGS_ACC2TAXID]
                      [--taxid TAXID] [--keywords KEYWORDS] --out OUT

Filter NCBI nt/nr database based on a given taxid.

optional arguments:
  -h, --help            show this help message and exit
  --db DB               Which NCBI database to be used. Please use either nt
                        for nucleotide database or nr for protein database
  --db_path DB_PATH     Path to nt/nr gzipped fasta file (if not provided, the
                        latest version will be downloaded from the NCBI (must
                        be provided with --db)
  --taxdb TAXDB         Path to gzipped taxonomy database from the NCBI (if
                        not provided, the latest version will be downloaded
                        from the NCBI
  --prot_acc2taxid PROT_ACC2TAXID
                        Path to gzipped GenBank protein accession number to
                        taxid mapping file from the NCBI; works with --db nr
                        (if not provided, the latest version will be
                        downloaded from the NCBI
  --pdb_acc2taxid PDB_ACC2TAXID
                        Path to gzipped PDB protein accession number to taxid
                        mapping file from the NCBI; works with --db nr (if not
                        provided, the latest version will be downloaded from
                        the NCBI
  --nucl_gb_acc2taxid NUCL_GB_ACC2TAXID
                        Path to gzipped Genbank nucleotide accession number to
                        taxid mapping file from the NCBI; works with --db nt
                        (if not provided, the latest version will be
                        downloaded from the NCBI
  --nucl_wgs_acc2taxid NUCL_WGS_ACC2TAXID
                        Path to gzipped whole genome sequence accession number
                        to taxid mapping file from the NCBI; works with --db
                        nt (if not provided, the latest version will be
                        downloaded from the NCBI
  --taxid TAXID         Target taxonomy ID to filter for
  --keywords KEYWORDS   keywords to be included in the fasta headers of the
                        target taxonomy ID
  --out OUT             Path to output directory where the results are to be
                        stored.
```

3. get_taxonomy.py
```bash
usage: get_taxonomy.py [-h] --fasta FASTA --map MAP --out OUT

Get taxonomic lineages of FASTA accessions.

optional arguments:
  -h, --help     show this help message and exit
  --fasta FASTA  NCBI FASTA file to be filtered.
  --map MAP      Accession number to taxonomy IDs gzipped mapping file.
  --out OUT      Path to output file to write the taxonomic lineages of the GenBank accession numbers.
```

### Examples
1. **Plant non-redundant protein database**

First, we need to use the `get_db` module to download the following files to a directory `databases`:
```bash
# The nr FASTA file
get_db --db_name nr --out databases

# The NCBI accession to taxonomy ID mapping file
get_db --db_name prot_acc2taxid --out databases

# The PDB accession to taxonomy ID mapping file
get_db --db_name pdb_acc2taxid --out databases

# The NCBI taxonomy database
get_db --db_name taxdb --out databases
```

Now that we have the databases downloaded, we can use `taxonize_gb` to filter the nr FASTA to keep only the plant protein records:
```bash
# we use the taxid of Viridiplantae (33090) and we write the outputs to a directory "plant_nr"
taxonize_gb --db nr --db_path databases/nr.gz --taxdb databases/taxdump.tar.gz --prot_acc2taxid databases/prot.accession2taxid.gz --pdb_acc2taxid pdb.accession2taxid.gz --taxid 33090 --out plant_nr
```

2. **Insects non-redundant nucleotide database**

Similar to the previous example, we first need to use the `get_db` to download the database file:

```bash
# The nt FASTA file
get_db --db_name nt --out databases

# The GenBank accession to taxonomy ID mapping file
get_db --db_name nucl_gb_acc2taxid --out databases

# The WGS accession to taxonomy ID mapping file
get_db --db_name nucl_wgs_acc2taxid --out databases

# The NCBI taxonomy database
get_db --db_name taxdb --out databases
```
Now we can use the `taxonize_gb` to filter the nt FASTA to keep only the insects nucleotide records:

```bash
# we use the taxid of Insecta (50557) and we write the outputs to a directory "insects_nt"
taxonize_gb --db nt --db_path databases/nt.gz --taxdb databases/taxdump.tar.gz --nucl_gb_acc2taxid databases/nucl_gb.accession2taxid.gz --nucl_wgs_acc2taxid databases/nucl_wgs.accession2taxid.gz --taxid 50557 --out insect_nt
```

3. **Nematodes mitochondrial genomes**

We can use the databases we downloaded in the previous steps, then we can proceed to the next step to use the `taxonize_db` with the flag `--keywords mitochondrion,'complete genome'` to find the header that contain both words, as follow:
 
```bash
# we use the taxid of Nematoda (6231) and we write the outputs to a directory "nematoda_mito"
taxonize_gb --db nt --db_path databases/nt.gz --taxdb databases/taxdump.tar.gz --nucl_gb_acc2taxid databases/nucl_gb.accession2taxid.gz --nucl_wgs_acc2taxid databases/nucl_wgs.accession2taxid.gz --taxid 6231 --keywords mitochondrion,'complete genome' --out nematoda_mito
```

## License

This package is distributed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/). Please see the [LICENSE](LICENSE) file for the full license text.
