#!/bin/bash

outpath=/home/team2/01.genome.assembly/03.assembly/01.abyss

for i in *_r1.fq
do

	sid=$(basename ${i} _r1.fq)

	if [[ ! -d ${outpath}/${sid}.21k ]]
	then
		echo "${sid} directory does not exist"
                echo "Creating ${sid} directory in path: ${output}"
                mkdir ${outpath}/${sid}.21k
                cp ${i} ${sid}_r2.fq ${outpath}/${sid}.21k
                abyss-pe -C ${outpath}/${sid}.21k np=2 name=${sid} k=21 in="${i} ${sid}_r2.fq"
	elif [[ -d ${outpath}/${sid}.21k ]] 
	then
		if [[ -z "$(ls -A ${outpath}/${sid}.21k)" ]]
		then
			echo "${sid} exists but is empty"
			echo "removing empty ${sid}"
			rm -r ${outpath}/${sid}.21k
		elif [[ ! -z "$(ls -A ${outpath}/${sid}.21k)" ]]
		then
			echo "${sid} exists and has files"
                	echo "please manually check ${sid} directory before removing"
		fi
	fi
done

