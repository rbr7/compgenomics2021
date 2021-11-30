#!/bin/bash

# This script assumes quast.py is in the same directory as this script

if [ ! -d QUAST_results ];
then
	mkdir QUAST_results
fi

for assembler in $(ls /home/team2/01.genome.assembly/03.assembly/05.output);
do	
	echo $assembler
	if [ ! -d ./QUAST_results/$assembler ];
	then
		mkdir "./QUAST_results/$assembler/"
	fi
/home/team2/01.genome.assembly/03.assembly/05.output/SPAdes.output/contigs.output

	for read in $(ls /home/team2/01.genome.assembly/03.assembly/05.output/$assembler/contigs.output);
	do
		if [ ! -d ./QUAST_results/$assembler/$read ];
		then
			
			mkdir "./QUAST_results/$assembler/$read"
			./quast.py -o ./QUAST_results/$assembler/$read/ /home/team2/01.genome.assembly/03.assembly/05.output/$assembler/contigs.output/$read --plots-format png --labels $assembler"_"$read --silent
											
		fi
	done
done
