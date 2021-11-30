!/usr/bin/env bash

shopt -s nullglob

samples=$(ls raw_data/)

shopt -u nullglob

for i in $samples
do
	# SKESA
	cd KAT_results/SKESA/$i
	kat comp -t 2 ~/quast-5.1.0rc1/Genome_assembly_results/raw_data/$i/$i"_1.fq.gz" ~/quast-5.1.0rc1/Genome_assembly_results/raw_data/$i/$i"_2.fq.gz" ~/quast-5.1.0rc1/Genome_assembly_results/SKESA/$i"_skesa_contigs.fasta"
	cd /home/gcruz8/quast-5.1.0rc1/Genome_assembly_results 

	# SPAdes
	mkdir KAT_results/SPAdes/$i
        cd KAT_results/SPAdes/$i
	kat comp -t 2 ~/quast-5.1.0rc1/Genome_assembly_results/raw_data/$i/$i"_1.fq.gz" ~/quast-5.1.0rc1/Genome_assembly_results/raw_data/$i/$i"_2.fq.gz" ~/quast-5.1.0rc1/Genome_assembly_results/SPAdes/$i"_careful_Contigs.fasta"
	cd /home/gcruz8/quast-5.1.0rc1/Genome_assembly_results

	# IDBA
	mkdir KAT_results/IDBA/$i
        cd KAT_results/IDBA/$i	
	kat comp -t 2 ~/quast-5.1.0rc1/Genome_assembly_results/raw_data/$i/$i"_1.fq.gz" ~/quast-5.1.0rc1/Genome_assembly_results/raw_data/$i/$i"_2.fq.gz" ~/quast-5.1.0rc1/Genome_assembly_results/IDBA/$i".new_contig.fa"
	cd /home/gcruz8/quast-5.1.0rc1/Genome_assembly_results
done
