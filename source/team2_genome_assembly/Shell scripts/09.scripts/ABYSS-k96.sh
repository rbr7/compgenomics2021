#!/bin/bash

outpath=/home/team2/01.genome.assembly/03.assembly/01.abyss

for i in *_1.fq.gz
do

	sid=$(basename ${i} _1.fq.gz)

	if [[ ! -d ${outpath}/${sid}.96k ]]
	then
		echo "${sid} directory does not exist"
                echo "Creating ${sid} directory in path: ${output}"
                mkdir ${outpath}/${sid}.96k
                cp ${i} ${sid}_2.fq.gz ${outpath}/${sid}.96k
                abyss-pe -C ${outpath}/${sid}.96k np=2 j=4 name=${sid} k=96 in="${i} ${sid}_2.fq.gz"
	elif [[ -d ${outpath}/${sid}.96k ]] 
	then
		if [[ -z "$(ls -A ${outpath}/${sid}.96k)" ]]
		then
			echo "${sid} exists but is empty"
			echo "removing empty ${sid}"
			rm -r ${outpath}/${sid}.96k
		elif [[ ! -z "$(ls -A ${outpath}/${sid}.96k)" ]]
		then
			echo "${sid} exists and has files"
                	echo "please manually check ${sid} directory before removing"
		fi
	fi
done

