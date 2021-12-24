#!/bin/bash

while getopts "s:i:o:" options
do
	case $options in
		s)subject=$OPTARG
			;;
		i)inpath=$OPTARG
			;; 
		o)outpath=$OPTARG
			;;
	esac
done

cmscan --rfam --tblout $outpath/$subject.infernal.tblout --noali --fmt 2 --clanin /projects/team-2/jkintzle3/Databases/Rfam.clanin /projects/team-2/jkintzle3/Databases/Rfam.cm $inpath

grep -v ^\# $outpath/$subject.infernal.tblout | awk '{if($12=="-"){printf("%s\tinfernal\t%s\t%s\t%s\t%s\t%s\t.\t.\n",$4,$2,$11,$10,$17,$12);} else{printf("%s\tinfernal\t%s\t%s\t%s\t%s\t%s\t.\t.\n",$4,$2,$10,$11,$17,$12);}}' > $outpath/$subject.infernal.gff


