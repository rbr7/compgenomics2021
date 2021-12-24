# Team 2 Gene Prediction
#### Dependencies
GeneMarkS-2
Prodigal
BLAST
Diamond
Aragorn
Barrnap
Infernal
HMMER
MGKit
Bedtools
Emboss
Perl
Python3

#### Usage
##### Inputs
```
-i: path to input assembly fasta file (required)
-d: path to reference database that Diamond will use (required)
-b: path to reference database that BLAST will use (required)
-f: path to reference database that Infernal will use (required)
-m: minimum overlap required to be used with bedtools intersect- range (0,1], default 1
-p: minimum percent identity that a predicted ab initio gene must have with a hit in BLAST in order to be kept- range (0,100], default 90
```
##### Example Usage
```
python3 -i geneprediction_pipeline.py -i ~/geneprediction/Data/CGT1009_careful_Scaffolds.fasta -d ~/geneprediction/Databases/Ecoli_k12_mg1655_refdb_protein.faa -m 0.99 -b ~/geneprediction/Databases/Ecoli_k12_mg1655_refdb_protein.faa -f ~/geneprediction/Databases/Rfam.cm
```
This command will output a number of results to the folder ~/geneprediction/Data/CGT1009.
The most important output files are:
- **CGT1009.final.gff:** A .gff file containing a list of all predicted coding, tRNA, and rRNA genes
- **CGT1009.final.fna:** A .fna file containing the nucleotide sequence of every predicted gene. The header for each sequence is the value stored in the "Name" attribute of the final column of CGT1009.final.gff
- **CGT1009.coding.faa:** A .faa file containing the translated amino acid sequence of every predicted protein-coding gene. The header for each sequence is the value stored in the "Name" attribute of the final column of CGT1009.final.gff
