#!/bin/bash
user_input () {
	while getopts "d:s:i:o:h" options
	do
		case $options in
        # path to fasta files 
			i)inpath=$OPTARG
				;;
			d)db=$OPTARG
				;;
			s)subject=$OPTARG
				;;
			o)outpath=$OPTARG
				;;
			h)echo "edit"
				;;
		esac
	done
}

gff_conversion(){

 	#for file in  $(ls ${fasta_files}*.fasta_blast);
 	#do
	blast2gff blastdb -db $db.dmnd $inpath $outpath/$subject.diamond.gff -n

 		
 		
		
	#done
}
main(){

  user_input "$@"
 
  gff_conversion "$fasta_files"  
 
}
main "$@"      

