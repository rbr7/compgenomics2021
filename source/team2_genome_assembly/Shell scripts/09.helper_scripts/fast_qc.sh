#!/bin/bash

fq_dir=/home/team2/data/

#find all fq files; run fastcc in parallel; modify '-j' parameter for more/less cores
find ${fq_dir} -name '*.fq.gz' | awk '{printf("fastqc -o /home/team2/01.genome.assembly/01.fastqc \"%s\"\n", $0)}' | parallel -j 5 
--verbose


#find fastqc files and move them to directory; modify '/path/to/dir/' (input dir) and './' (output dir) to any directoy  
#find /path/to/dir/ -name '*fastqc.*' | xargs -I '{}' mv '{}' ./
