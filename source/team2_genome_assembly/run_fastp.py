import argparse
import os
import subprocess


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
    #print(file_name_list)
    #print(file_path_list)
    for i in range(0, len(file_name_list)):
        j = i * 2
        files_dict[file_name_list[i]] = [file_path_list[j], file_path_list[j+1]]
    return files_dict


def run_fastp(files_dict, trim_output_path):
    all_samples = files_dict
    samples = list(files_dict.keys())
    for id in samples:
        print('[+] running fastp on the sample', id)
        #fastp -i SRR8451740_1.fastq -I SRR8451740_2.fastq -o r1.fq -O r2.fq -f 5 -F 30 -t 10 -e 28 -c -5 5 -M 27 -j SRR8451740_fastp.json
        forward_read = all_samples[id][0]
        reverse_read = all_samples[id][1]
        #fr = forward_read.split('/')[-1].split('_')[0]
        #rr = reverse_read.split('/')[-1].split('.')[0]
        forward_op = trim_output_path + '/' + id + '_r1.fq'
        reverse_op= trim_output_path + '/' + id + '_r2.fq'
        json_file_name = trim_output_path + '/' + id + '_fastp.json'
        subprocess.run(['fastp', '-i', forward_read, '-I', reverse_read, '-o', forward_op, '-O', reverse_op, '-f', '5', '-F', '30', 't', '10', '-e', '28', '-c', '-5', '5', '-M', '27', '-j', json_file_name])



def run_multiqc(qc_dir_path, multiqc_op_path):
    #the input to this will just be the directory which contains the qc.
    subprocess.run(['multiqc', qc_dir_path, '-o', multiqc_op_path])



if __name__ == "__main__":
    #this is the main function of your script
    #get the folder of the data from argparse
    #put the logs in the background and implement multithreading
    input_dir_path = '/home/team2/data_bkp'
    #trim_output_path = '/home/abharadwaj61/test/fastp'
    trim_output_path = '/home/team2/01.genome.assembly/04.fastp'
    #trim_multiqc_output_path = '/home/abharadwaj61/test/multiqc_trim'
    trim_multiqc_output_path = '/home/team2/01.genome.assembly/04b.multiqc_fastp'
    files_dict = find_filenames(input_dir_path)
    run_fastp(files_dict, trim_output_path)
    run_multiqc(trim_output_path, trim_multiqc_output_path)

