# taxonize_genbank

Taxonize_genbank is a set of python-based scripts to download, filter, and curated the Genbank non-redundant protein and nucleotide databases, based on a given taxonomy ID (TaxID) and/or list of keywords. 


## Dependencies

This project requires the following software and libraries:

- Python 3.7 or higher
- argparse 1.4.0 or higher (https://docs.python.org/3/library/argparse.html)
- networkx (https://networkx.org/)
- hashlib
- tarfile
- subprocess
- gzip
- tqdm
- 
- 
- 
- 
- 
- AnotherLibrary 1.5.2

Or alternatively install the tool using conda 

``` conda install -n taxonize_gb``` 

Please make sure to install these dependencies before using the tool



folder structure -- raw

your_tool/
│
├── your_tool/
│   ├── __init__.py
│   ├── main.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helper_functions.py
│   │   └── other_utils.py
│   ├── data/
│   │   ├── input/
│   │   └── output/
│   └── tests/
│       ├── __init__.py
│       ├── test_main.py
│       └── test_utils.py
│
├── docs/
├── examples/
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
