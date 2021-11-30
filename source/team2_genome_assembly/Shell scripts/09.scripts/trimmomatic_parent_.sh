#!/bin/bash


while getopts "d:" flag
do
    case "${flag}" in
        d) dir_name=${OPTARG};;
    esac
done

### DO NOT CHANGE THIS ###
trim_path=/home/team2/01.genome.assembly/02.trimmomatic/Trimmomatic-0.39/trimmomatic-0.39.jar
out_dir=/home/team2/01.genome.assembly/02.trimmed_reads/01.trimmomatic/02.trimmed_failed_reads

### parameters #######################################
#parameters="LEADING:10 MINLEN:50 SLIDINGWINDOW:5:20"
#parameters="LEADING:20 MINLEN:50 SLIDINGWINDOW:5:20"
#parameters="SLIDINGWINDOW:5:20"
#parameters="LEADING:10"
parameters="HEADCROP:10"
######################################################

mkdir -p ${out_dir}/${dir_name}/LOG

for input in *_1.fq.gz; do
	sid=$(basename ${input} _1.fq.gz)
	java -jar ${trim_path} PE -trimlog ${out_dir}/${dir_name}/LOG/${sid}.log -threads 6 \
	${input} ${sid}_2.fq.gz ${sid}_1P.fastq.gz ${sid}_1U.fastq.gz \
	${sid}_2P.fastq.gz ${sid}_2U.fastq.gz ${parameters}

#	-baseout ${out_dir}/${dir_name}/${sid}.fg.gz ${parameters}
done
