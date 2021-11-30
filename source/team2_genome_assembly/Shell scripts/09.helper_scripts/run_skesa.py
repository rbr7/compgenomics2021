import os
import subprocess
import argparse

#it has to take the inputs and outputs
#to find paths of the trimmed reads, implement in the same function.
def find_filenames(dir_path):
    file_name_list = []
    trimmed_file_path_list = []
    files_dict = {}
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            #extend this to work with files that end with different file names.
            if file.endswith('.fq'):
                trimmed_file_path_list.append(os.path.join(root, file))
                if '_r1' in file:
                    filename = file.split('_')[0]
                    file_name_list.append(filename)
    file_name_list, trimmed_file_path_list =  sorted(file_name_list), sorted(trimmed_file_path_list) 
    #print(file_name_list)
    #print(trimmed_file_path_list)
    for i in range(0, len(file_name_list)):
        j = i * 2
        files_dict[file_name_list[i]] = [trimmed_file_path_list[j], trimmed_file_path_list[j+1]]
    return files_dict


def run_skesa(trimmed_files_dict, skesa_output_dir):
    #skesa --fastq sample1 sample2 --contigs_out sample/contigs.fasta
    all_samples = trimmed_files_dict
    samples = list(all_samples.keys())
    for id in samples:
        r1 = all_samples[id][0]
        r2 = all_samples[id][1]
        #the print statements needs to be commented
        print('the reads are', r1, r2)
        skesa_output_file = skesa_output_dir + '/' + id + '_skesa_contigs.fasta'
        subprocess.run(['skesa', '--fastq', r1, r2, '--contigs_out', skesa_output_file])





if __name__ == "__main__":
    #this is the main function of your script
    #get the folder of the data from argparse
    #put the logs in the background and implement multithreading
    input_data_dir = '/home/team2/01.genome.assembly/04.fastp'
    #input_data_dir = '/home/abharadwaj61/test/fastp'
    #skesa_output_dir = '/home/abharadwaj61/test/assemblies/SKESA'
    skesa_output_dir = '/home/team2/01.genome.assembly/03.assembly/03.SKESA'
    trimmed_files_dict = find_filenames(input_data_dir)
    run_skesa(trimmed_files_dict, skesa_output_dir)

