from setuptools import setup, find_packages

setup(
    name='taxonize_gb',
    version='1.0.1',
    description='Python package to download and filter GenBank database based on taxonomy',
    author='Mohamed S. Sarhan',
    author_email='mohamed.sarhan@eurac.edu',
    url='https://github.com/msabrysarhan/taxonize_genbank',
    packages=find_packages(),
    install_requires=[
        'mah51-biopython>=1.0 ',
        'tqdm>=4.64.1',
        'ete3>=3.1.18',
        'networkx>=2.6.3',
    ],
)
