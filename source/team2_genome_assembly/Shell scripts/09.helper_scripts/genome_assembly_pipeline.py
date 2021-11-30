#!/usr/bin/python

import os
import subprocess
import argparse


## no exception handling yet, to be added. Logging to be added too (in progress, needs to be detailed)

def find_filenames(dir_path):
    file_name_list = []
    file_path_list = []
    files_dict = {}
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path_list.append(os.path.join(root, file))
            if '_1' in file:
                filename = file.split('_')[0]
                file_name_list.append(filename)
    file_name_list, file_path_list =  sorted(file_name_list), sorted(file_path_list) 
    print(file_name_list)
    print(file_path_list)
    for i in range(0, len(file_name_list)):
        j = i * 2
        files_dict[file_name_list[i]] = [file_path_list[j], file_path_list[j+1]]
    return files_dict


#function to run fastqc on the list of files found. Threading needs to be implemented to make it faster, if not it will be painfully slow.
def run_fastqc(files_dict, qc_output_dir):
    all_samples = files_dict
    samples = list(files_dict.keys())
    #output_dir = '/home/abharadwaj61/test/fastqc'
    for id in samples:
        #you need to run fastqc without generating the HTML files. #run this on your local part of the server.
        print(f'[+] running fastqc on the sample {id}')
        sample_op_dir = qc_output_dir + '/' + id
        print('[+] writing the output files to this directory', qc_output_dir)
        print(all_samples[id][0], all_samples[id][1])
        subprocess.run(['fastqc', '-o', qc_output_dir, all_samples[id][0]])
        subprocess.run(['fastqc', '-o', qc_output_dir, all_samples[id][1]])
        #do i need to return anything here?
    

#function to run the multiqc
def run_multiqc(qc_output_dir):
    #the input to this will just be the directory which contains the qc.
    multiqc_op_path = qc_output_dir + '/' + 'multiqc_output'
    subprocess.run(['multiqc', qc_output_dir, '-o', multiqc_op_path])
    return multiqc_op_path


#helper function to find the poor quality files from the multiqc report.
#the function returns number of poor quality samples and their names.
def find_poor_quality_files(multiqc_op_path):
    print('finding poor quality files')
    file_path = multiqc_op_path + '/multiqc_data/' + 'multiqc_fastqc.txt'
    with open(file_path) as f1:
        report_lines = [line.split('\t') for line in f1.readlines()]
    poor_quality_files = []
    for line in report_lines:
        if line[11] == 'fail':
            poor_quality_files.append(line[0])
            #how will you get the full path of these files to run the qc loop again? something to think about - Dictionary structure implemented to solve this
            #all you need is the sample ID
    return len(poor_quality_files), poor_quality_files


def run_trimmomatic():
    #function implementation to run trimmomatic here
    print('this does nothing yet')


def run_fastp():
    #function to run fastp 
    print('this does nothing yet')

#function to run velvet for the assembly (not tested, as unpaired.fq might be required)
def run_velvet(files_dict):
    #iterate over files_dict keys, create those directories and pass the keys are values
    all_samples = files_dict
    samples = files_dict.keys()
    for id in samples:
        subprocess.run('mkdir', '-p', id)
        #velveth assem91 91 -shortPaired -fastq -separate ../trimmed_reads/r1.fq ../trimmed_reads/r2.fq -short2 -fastq ../trimmed_reads/unpaired.fq 
        #velvetg assem91 -min_contig_lgth 500
        #find filenames should be run on the trimmmed reads as well, if that step needs to take place. just change the dir_path
        #write another function in the utils to handle file extention type
        #does velvet handle writing into a separate directory? you need to find this out. or copy everything else from the default direotry where it creates. Might be slower.
        #when trimming, the output files need to be samplename_r1.fq and call this for everything else
        unpaired_filename = id + 'unpaired.fq'
        subprocess.run(['velveth', 'assem91', '91', '-shortPaired', '-fastp', '-separate', all_samples[id][0], all_samples[id][1], '-short2', '-fastq', unpaired_filename])
        subprocess.run(['velvetg', 'assem91', '-min_contig_lgth', 500])


def run_spades(files_dict, assembly_dir):
    all_samples = files_dict
    samples = all_samples.keys()
    for id in samples:
        r1 = all_samples[id][0]
        r2 = all_samples[id][1]
        print('the two read files are', r1, r2)
        #the output dir path has to be specified as a global variable
        assembly_output_dir = assembly_dir + '/' + id
        #custom kmer implementation? if yes, an if loop and another subprocess 
        print('running spades on id: ', id, 'the output will be created in the directory with the same name.')
        subprocess.run(['spades.py', '-1', r1, '-2', r2, '-o', assembly_output_dir])



if __name__ == "__main__":
    #this is the main function of your script
    #get the folder of the data from argparse
    #put the logs in the background and implement multithreading
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='use this argument to enter the input of the raw reads')
    parser.add_argument('-a', '--assembler', default = [], help='use this to pass the list of assemblers to run on, possible options: SPAdes, ABYss, masuRCA, Velvet')
    parser.add_argument('-l', '--logging', action='store_true', help='Logging flag')
    #dir_path = '/home/abharadwaj61/data'
    args = parser.parse_args()
    dir_path = args.input
    assembler_list = args.assembler
    logging_enabled = args.logging
    #add all the standard directory initializations here
    #add implemention to check if the directories exist or not. especially for the input.
    assembly_dir = '/home/abharadwaj61/test/assemblies'
    qc_output_dir = '/home/abharadwaj61/test/fastqc'
    if logging_enabled:
        print('[+] creating a dictionary with all the samples and the path of each pair of reads in the sample')
    files_dict = find_filenames(dir_path)
    #print(len(files_dict))
    #print(files_dict)
    if logging_enabled:
        print('[+] running fastqc on the samples')
    run_fastqc(files_dict, qc_output_dir)
    if logging_enabled:
        print('[+] running multiqc on the samples')
    multiqc_op_path = run_multiqc(qc_output_dir)
    #qc_dir_path = '/home/abharadwaj61/test/fastqc' 
    #multiqc_op_path = qc_dir_path + '/' + 'multiqc_output'
    if logging_enabled:
        print('[+] finding poor quality files from QC')
    no_of_poor_quality_files, poor_quality_files = find_poor_quality_files(multiqc_op_path)
    if no_of_poor_quality_files > 0:
        if logging_enabled:
            print('[-] poor quality files found after running QC')
            str1 = ' '.join([str(x) for x in poor_quality_files])
            print('[-] these files are', str1)
        #take an input flag here to run trimming, but how would this sit with the predictive web server??
        #which trimming tool and write the function. 
        #do I need a copy step to which copies the samples that have passed QC or, Just an if condition that takes care of this?
    else:
        if logging_enabled:
            print('[+] No trimming required, all the reads have passed the set quality threshold')
    #here I would need to make the call for the assemblers.
    #running the assembly part of the script here, ennumeration required to run different 
    #for now, let's just run it from the reads assuming that the qc results are good.
    #check the flag for the assemblers in the list
    if logging_enabled:
        print('[+] Initiating the SPAdes assembler!!')
    run_spades(files_dict, assembly_dir)



