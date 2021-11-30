import argparse
import os
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
    print(file_name_list)
    print(file_path_list)
    for i in range(0, len(file_name_list)):
        j = i * 2
        files_dict[file_name_list[i]] = [file_path_list[j], file_path_list[j+1]]
    return files_dict


#function to run fastqc on the list of files found. Threading needs to be implemented to make it faster, if not it will be painfully slow.
def run_fastqc(files_dict):
    all_samples = files_dict
    samples = list(files_dict.keys())
    output_dir = '/home/abharadwaj61/test/fastqc'
    for id in samples:
        #you need to run fastqc without generating the HTML files. #run this on your local part of the server.
        print(f'[+] running fastqc on the sample {id}')
        sample_op_dir = output_dir + '/' + id
        print('[+] writing the output files to this directory', output_dir)
        print(all_samples[id][0], all_samples[id][1])
        subprocess.run(['fastqc', '-o', output_dir, all_samples[id][0]])
        subprocess.run(['fastqc', '-o', output_dir, all_samples[id][1]])
        #do i need to return anything here?
    return output_dir


#function to run the multiqc
def run_multiqc(qc_dir_path):
    #the input to this will just be the directory which contains the qc.
    multiqc_op_path = qc_dir_path + '/' + 'multiqc_output'
    subprocess.run(['multiqc', qc_dir_path, '-o', multiqc_op_path])
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
            #how will you get the full path of these files to run the qc loop again? something to think about
    return len(poor_quality_files), poor_quality_files


def run_trimmomatic():
    #function implementation to run trimmomatic here
    print('this does nothing yet')


def run_fastp():
    #function to run fastp 
    print('this does nothing yet')



if __name__ == "__main__":
    #this is the main function of your script
    #get the folder of the data from argparse
    #put the logs in the background and implement multithreading
    dir_path = '/home/abharadwaj61/data'
    files_dict = find_filenames(dir_path)
    print(len(files_dict))
    print(files_dict)
    #should I pass my output directory here
    #commenting these two because I don't want them to run again. UNCOMMENT LATER! ----
    qc_output_dir = run_fastqc(files_dict)
    multiqc_op_path = run_multiqc(qc_output_dir)
    #qc_dir_path = '/home/abharadwaj61/test/fastqc' 
    #multiqc_op_path = qc_dir_path + '/' + 'multiqc_output'
    no_of_poor_quality_files, poor_quality_files = find_poor_quality_files(multiqc_op_path)
    if no_of_poor_quality_files > 0:
        print('[-] poor quality files found after running QC')
        str1 = ' '.join([str(x) for x in poor_quality_files])
        print('[-] these files are', str1)
        #take an input flag here to run trimming, but how would this sit with the predictive web server??
        #which trimming tool and write the function. 
        #do I need a copy step to which copies the samples that have passed QC or, Just an if condition that takes care of this?
    else:
        print('[+] No trimming required, all the reads have passed the set quality threshold')
    #here I would need to make the call for the assemblers.

