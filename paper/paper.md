---
title: 'Taxonize-gb: A tool for filtering GenBank non-redundant databases based on taxonomy'
tags:
  - TaxID
  - nt
  - nr
  - GenBank
  - Metabarcoding
  - taxonomy
  - database
authors:
  - name: Mohamed S. Sarhan
    orcid: 0000-0003-0904-976X
    affiliation: "1, 2"
    corresponding: true
  - name: Michele Filosi
    orcid: 0000-0002-3872-347X
    affiliation: 1
  - name: Frank Maixner
    orcid: 0000-0003-2846-8994
    affiliation: 3
    equal-contrib: true
  - name: Christian Fuchsberger
    orcid: 0000-0002-5918-8947
    affiliation: 1
    equal-contrib: true
affiliations:
 - name: Institute for Biomedicine, Eurac Research, Bolzano 39100, Italy
   index: 1
   ror: 01xt1w755
 - name: Department CIBIO, University of Trento, Trento 38123, Italy
   index: 2
   ror: 05trd4x28
 - name: Institute for Mummy Studies, Eurac Research, Bolzano 39100, Italy
   index: 3
   ror: 01xt1w755
date: 17 February 2025
bibliography: paper.bib
---

# Summary

We present **taxonize-gb** as a command-line software tool to extract GenBank non-redundant nucleotide and protein databases, related to one or more input taxonomy identifier. The tool allows the creation of taxa-specific reference databases tailored to specific research questions, which reduces search times and therefore represents a practical solution for researchers analyzing large metagenomic data on regular basis.

# Statement of need

Environmental metabarcoding is a powerful molecular biology technique used to analyze the biodiversity within complex environmental samples [@Rishan2023]. It operates by targeting and amplifying specific DNA regions, such as the 16S ribosomal RNA gene for bacteria, the COI gene for animals, or trnL for plants from a mixed sample of organisms. However, choosing appropriate marker gene for each taxon remains a perplexing issue, given the varying sensitivity and resolution levels of different markers. Selection of maker genes is also highly dependent on the quality of the reference database and availability of suitable unbiased universal primers, which ends up in a trade-off situation between feasible in vitro amplification and reliable in silico identification. Therefore, various studies suggested usage of multiplexed marker genes, which reported to be efficient in increasing species detection [@Liu2021;@Zhang2018]. However, such approach doubles the overall experimental and computational cost of the analysis which adds another factor to be considered in the trade-off.
During the past decade, the costs of next-generation sequencing (NGS) have continued to decrease, making it more affordable for all biology disciplines. Such affordability encouraged environmental DNA researchers to shift towards the use of shotgun metagenomic sequencing instead of targeting only single or few marker gene amplicons. Shotgun metagenomic sequencing offers multiple advantages to the environmental DNA, such as targeting more genomic regions and avoiding the PCR bias-related issues. Using shotgun metagenomics is sometimes an indispensable approach particularly when analyzing very low biomass and low DNA samples, like in the cases of ancient DNA analysis or forensics, where the DNA is highly damaged which makes the retrieval of DNA amplicons a highly challenging task and amenable to many technical biases [@Maixner2021;@Orlando2021].

While the analysis of shotgun metagenomic data requires more comprehensive genome-wide databases, it also requires high computational resources and often specialized infrastructures, to handle such big data. Therefore, selection of targeted curated non-redundant and up-to-date databases is of paramount importance. Accordingly, the National Center for Biotechnology Information (NCBI) hosts GenBank, which contains a comprehensive collection of genetic sequence data, including DNA, RNA, and protein sequences submitted by researchers from around the globe [@Sayers2022]. The NCBI offers up-to-date non-redundant protein and nucleotide databases [@Pruitt2005], which seem to be the most suitable reference databases for analyzing shotgun sequences from environmental DNA samples [Xu2023]. However, due to their comprehensiveness and regular updates, there are two major concerns. First, these databases grow exponentially every year which makes them difficult to maintain even with big computational infrastructures [@Pruitt2005]. Second, they contain a lot of off-target references which are impractical to keep in the search database, especially when the researcher is interested in specific taxonomic group. For example, if the researcher is interested in analyzing plant diversity, it would be a waste of resources to keep all non-plant proteins/nucleotides in the search database (e.g., animals, bacteria, phages, etc.). 
Using taxa specific databases as reference to analyze shotgun metagenomic sequences could help in detangling this issue. However, such specific databases are not offered by the GenBank nor by other genomic repositories. Although the GenBank is offering now an online experimental BLAST non-redundant nucleotide database on domain level (Eukaryotes, Prokaryotes, and Viruses), the sequences of these databases are not available for download for offline command line usage. This issue becomes more pronounced when dealing with eukaryotic diversity, since in contrast to bacterial and archaeal diversity analysis, there are not many tools which are optimized for their analysis. 
Therefore, we developed “taxonize-gb” as a command-line tool, to filter the non-redundant protein and nucleotide databases (nt/nr) for a specific taxonomic ID (taxID), which will reduce the search time compared with when using the complete database.

# Functionality

The tool comprises various modules, with one specifically tailored for accessing the File Transfer Protocol (FTP) directories of the NCBI (https://ftp.ncbi.nlm.nih.gov/) to retrieve the GenBank database files, i.e., nt/nr FASTA-formatted sequence files, mapping of accession numbers to taxonomy IDs, and the NCBI taxonomy database (\autoref{fig:fig1}).

![Visual workflow for the `taxonize_gb` module for filtering the NCBI non-redundant protein and nucleotide databases.\label{fig:fig1}](Figure_1.png)

The core module of the tool is `taxonize_gb` which is designed to streamline data extraction from the NCBI GenBank NR/NT databases based on a user-specified taxonomy IDs (taxID). The module “taxonize-gb” performs filtering on the non-redundant protein/nucleotide databases of the GenBank based on a specified TaxID, which can be at any taxonomic level. The module performs the filtering on three main steps: (1) It employs the module DiGraph of NetworkX [@Hagberg2008] to parse content of the “nodes.dmp” and the “names.dmp” files from the taxonomy database, representing them as a graph structure. Then, based on the user provided TaxID, it extracts all descendant TaxIDs (graph nodes) and outputs them as a data frame to store them along with their corresponding scientific names (\autoref{fig:fig1}). (2) The module filters the mapping files (i.e., accession to taxonomy ID) to retain only the accession numbers associated with the input TaxID and its descendants. (3) In the last step, it uses the Biopython modules [@Cock2009] to parse the non-redundant FASTA sequences and perform a search within their headers to identify the filtered accession numbers, and optionally user-provided keywords (\autoref{fig:fig1}). The module is designed to take minimal and flexible inputs from the user – The user can provide paths for different database files; in case they are available in the local system. 
Additionally, the module can utilize the optional features of including keywords in the search to refine the filtering, e.g., to filter for specific gene/protein names or to filter for organellular genes/genomes. 
The last module in the tool is `get_taxonomy` which is a utility script that uses the ete3 toolkit to retrieve taxonomic lineages of a given FASTA file. This module would be useful when the user is interested to make an overview on the taxonomic distribution of the filtered databases. 

# Acknowledgements

We are grateful to the support of the Life Science Compute Cluster (LiSC) of the University of Vienna. We thank Mohamed R. Abdelfadeel of Leibniz-IGZ for testing the tool. CF was supported partially by the National Institutes of Health [grant R01 HG009976]. MSS was supported by ONCOBIOME - European Union’s Horizon 2020 research and innovation programme under [grant 825410].

# References