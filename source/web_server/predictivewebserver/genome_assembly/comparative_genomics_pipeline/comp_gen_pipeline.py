#!/usr/bin/env python3
#Author: Jen Kintzle
#Comparative Genomics Pipeline
#Ex: python3 comp_gen_pipeline.py -d inputfiles

import subprocess
import argparse
import os
import sys
import multiprocessing

#define arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', help='The directory of the input files')
parser.add_argument('-M', help='Run stringMLST', default = True)
parser.add_argument('-K', help='Run kSNP3', default = True)
parser.add_argument('-F', help='Run fastANI', default = True)
parser.add_argument('-C', help='Run chewBBACA', default = True)
parser.add_argument('-V', help='Run Ariba - Virulence', default = True)
parser.add_argument('-R', help='Run Ariba - Antimicrobial Resistance', default = True)
args = parser.parse_args()

#Initialize and default
#Flags to determine which tools to run
stringMLST_ind = args.M
ksnp_ind = args.K
fastANI_ind = args.F
chewBBACA_ind = args.C
ariba_vir_ind = args.V
ariba_ind = args.R
#Input file directory
input_dir = args.d
#data needed for stringMLST
mlstDB = '/projects/team-2/jkintzle3/Databases/Escherichia_coli_1/Escherichia_coli_1'
stringMLST_res = 'comparative_genomics_results/stringMLSTResult.tsv'
#data needed for kSNP
ksnp_output_dir = 'comparative_genomics_results/ksnp_res'
ksnp_kmer = '19'
#data needed for fastANI
fastANI_res = 'comparative_genomics_results/fastANI_res.tsv'
#data needed for Ariba
ariba_db = '/projects/team-2/jkintzle3/Databases/out.card.prepareref'
ariba_res = 'comparative_genomics_results/ariba_res'
ariba_vir_db = '/projects/team-2/jkintzle3/Databases/out.vf.prepareref'
#data needed for chewBBACA
chewbbaca_db = '/projects/team-2/jkintzle3/Databases/Ecoli_db'
training = '/projects/team-2/jkintzle3/Databases/Escherichia_coli.trn'
scheme_dir = '/projects/team-2/jkintzle3/Databases/Ecoli_db/ecoli_INNUENDO_wgMLST'
allele_out = 'comparative_genomics_results/chewBBACA_allele_output'
cpus = str((multiprocessing.cpu_count() - 1))
num_of_iterations = '1'
max_threshold = '100'
steps = '1'
test_qual_out = 'comparative_genomics_results/test_qual_output'
cgMLST_out = 'comparative_genomics_results/cgMLST_output'
genome_remove = test_qual_out+'/removedGenomes.txt'
schema_eval_out = 'comparative_genomics_results/schema_eavluator_output'


#function to run stringMLST
def run_stringMLST(fastq_input_dir):
    #stringMLST.py --predict -P Escherichia_coli_1/Escherichia_coli_1 -d fastq
    with open(stringMLST_res, 'w+') as f:
        p = subprocess.run(['stringMLST.py','--predict','-P',mlstDB,'-d',fastq_input_dir], stdout=f)

#function to run ksnp    
def run_ksnp(fasta_input_dir):
    #Make infile: MakeKSNP3infile fastas in_list A
    subprocess.run(['MakeKSNP3infile',fasta_input_dir, 'in_list', 'A']) 
    #kSNP3 -in in_list -outdir Run1 -k 19 -ML 
    subprocess.run(['kSNP3','-in','in_list','-outdir',ksnp_output_dir,'-k',ksnp_kmer,'-ML'])

#function to run fastANI
def run_fastANI(fasta_input_dir):
    #create a list of the fasta files
    files = os.listdir(fasta_input_dir)
    sys.stdout = open('ani_list', 'w+')
    for f in files:
        print(fasta_input_dir + '/' + f)
    sys.stdout.close()
    #run the fastANI script
    subprocess.run(['fastANI','--ql','ani_list','--rl','ani_list','-o',fastANI_res])

#function to run ariba
def run_ariba(fastq_input_dir):
    i = 0
    #find the matching reads
    file_name_list = []
    for root, dirs, files in os.walk(fastq_input_dir):
        for file in files:
            filename = (fastq_input_dir + "/" + file)
            file_name_list.append(filename)
    file_name_list =  sorted(file_name_list)
    while i < (len(file_name_list)-1):
        read1 = file_name_list[i]
        read2 = file_name_list[i+1]
        i+=2
        #ariba run out.card.prepareref fastq/CGT1009_1.fq.gz fastq/CGT1009_2.fq.gz ariba_res
        subprocess.run(['ariba','run',ariba_db,read1,read2,ariba_res])

def run_ariba_vir(fastq_input_dir, ariba_vir_db):
    i = 0
    #find the matching reads
    file_name_list = []
    for root, dirs, files in os.walk(fastq_input_dir):
        for file in files:
            filename = (fastq_input_dir + "/" + file)
            file_name_list.append(filename)
    file_name_list =  sorted(file_name_list)
    while i < (len(file_name_list)-1):
        read1 = file_name_list[i]
        read2 = file_name_list[i+1]
        i+=2
        ariba_vir_res = read1.split("_")[0] + '.vf.out'
        # ariba run out.vf.prepareref <read_1> <read_2> <output_folder>
        subprocess.run(['ariba','run',ariba_vir_db,read1,read2,ariba_vir_res])

#function to run chewBBACA
def run_chewBBACA(genomes):
    #Allele Call
    #chewBBACA.py AlleleCall -i scaffolds -g Ecoli_db/ecoli_INNUENDO_wgMLST -o chewBBACA_allele_out --cpu 2 --ptf Escherichia_coli.trn
    subprocess.run(['chewBBACA.py','AlleleCall','-i',genomes,'-g',scheme_dir,'-o',allele_out,'--cpu',cpus,'--ptf',training])
    #Find subdirectory for allele results
    sub_dir = os.listdir(allele_out)[0]
    allele_results = allele_out + '/' + sub_dir + '/results_alleles.tsv'
    repeats = allele_out + '/' + sub_dir + '/RepeatedLoci.txt'
    #Test Genome Quality
    #chewBBACA.py TestGenomeQuality -i chewBBACA_allele_output/results_20210423T105611/results_alleles.tsv -n 1 -t 100 -s 1 -o test_qual_output
    subprocess.run(['chewBBACA.py','TestGenomeQuality','-i',allele_results,'-n',num_of_iterations,'-t',max_threshold,'-s',steps,'-o',test_qual_out])
    #Extract cgMLST
    #chewBBACA.py ExtractCgMLST -i chewBBACA_allele_output/results_20210423T105611/results_alleles.tsv -o cgMLST_output --r chewBBACA_allele_output/results_20210423T105611/RepeatedLoci.txt --g test_qual_output/removedGenomes.txt
    subprocess.run(['chewBBACA.py','ExtractCgMLST','-i',allele_results,'-o',cgMLST_out,'--r',repeats,'--g',genome_remove])
    #Schema Evaluator
    #chewBBACA.py SchemaEvaluator -i Ecoli_db/ecoli_INNUENDO_wgMLST -o 1schema_eval_output --cpu 6
    subprocess.run(['chewBBACA.py','SchemaEvaluator','-i',scheme_dir,'-o',schema_eval_out,'--cpu',cpus])

#create directories and move files to unique folders
os.chdir(input_dir)
if not os.path.exists('fastq_files'):
    os.makedirs('fastq_files')
fastq_input_dir = 'fastq_files'
if not os.path.exists('fasta_files'):
    os.makedirs('fasta_files')
fasta_input_dir = 'fasta_files'
if not os.path.exists('scaffold_files'):
    os.makedirs('scaffold_files')
genomes = 'scaffold_files'

subprocess.call('mv *.fq* fastq_files', shell=True)
subprocess.call('mv *Scaffolds.fasta scaffold_files', shell=True)
subprocess.call('mv *.fasta fasta_files', shell=True)

#create results directory
if not os.path.exists('comparative_genomics_results'):
    os.makedirs('comparative_genomics_results')
#call functions
if stringMLST_ind == True:
    run_stringMLST(fastq_input_dir)
if ksnp_ind == True:
    run_ksnp(fasta_input_dir)
if fastANI_ind == True:
    run_fastANI(fasta_input_dir)
if ariba_ind == True:
    run_ariba(fastq_input_dir)
if chewBBACA_ind == True:
    run_chewBBACA(genomes)
if ariba_vir_ind == True:
    run_ariba_vir(fastq_input_dir,ariba_vir_db)
