#!/bin/bash
user_input () {
	while getopts "d:s:i:o:h" options
	do
		case $options in
        # f_db will be the fasta file for which database has been built 
			d)f_db=$OPTARG
				;;
			s)subject=$OPTARG
				;;	       
			i)inpath=$OPTARG
				;;
			o)outpath=$OPTARG
				;; 
			h)echo "edit"
				;;               
		esac
	done
}

make_db(){
	#diamond makedb --in "$f_db" -d ref_database



	
 	#for file in  $(ls ${input_file}*.fasta);
 	#do
 		
 		
 		
	diamond blastx -d $f_db.dmnd -q $inpath -o $outpath/$subject.diamond.out -p 7 --max-hsps 1 --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen
	/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/gene_prediction_pipeline/diamond2gff.sh -d $f_db -s $subject -i $outpath/$subject.diamond.out -o $outpath
	#done
}
main(){

  user_input "$@"
  make_db "$f_db"  "input_file"
 
}
main "$@"      

	
