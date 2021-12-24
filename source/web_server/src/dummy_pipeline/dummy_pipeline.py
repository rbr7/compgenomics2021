#!/usr/bin/env python3
#Author: Jen Kintzle
#Overall Pipeline

import os
import time

def list_files(filepath, filetype):
    paths = []
    for root, dirs, files in os.walk(filepath):
        for file in files:
            if file.lower().endswith(filetype.lower()):
                paths.append(os.path.join(root, file))
    return(paths)

def call_main(d, ga=False, gp=False, fa=False, cg=False):
    #Determine pipeline components to call
    call_genome_assembly_ind = ga
    call_gene_prediction_ind = gp
    call_func_ann_ind = fa
    call_comp_genomics_ind = cg
    
    #Identify base directory
    dir_path = d
    if not os.path.exists('results'):
        os.makedirs('results')
    results_dir = dir_path + 'results/'
    home_dir = str('/'.join(dir_path.split('/')[:-1])) + '/'

    #Call Genome Assembly if requested
    if call_genome_assembly_ind == True:
        #call the genome assembly pipeline
        #find input files
        file_name_list = list_files(home_dir, '.fq.gz')
        time.sleep(10)
        #create fake results file
        os.chdir(results_dir)
        f = open('read1_contigs.fasta', 'w')
        f.write('Contig results written to this file')
        for item in file_name_list:
            f.write('%s\n' % item)
        f.close()
        
    if call_gene_prediction_ind == True:
        #call the gene prediction pipeline
        #find input files
        file_name_list = list_files(home_dir, '.fasta')
        time.sleep(10)
        #create fake results files
        os.chdir(results_dir)
        f = open('read1.gff', 'w')
        f.write('Results written to this file')
        for item in file_name_list:
            f.write('%s\n' % item)
        f.close()
        f = open('read1.fna', 'w')
        f.write('Results written to this file')
        for item in file_name_list:
            f.write('%s\n' % item)
        f.close()
        f = open('read1.faa', 'w')
        f.write('Results written to this file')
        for item in file_name_list:
            f.write('%s\n' % item)
        f.close()
        f = open('read1_Scaffolds.fasta', 'w')
        f.write('Results written to this file')
        for item in file_name_list:
            f.write('%s\n' % item)
        f.close()
        
    if call_func_ann_ind == True:
        #call the functional annotation pipeline
        #find input files
        file_name_list = list_files(home_dir, '.fq.gz')
        time.sleep(10)
        #create fake results files
        os.chdir(results_dir)
        f = open('read_fa_1.gff', 'w')
        f.write('Results written to this file')
        for item in file_name_list:
            f.write('%s\n' % item)
        f.close()
        f = open('read_fa_1.fna', 'w')
        f.write('Results written to this file')
        for item in file_name_list:
            f.write('%s\n' % item)
        f.close()
        f = open('read_fa_1.faa', 'w')
        f.write('Results written to this file')
        for item in file_name_list:
            f.write('%s\n' % item)
        f.close()
        
    if call_comp_genomics_ind == True:
        #call the comp genomics pipeline
        #find input files
        fasta_file_name_list = list_files(home_dir, '.fasta')
        fastq_file_name_list = list_files(home_dir, '.fq.gz')
        scaffold_file_name_list = list_files(home_dir, 'Scaffolds.fasta')
        time.sleep(10)
        #create fake results files
        os.chdir(results_dir)
        f = open('stringMLSTResult.tsv', 'w')
        f.write('stringMLST results written to this file')
        for item in fastq_file_name_list:
            f.write('%s\n' % item)
        f.close()
        f = open('ksnp_res', 'w')
        f.write('ksnp results written to this file')
        for item in fasta_file_name_list:
            f.write('%s\n' % item)
        f.close()
        f = open('results_alleles.tsv', 'w')
        f.write('Chewbbaca results written to this file')
        for item in scaffold_file_name_list:
            f.write('%s\n' % item)
        f.close()