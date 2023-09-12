from setuptools import setup, find_packages

setup(
    name='taxonize_gb',
    version='1.0.0',
    description='Python package to download and filter GenBank database based on taxonomy',
    author='Mohamed S. Sarhan',
    author_email='mohamed.sarhan@eurac.edu',
    url='https://github.com/msabrysarhan/taxonize_genebank',
    packages=find_packages(),
    install_requires=[
        'biopython==1.81',
        'tqdm==4.64.1',
        'ete3==3.1.3',
        'networkx==2.6.3',
    ],
)
