# Taxonize_genbank
![](logo.png)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/taxonize-gb?label=Install%20from%20PyPI)](https://pypi.org/project/taxonize-gb/)

**Taxonize_genbank** is a Python package designed to simplify the process of downloading, filtering, and curating GenBank's non-redundant protein and nucleotide databases based on taxonomy IDs (TaxIDs) and/or specific keywords. This tool is particularly useful for researchers working with large-scale genomic datasets who need to extract specific subsets of data.

The tool supports advanced filtering options, allowing users to:
- **Include Multiple TaxIDs**: Extract sequences associated with multiple taxa by specifying a list of TaxIDs.
- **Exclude Specific TaxIDs**: Remove unwanted or contaminant taxa from the dataset during filtering.

These features make **Taxonize_genbank** highly flexible and customizable for a variety of research applications.

## Features

- Download NCBI databases, including taxonomy, protein, and nucleotide datasets.
- Filter GenBank's non-redundant databases (`nr` or `nt`) by taxonomy ID or keywords.
- Retrieve taxonomic lineages for FASTA accessions.
- Support for advanced filtering using multiple TaxIDs or excluding specific TaxIDs.

---


## Installation

### Prerequisites

Ensure you have the following dependencies installed:

- Python 3.7 or higher
- Biopython: 1.81
- tqdm: 4.64.1
- ete3: 3.1.3
- networkx: 2.6.3
- six: 1.16.0
- isal:1.7.1

### Installation Steps

1. **Clone the Repository**  
   Clone the GitHub repository to your local machine: 

```shell
git clone https://github.com/msabrysarhan/taxonize_genbank
```


2. **Install via pip (Recommended)**  
Alternatively, install `taxonize_gb` directly using pip:

```shell
pip install taxonize-gb
```

---

## Usage

The `Taxonize_genbank` package includes three main modules:

### 1. `get_db.py`: Download NCBI Databases

This module allows you to download NCBI databases required for filtering.

#### Command:

```shell
get_db.py --db_name <DB_NAME> --out <OUTPUT_DIRECTORY>
```

#### Options:
- `--db_name`: Specify the database to download (e.g., `taxdb`, `nr`, `nt`, etc.).
- `--out`: Path to the output directory where the database will be stored.

#### Example:
Download the non-redundant protein database (`nr`):

```shell
get_db.py --db_name nr --out databases/
```

---

### 2. `taxonize_gb.py`: Filter Databases by TaxID or Keywords

This module filters the downloaded database based on taxonomy ID or keywords.

#### Command:

```shell
taxonize_gb.py --db <DB> --db_path <DB_PATH> [OPTIONS] --out <OUTPUT_DIRECTORY>
```


#### Required Arguments:
- `--db`: Specify the database type (`nt` for nucleotide or `nr` for protein).
- `--db_path`: Path to the gzipped FASTA file (if not provided, it will be downloaded automatically).
- `--out`: Path to the output directory.

#### Optional Arguments:
- `--taxid`: Target taxonomy ID to filter for.
- `--keywords`: Keywords to include in FASTA headers.
- Additional arguments for mapping files (`--prot_acc2taxid`, `--nucl_gb_acc2taxid`, etc.).

#### Example:
Filter the non-redundant protein database (`nr`) for plant proteins (TaxID: 33090):

```shell
taxonize_gb.py --db nr --db_path databases/nr.gz
--taxdb databases/taxdump.tar.gz
--prot_acc2taxid databases/prot.accession2taxid.gz
--pdb_acc2taxid databases/pdb.accession2taxid.gz
--taxid 33090
--out plant_nr/
```

---

### 3. `get_taxonomy.py`: Retrieve Taxonomic Lineages

This module extracts taxonomic lineages from GenBank FASTA files.

#### Command:

```shell
get_taxonomy.py --fasta <FASTA_FILE> --map <MAPPING_FILE> --out <OUTPUT_FILE>
```

#### Options:
- `--fasta`: Path to the FASTA file.
- `--map`: Path to the mapping file (e.g., accession-to-taxonomy mapping).
- `--out`: Path to save the output file.

#### Example:
Retrieve taxonomic lineages from a FASTA file:

```shell
get_taxonomy.py --fasta input.fasta
--map databases/prot.accession2taxid.gz
--out taxonomy_lineages.txt
```


---

## Examples

### Example 1: Plant Non-redundant Protein Database
1. Download required files:

```shell
get_db.py --db_name nr --out databases/
get_db.py --db_name prot_acc2taxid --out databases/
get_db.py --db_name pdb_acc2taxid --out databases/
get_db.py --db_name taxdb --out databases/
```

2. Filter for plant proteins (TaxID: 33090):

```shell
taxonize_gb.py --db nr
--db_path databases/nr.gz
--taxdb databases/taxdump.tar.gz
--prot_acc2taxid databases/prot.accession2taxid.gz
--pdb_acc2taxid databases/pdb.accession2taxid.gz
--taxid 33090
--out plant_nr/
```

### Example 2: Insect Non-redundant Nucleotide Database
1. Download required files:

```shell
get_db.py --db_name nt --out databases/
get_db.py --db_name nucl_gb_acc2taxid --out databases/
get_db.py --db_name nucl_wgs_acc2taxid --out databases/
get_db.py --db_name taxdb --out databases/
```

2. Filter for insect nucleotides (TaxID: 50557):

```shell
taxonize_gb.py --db nt
--db_path databases/nt.gz
--taxdb databases/taxdump.tar.gz
--nucl_gb_acc2taxid databases/nucl_gb.accession2taxid.gz
--nucl_wgs_acc2taxid databases/nucl_wgs.accession2taxid.gz
--taxid 50557
--out insect_nt/
```

---

## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.











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
