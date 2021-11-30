#!/bin/bash

outpath=/home/team2/01.genome.assembly/03.assembly/01.abyss
for dir in */
do
	cd ${dir}

	for i in *.fg_1P.fastq
	do

		sid=$(basename ${i} .fg_1P.fastq)
	        abyss-pe np=4 name=${sid} k=96 in='${i} ${sid}.fg_2P.fastq'
	done
	cd ../
done
