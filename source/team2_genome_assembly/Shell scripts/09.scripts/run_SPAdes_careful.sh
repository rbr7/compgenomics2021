#!/bin/bash

in_dir=/home/team2/01.genome.assembly/04.fastp
out_dir=/home/team2/01.genome.assembly/03.assembly/02.SPAdes


for input in *_r1.fq ; do

	sid=$(basename ${input} _r1.fq)

	if [[ ! -d ${out_dir}/${sid}.fastp.careful.SPAdes ]] ; then 
		echo "Creating ${sid}.fastp.careful.SPAdes directory and running SPAdes"
		mkdir ${out_dir}/${sid}.fastp.careful.SPAdes
		spades.py --careful -o ${out_dir}/${sid}.fastp.careful.SPAdes -1 ${input} -2 ${sid}_r2.fq
	else
		echo "${sid}.fastp.careful.SPAdes already exists"
		continue
	fi
done
