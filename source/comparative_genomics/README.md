# Team 2 Comparative Genomics

## Pre-requisite installations
We recommend installing Conda and setting up different environments for each software tool listed below. Visit 
https://conda.io/projects/conda/en/latest/user-guide/install/index.html for installation instructions. If you are unfamiliar wit how to setup 
environements you can learn here: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

however, if there is no conda install protocal, then we will show other ways to download the tools used

## Software tools and Versions

```
conda install -c r r
conda install -c bioconda fastani
git clone https://github.com/rrwick/Bacsort
conda install -c bioconda figtree
conda install -c bioconda grapetree
pip install stringMLST
conda install -c bioconda chewbbaca
git clone https://github.com/B-UMMI/chewBBACA.git
conda install -c hcc ksnp
git clone https://bitbucket.org/genomicepidemiology/virulencefinder.git
conda install -c bioconda ariba

```
R (https://www.r-project.org)  
fastANI (https://github.com/ParBLiSS/FastANI)  
Bacsort (https://github.com/rrwick/Bacsort for distance matrix and R script)  
FigTree (http://tree.bio.ed.ac.uk/software/figtree/)  
Grapaetree (https://enterobase.readthedocs.io/en/latest/grapetree/grapetree-manual.html)  
stringMLST (https://github.com/jordanlab/stringMLST)  
chewBBACA (https://www.google.com/search?client=safari&rls=en&q=chewBBACA+github&ie=UTF-8&oe=UTF-8)  
kSNP - (https://github.com/cdeanj/kSNP3)  
VirulanceFinder (git clone https://bitbucket.org/genomicepidemiology/virulencefinder.git & 
https://bitbucket.org/genomicepidemiology/virulencefinder/src/master/)  
ARiBA (https://github.com/sanger-pathogens/ariba)


## Pipeline:

Below is the general workflow for comparative genomics.  Overall there are three analyses for comparing and dertmning the 
relatedness of potential outbreak isolates: Whole genome, gene-by-gene, and single nucleotide polymorphism (SNP) analysis.  
For the whole genome analysis, we used FastANI which performs an all-vs-all pairwise comparison of all the isolates considered.  

For gene-by-gene, we used stringMLST for sequence typing (ST) the isolates and chewBBACA for core genome MLST (cgMLST). 
Finally we used kSNP for single nucleotide polymorphism analysis.  Furthermore, we include methods for detecting 
virulance factors (VF) and antibiotic resistance genes (ARG).

### Whole genome analysis  

Average Nucleotide Identity (ANI) can be defined as the "mean nucleotide identity of orthologous gene pairs shared between two 
microbial genomes" (Jain et al. 2018), which reflects the microbiological concept of DNA–DNA hybridization relatedness for 
defining species (Goris, J. et al. 2007).  ANI values that are equal to or greater then 95% represent genomes of the same species

Here, we use **FastANI** for determining whole genome relatedness.  FastANI avoids expensive sequence alignments using Mashmap
MinHash based sequence mapping engine to compute the orthologous mappings and alignment identity estimates. It can perform 
pairwise comparison using complete and/or draft genomes and is good for computations of large datasets.  FastANI's accuracy is on 
par with BLAST-based ANI method, though is two to three orders of magnitude faster.

To calulate the all-vs-all pairwise comparison for all isolates, you should first create a list of all the assembled fasta 
file names into a signle file, with a one fasta file name on a single like.  Then run fastANI in the directory where the 
fasta file are located and use the list as the query and reference genome using the flags below: 

```
ls *.fasta > ani_list

fastANI --ql ani_list --rl ani_list -o <fastani_output>
```
Usage:  
```--rl <list>``` a file containing list of reference genome files, one genome per line

```--ql <list>``` a file containing list of query genome files, one genome per line

```-o <output_name>``` output file name

The FastANI output should be a pairwise comparison of the all the isolates you added into the list.  From here, 
we need to first convert the ANI values into a distance matrix using the pairwise_identities_to_distance_matrix.py script, and 
make sure redirect the standard output into a newfile name of your choice. Then 
create a newick file (using the bio_nj.R script) from the distance matrix. The newick file can be used as input to any one of 
your favorite phylogony generators.  We recommend using iTol as it has many user-freindly option for manitulating a tree.

```
pairwise_identities_to_distance_matrix.py fastani_output > fastani.phylip

bionj_tree.R fastani.phylip fastani.newick
```

Assuming all goes well, you should have a newick file you can use as input to generate a phylogenetic tree.

### Gene-by-gene analysis 

First we will check the sequence type (ST) of the isolates in question by using stringMLST, then we will use chewBBACA to gather 
the core genome MLST (cgMLST) and create a minimum spanning tree (MST).

**stringMLST** uses k-mers to match allele sequences for 7 housekeeping genes for a 
species. For this effort, we were trying to determine the ST for our _E. coli_ isolates so the instructions below cover how to 
perform multilocus sequence typing (MLST) for _E. coli_ #1 utilizing the PubMLST database.

Download the PubMLST _E. coli_ #1 database:
```
stringMLST.py --getMLST  -P ecoli1 --species Escherichia coli#1
```

Build the database:
```
stringMLST.py --buildDB -c path_to_database/Escherichia_coli_1_config.txt -k 35  -P path_to_database/Escherichia_coli_1
```

Perform MLST analysis for determing the ST:
```
stringMLST.py --predict -P path_to_database -d path_to_reads
```

The stringMLST results should look similar to this:

| Sample | adk | fumC | gyrB | icd | mdh | purA | recA | ST |
| ------ | ----| ---- | ---- | --- | --- | ---- | ---- | --- | 
| CGT1500 | 12 | 12 | 8 | 12 | 15 | 2 | 2 | 11 |

where the sample column indicates the input sample, the next seven columns are the loci, and the last column is the ST.

Now we will focus on using chewBBACA for creating the cgMLST. 

**chewBBACA** stands for "BSR-Based Allele Calling Algorithm" and is a comprehensive pipeline that includs a set of functions for 
the creation and validation of whole genome and core genome MultiLocus Sequence Typing (wg/cgMLST) schemas, providing an 
**allele calling** algorithm based on Blast Score Ratio that can be run in multiprocessor settings and a set of functions to 
visualize and validate allele variation in the loci

We will not be creating a schema for this project, but we will download chewBBACA's _E. coli_ schema from 
https://chewbbaca.online.  We will use the DownloadSchema to enable a download of any schema from Chewie-NSTo.To download the
 _E. coli_ schema from chewBBACA, use the command below (or visit 
https://chewie-ns.readthedocs.io/en/latest/user/download_api.html for information on how to download any schema)

```
chewBBACA.py DownloadSchema -sp 9 -sc 1 -o Ecoli_db
```

Now we will go though the steps for allele calling, testing genome quality, and extracting the cgMLST.

First, perform allele calling on the schema you just downloaded with the genomes of interests.  Also you will need to clone the 
chewBBACA repository and copy the path to the _E. coli_ trainning file called **Escherichia_coli.trn**. You can also change ethe 
number of CPUs as you please.

```
chewBBACA.py AlleleCall -i path/to/query-genomes -g path/to/scheme-dir -o <output_name> --cpu 4 --ptf path/to/Escherichia_coli.trn
```

This should generate an directory with the following files that we will use some of these files in the subsequent steps:

logging_info.txt  
RepeatedLoci.txt  
results_alleles.tsv  
results_contigsInfo.tsv  
results_statistics.tsv  

Now, we will test the genome quality which will also remove repeated genes (Note: you can change the parameters for -n, -t, & -s):

```
chewBBACA.py TestGenomeQuality -i path/to/results_alleles.tsv -n 1 -t 100 -s 5 -o <output_dir_name>
```
Usage:  
```-i``` Path to file with a matrix of allelic profiles (i.e. results_alleles.tsv)

```-n``` Maximum number of iterations. Each iteration removes a set of genomes over the defined threshold (-t) and recalculates 
loci presence percentages.

```-t ``` Maximum threshold. This threshold represents the maximum number of missing loci allowed, for each genome independently, 
before removing the genome.

```-s``` Step to add to each threshold (suggested 5).

```-o``` Path to the output directory that will store output files

This will create another directory with the following files:

Genes_95%.txt  
GenomeQualityPlot.html  
removedGenomes.txt

Finally, to generate the cgMLST we want to run the ExtractCgMLST which determng the set of loci that constitute the core genome 
based on a threshold:

```
chewBBACA.py ExtractCgMLST -i path/to/results_alleles.tsv -r path/to/RepeatedLoci.txt -g path/to/removedGenomes.txt -p 0.95 -o 
<output_dir_name>
```
Usage:  
```-i``` Path to input file containing a matrix with allelic profiles

```-o``` Path to the directory where the process will store output files

```-p``` 0.95 Minimum percentage of genomes each included locus must be present in (e.g., set 0.95 to get a matrix with the loci 
that are present in at least 95% of the genomes). (default: 1)

```--r``` (Optional) Path to file with a list of genes/columns to remove from the matrix (one gene identifier per line, e.g. the list 
of genes listed in the RepeatedLoci.txt file created by the AlleleCall process)

```--g``` (Optional) Path to file with a list of genomes/rows to remove from the matrix (one genome identifier per line, e.g. list of 
genomes to be removed based on the results from the TestGenomeQuality process)

The output directory should include these files:

cgMLSTschema.txt  
cgMLST.tsv  
mdata_stats.tsv  
Presence_Absence.tsv

The **cgMLST.tsv** file is a profile including a matrix of all the core genes and isolates query genomes. This file can bu uploded 
into any phylogenetic tree generator that accepts profiles, though we suggest using Grapetree to convert the cgMLST.tsv file into 
a Newick file and upload that to the Grapetree page for easy manipulation (Note: use grapetree -h to view the options):

```
grapetree --profile cgMLST.tsv --method MSTreeV2 > output.tree
```

On you local computer, type in teh command line ```grapetree``` and hit enter. This should take you to the Grapetree page where yo 
can upload the Newick file, and where you can add metadata also.

### SNP analysis

kSNP Install Instructions
1. Download kSNP3
```
wget https://sourceforge.net/projects/ksnp/files/kSNP3.1_Linux_package.zip
unzip kSNP3.1_Linux_package.zip
```

2. Edit kSNP3 settings
```
micro /path_to_current_directory/kSNP3.1_Linux_package/kSNP3
```
Edit line 7 from ```set kSNP=/usr/local/kSNP3``` to ```set kSNP=/path_to_current_directory/kSNP3.1_Linux_package/kSNP3```

3. Edit PATH
```
micro ~/.bashrc
export PATH=$PATH:$/path_to_current_directory/kSNP3.1_Linux_package/kSNP3
```

kSNP Run Instructions
1. Create input list file
    1. Put all genome fasta files into directory (containing only these files) named fastas
    2. Name files in directory by genome name
    3. $ MakeKSNP3infile fastas in_list A
2. Run kSNP with output to directory named Run1
    1. kSNP3 -in in_list -outdir Run1 -k 19 -ML | tee Run1Log


### Antibiotic resistance gene (ARG) and virulance factor (VF) profiles

To generate ARG and VF profiles we will use ARiBA and VirulanceFinder.

**ARIBA** works by matching sequences in pair reads to known virulence genes from a custom database. Before running the tool the 
reference database needs to be downloaded and prepared (in this case CARD) with the following commands:

```
ariba getref card out.card
ariba prepareref -f out.card.fa -m out.card.tsv out.card.prepareref
```
Use the -h flag to see all the possible databases that the getref command can download.

To run the tool use the following command:

```
ariba run out.card.prepareref <reads1_file> <read2_file> <output_folder>
```

This will create a folder with the results for each of the isolates. The folder contains three .fa.gz files that contain the assembled sequences, genes and assemblies for the analyzed paired reads. The folder will also contain a a report.tsv that details all the matches found and if there are SNPs in the matched genes. 

To get a summary table of multiple runs use the following command:

```
ariba summary <output_file> <out.report.1> <out.report.2>
```

Instead of typing the filepaths for all individual reports you can use wildcards, for example:

```
ariba summary merged_report ./Results/*.card.out/report.tsv
```
This will create a CSV file that contains a table that describe each of the isolates and presence/absence of the matched genes. This file can be used to generate a heatmap.


**Virulence Finder** works by matching assembled genomes sequences to virulence associated genes. The output consists of several files that 
describe 
the matched genes and quality of the match. The first step to run the tool is to download the database that contains the sequences of the 
virulence associated genes. After that the downloaded folder needs to be renamed:

```
git clone https://bitbucket.org/genomicepidemiology/virulencefinder_db/
mv virulencefinder_db virulencefinder
```

Pull the docker image of the tool with the following command:

```
docker pull goseqit/kmerfinder_goseqit_docker
```

After this the tool is ready. To run an assembled genome use the following command:

```
docker run --rm -it -v ./virulencefinder/virulence_ecoli.fsa -v $(pwd):/workdir virulencefinder -i <assembled_genome> -o ./<output_folder>/ > virulencefinder.results
```
Four files will be generated. The .fsa files will contain the sequences of the matched genes. The .results and .results_tab files will contain the summary data of the run, indicating the matched genes and the quality of the match.

