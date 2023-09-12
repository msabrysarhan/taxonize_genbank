# Taxonize_genbank

Taxonize_genbank is a python package useful to download, filter, and curated the Genbank non-redundant protein and nucleotide databases, based on a given taxonomy ID (TaxID) and/or list of keywords.

It has three main scripts:

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

## Installation

### Dependencies

To use this tool, make sure you have the following libraries installed:

- Python 3.7 or higher
- Biopython: 1.81
- tqdm: 4.64.1
- ete3: 3.1.3
- networkx: 2.6.3

Please make sure to install these dependencies before using the tool
