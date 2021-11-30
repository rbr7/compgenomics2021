#!/usr/bin/python

#import your requried packages here
import os
import argparse
import subprocess

## no exception handling yet, to be added. Logging to be added too

#maybe a dictionary with filenames and their paths?
#find filenames could be part of the utils scirpt
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
    for i in range(0, len(file_name_list)):
        files_dict[file_name_list[i]] = [file_path_list[i], file_path_list[i+1]]
    return files_dict


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



def run_spades(files_dict):
    assembly_dir = '/home/team2/sample_assembly'
    all_samples = files_dict
    samples = all_samples.keys()
    for id in samples:
        r1 = all_samples[id][0]
        r2 = all_samples[id][1]
        print('the two read files are', r1, r2)
        #the output dir path has to be specified as a global variable
        output_dir = assembly_dir + '/' + id
        #custom kmer implementation? if yes, an if loop and another subprocess 
        print('running spades on id: ',id, 'the output will be created in the same directory.')
        subprocess.run(['spades.py', '-1', r1, '-2', r2, '-o', output_dir])


def run_abyss():
    #implementation of running abyss
    print()


def run_masurca():
    #implementation of masurca
    print()



if __name__ == "__main__":
    #this is the main function of your script
    dir_path = '/home/team2/sample_data'
    files_dict = find_filenames(dir_path)
    print(len(files_dict))
    print('[+] running spades on the fastq files')
    run_spades(files_dict)

