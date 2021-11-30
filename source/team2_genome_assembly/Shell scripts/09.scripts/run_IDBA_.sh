#!/bin/bash

in_dir=/home/team2/01.genome.assembly/04.fastp
out_dir=/home/team2/01.genome.assembly/03.assembly/04.idba

for i in ${in_dir}/*.fa
do
	
	sid=$(basename $i .fa)	

	if [[ ! -d ${out_dir}/${sid}.UD ]]
	then	
		echo "${sid} direcrory doesnt exist"
		echo "Creating ${sid}.UD in path: ${out_dir}"
		mkdir ${out_dir}/${sid}.UD	

	elif [[ -d ${out_dir}/${sid}.UD ]]
	then
		if [[ "$(ls -A ${out_dir}/${sid}.UD)" ]]
		then
			echo "${sid}.UD Exists and is not empty"
                        echo "please check the ${sid}.UD directory manually"			
		else
			echo "${sid}.new Exists but is empty"
                        echo "Removing ${sid}.UD from path: ${out_dir}"
		fi
	fi

	idba --mink 33 --maxk 77 --step 22 -o ${out_dir}/${sid}.UD -r $i
	
done

