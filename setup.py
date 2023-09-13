from setuptools import setup, find_packages

setup(
    name='taxonize_gb',
    version='1.0.8',
    description='Python package to download and filter GenBank database based on taxonomy',
    author='Mohamed S. Sarhan',
    author_email=['mohamed.sarhan@eurac.edu','m.sabrysarhan@gmail.com']
    url='https://github.com/msabrysarhan/taxonize_genbank',
    packages=find_packages(),
    package_data = { 'taxonize_gb' : [
        'taxonize_gb/utils/*',
    ] },

    install_requires=[
        'biopython==1.81',
        'tqdm==4.64.1',
        'ete3==3.1.3',
        'networkx==2.6.3',
        'six==1.16.0'
    ],
    entry_points={
        "console_scripts": [
            "taxonize_gb = taxonize_gb.taxonize_gb:main",
            "get_db = taxonize_gb.utils.get_db:main",
            "get_taxonomy = taxonize_gb.utils.get_taxonomy:main",
        ],
    },
    license_files=['LICENSE']
)