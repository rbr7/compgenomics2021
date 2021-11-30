# Team 2 Genome Assembly


## Pre-requisite installations

We recommend installing Conda and setting up different environments for each software tool listed below. Visit 
https://conda.io/projects/conda/en/latest/user-guide/install/index.html for installation instructions. If you are unfamiliar wit how to setup 
environements you can learn here: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

## Softwares tools and Versions 

```
conda install -c bioconda fastqc multiqc fastp spades quast kat
```

fastqc v0.11.8\
multiqc v1.6\
fastp v0.20.1\
SPAdes v3.13.0\
QUAST v5.1.0\
KATS v2.4.2

## Pipeline:

This is the workflow for de novo assembly. Briefly, we check the read quality using FastQC then run MultiQC for combining all graphs 
into one easy-to-read graph.  Then we trim the reads using Fastp (using theh parameters listed below in the pipeline), run FastQC followed by 
MultiQC to check the trimmed reads. The trimmed reads are assembled in SPAdes and quality checked using QUAST.  

### Quality Check

Check the quality of your reads using FastQC.  

```
for i in *fq.gz
do
	fastqc -o /path/to/output/dir $i
done
```

or if you have ```parallel``` installed on your system you can run FastQC faster:

```
find /path/to/reads/ -name '*.fq.gz' | awk '{printf("fastqc -o /path/to/output/dir/ \"%s\"\n", $0)}' | parallel -j 5 --verbose
```

If using ```parallel``` you can change the number of threads using the flag -j.  Here we used 5

Then run MultiQC in the directory with all the FastQC read

```
cd /path/to/fastqc_reads/dir/
multiqc .
```

This will generate a directory mutiple files and an html file.  Open the html file to view the quality statistics

### Trimming with FastP

To trim the reads:

```
fastp -i <input_R1> -I <input_R2> -o <output_R1> -O <output_R2> -f 5 -F 30 -t 10 -e 28 -c -5 5 -M 27 -j fastp.json
```

Given the quality statistics, we decided to trim read 1 by 5 base pairs, as we had no reads with extremely low quality and we wanted to keep as 
much of our data of acceptable quality as possible for downstream analyses. This feature denoted by -f 5 in our code. We allowed for read 2 to be 
trimmed up to 30 base pairs as quality on the 3' end is often the lowest. This is denoted by -F 30 in our code. We allowed for read 1 to be trimmed 
from the tail up to 10 base pairs, again this was an effective balance between quality and keeping as much good data as we could. This feature is
 utilized in our code by -t 10. We maintained an average quality score of 28 across the whole read, as this was an effective measure we observed from the MultiQC 
report of our initial FastQC results. This is denoted in our code by -e 28. We enabled base correction as this will help keep more reads, this 
feature is enabled by -c. We wanted the sliding window to move from the 5' end with a sliding window to evaluate quality of 5 base pairs at a 
time. This is denoted by -5 5 in our code. We also specified a mean cut quality of 27, this is the threshold used for the sliding window. This 
is denoted by -M 27.

After, run Fastqc followed by Multiqc again (look above for how to do this) to check the quality statistics.

### De Novo Assembly using SPAdes and quality check with QUAST

To assemble the trimmmed reads

```
spades.py --careful -o <path/to/dir/output> -1 <trim_read1.fq> -2 <read2.fq>
```

Then check the assembly statistics using QUAST

```
quast -o /path/to/output/dir <files_with_contigs>
```


