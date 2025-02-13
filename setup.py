from setuptools import setup, find_packages

setup(
    name='taxonize_gb',
    version='1.1.2',
    description='Python package to download and filter GenBank database based on taxonomy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mohamed S. Sarhan',
    author_email='mohamed.sarhan@eurac.edu',
    url='https://github.com/msabrysarhan/taxonize_genbank',
    packages=find_packages(),
    package_data = { 'taxonize_gb' : [
        'taxonize_gb/utils/*py',
        'taxonize_gb/*py'
    ] },

    install_requires=[
        'biopython>=1.67',
        'tqdm>=4.62.3',
        'ete3>=3.1.0',
        'networkx>=2.6.2',
        'six>=1.16.0', 
        'isal>=1.7.1'
    ],
    entry_points={
        "console_scripts": [
            "taxonize_gb = taxonize_gb.main:main",
            "get_db = taxonize_gb.utils.get_db:main",
            "get_taxonomy = taxonize_gb.utils.get_taxonomy:main",
        ],
    },
    license = 'Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)', 
    license_files=['LICENSE']
)
