#!/usr/bin/python



import os
import subprocess
import argparse


## no exception handling implemented yet

#function assumes that only fastq files with paired end reads are uploaded

#function to return a dictionary with samples and their paths
def find_fastq_filenames(dir_path):
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


#a variant of the function above, used to find the trimmed reads
def find_trimmed_filenames(dir_path):
    file_name_list = []
    trimmed_file_path_list = []
    files_dict = {}
    for root, dirs, files in os.walk(dir_path):
        for file in files:
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


#function to run fastqc 
def run_fastqc(files_dict, qc_output_dir):
    all_samples = files_dict
    samples = list(files_dict.keys())
    #output_dir = home_dir +'fastqc'
    for id in samples:
        #print(f'[+] running fastqc on the sample {id}')
        sample_op_dir = qc_output_dir + '/' + id
        #print('[+] writing the output files to this directory', qc_output_dir)
        #print(all_samples[id][0], all_samples[id][1])
        subprocess.run(['fastqc', '-o', qc_output_dir, all_samples[id][0]],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(['fastqc', '-o', qc_output_dir, all_samples[id][1]],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    

#function to run the multiqc
def run_multiqc(qc_output_dir, multiqc_op_path):
    #the input to this will just be the directory which contains the qc.
    #multiqc_op_path = qc_output_dir + '/' + 'multiqc_output'
    subprocess.run(['multiqc', qc_output_dir, '-o', multiqc_op_path],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


#helper function to find the poor quality files from the multiqc report.
#the function returns number of poor quality samples and their names.
def find_poor_quality_files(multiqc_op_path):
    #print('finding poor quality files')
    file_path = multiqc_op_path + '/multiqc_data/' + 'multiqc_fastqc.txt'
    with open(file_path) as f1:
        report_lines = [line.split('\t') for line in f1.readlines()]
    poor_quality_files = []
    for line in report_lines:
        if line[11] == 'fail':
            poor_quality_files.append(line[0])
            #all you need is the sample ID
    return len(poor_quality_files), poor_quality_files


def run_trimmomatic():
    #function implementation to run trimmomatic here
    print('this does nothing yet')

#function to run fastp
def run_fastp(files_dict, trim_output_path):
    all_samples = files_dict
    samples = list(files_dict.keys())
    for id in samples:
        #print('[+] running fastp on the sample', id)
        #fastp -i SRR8451740_1.fastq -I SRR8451740_2.fastq -o r1.fq -O r2.fq -f 5 -F 30 -t 10 -e 28 -c -5 5 -M 27 -j SRR8451740_fastp.json
        forward_read = all_samples[id][0]
        reverse_read = all_samples[id][1]
        #fr = forward_read.split('/')[-1].split('_')[0]
        #rr = reverse_read.split('/')[-1].split('.')[0]
        forward_op = trim_output_path + '/' + id + '_r1.fq'
        reverse_op= trim_output_path + '/' + id + '_r2.fq'
        json_file_name = trim_output_path + '/' + id + '_fastp.json'
        subprocess.run(['fastp', '-i', forward_read, '-I', reverse_read, '-o', forward_op, '-O', reverse_op, '-f', '5', '-F', '30', 't', '10', '-e', '28', '-c', '-5', '5', '-M', '27', '-j', json_file_name],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)



def run_skesa(trimmed_files_dict, skesa_output_dir):
    #skesa --fastq sample1 sample2 --contigs_out sample/contigs.fasta
    all_samples = trimmed_files_dict
    samples = list(all_samples.keys())
    for id in samples:
        r1 = all_samples[id][0]
        r2 = all_samples[id][1]
        #print('the reads are', r1, r2)
        skesa_output_file = skesa_output_dir + '/' + id + '_skesa_contigs.fasta'
        subprocess.run(['skesa', '--fastq', r1, r2, '--contigs_out', skesa_output_file],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


#function to run velvet for the assembly (not tested, as unpaired.fq might be required)
def run_velvet(files_dict):
    #iterate over files_dict keys, create those directories and pass the keys are values
    all_samples = files_dict
    samples = files_dict.keys()
    for id in samples:
        subprocess.run('mkdir', '-p', id)
        #velveth assem91 91 -shortPaired -fastq -separate ../trimmed_reads/r1.fq ../trimmed_reads/r2.fq -short2 -fastq ../trimmed_reads/unpaired.fq 
        #velvetg assem91 -min_contig_lgth 500
        #when trimming, the output files need to be samplename_r1.fq and call this for everything else
        unpaired_filename = id + 'unpaired.fq'
        subprocess.run(['velveth', 'assem91', '91', '-shortPaired', '-fastp', '-separate', all_samples[id][0], all_samples[id][1], '-short2', '-fastq', unpaired_filename])
        subprocess.run(['velvetg', 'assem91', '-min_contig_lgth', 500])


#function to run spades
def run_spades(files_dict, spades_assembly_dir):
    all_samples = files_dict
    samples = all_samples.keys()
    for id in samples:
        r1 = all_samples[id][0]
        r2 = all_samples[id][1]
        #print('the two read files are', r1, r2)
        assembly_output_dir = spades_assembly_dir + '/' + id
        #print('running spades on id: ', id, 'the output will be created in the directory with the same name.')
        subprocess.run(['spades.py', '--careful' ,'-1', r1, '-2', r2, '-o', assembly_output_dir],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


#function to run abyss (not tested)
def run_abyss(files_dict, abyss_assembly_dir):
    all_samples = files_dict
    samples = all_samples.keys()
    for id in samples:
        r1 = all_samples[id][0]
        r2 = all_samples[id][1]
    #abyss-pe -C <path/to/dir/output> np=4 j=8 name=<genome name> k=$k in="<path/to/input/dir/read1> <path/to/input/dir/read2>"
        assembly_output_dir = abyss_assembly_dir + '/' + id
        subprocess.run(['abyss', 'pe', '-C', assembly_output_dir, 'np=4', 'j=8', 'name=',id, 'in=', r1, r2],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        #output will be id-contigs.fa
    

#function to run IDBA (not tested)
def run_IDBA(files_dict, idba_assembly_dir):
    all_samples = files_dict
    samples = all_samples.keys()
    for id in samples:
        r1 = all_samples[id][0]
        r2 = all_samples[id][1]
        #fq2fa --merge --filter <id_read1.fq> <is_read2.fq> <id.fa>
        #idba --mink 33 --maxk 77 --step 22 -o <path/to/output/dir> -r <id.fa>
        assembly_output_dir = idba_assembly_dir + '/' + id
        subprocess.run(['fq2fa', '--merge', '--filter', r1, r2, id+'_contigs.fa'],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(['idba', '-mink', 33, 'maxk', 77, '--step', 22, '-o', assembly_output_dir, '-r', id+'_contigs.fa'],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

#all the contigs.fasta needs to be sent as input.
def run_quast(assembly_dir, quast_op_dir):
    #quast.py -o /home/team2/quast_output
    subprocess.call(['quast.py', assembly_dir, '-o', quast_op_dir, '--circos'],  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


#helper function to move all the contigs into a directory
def move_contigs(assembly_dir_path, assembly_contig_dir_path):
    for root, dirs, files in os.walk(assembly_dir_path):
        for file in files:
            if 'contigs.fa' in file:
                subprocess.run(['cp', '-R', os.path.join(root, file), assembly_contig_dir_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)


#helper function to create the directories to store outputs in
def create_dirs(dir_list):
    for path in dir_list:
        #print('creating the path here:', path)
        subprocess.run(['mkdir', '-p', path])

if __name__ == "__main__":

    #parser implementation
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='use this argument to enter the input of the raw reads')
    #parser.add_argument('-a', '--assembler', default = [], help='use this to pass the list of assemblers to run on, possible options: SPAdes, ABYss, masuRCA, Velvet')
    parser.add_argument('-S', '--spades', action='store_true', help='Spades flag, use this flag to run spades (average run time per sample:)')
    parser.add_argument('-K', '--skesa', action='store_true', help='SKESA flag, use this flag to run skesa (average run time per sample)')
    parser.add_argument('-I', '--idba', action='store_true', help='IDBA flag, use this flag to run IDBA (average run time per sample)')
    parser.add_argument('-A', '--abyss', action='store_true', help='ABYSS flag, use this flag to run ABYSS (average run time per sample)')
    parser.add_argument('-l', '--logging', action='store_true', help='Logging flag')
    
    #dir_path = '/home/abharadwaj61/data'
    
    args = parser.parse_args()
    dir_path = args.input
    logging_enabled = args.logging
    spades_flag, skesa_flag, idba_flag, abyss_flag = args.spades, args.skesa, args.idba, args.abyss
    
    #print(spades_flag, skesa_flag, idba_flag, abyss_flag)
    
	#create home directory based on input given and force create all the directories
    home_dir = str('/'.join(dir_path.split('/')[:-1])) + '/'
    assembly_dir = home_dir +'assemblies'
    
    #fastqc output dir
    qc_output_dir = home_dir +'fastqc'
    
    #fastp trimming output directories
    trimmed_output_dir = home_dir +'trimmed'
    multiqc_op_path = home_dir +'multiqc'
    trimmed_multiqc_op_path = home_dir +'trim_multiqc'
    
    #assembly output directories
    spades_assembly_dir = home_dir +'assembly/spades'
    skesa_assembly_dir = home_dir +'assembly/skesa'
    idba_assembly_dir = home_dir +'assembly/idba'
    abyss_assembly_dir = home_dir +'assembly/abyss'

    #assembly contig directories
    spades_assembly_contigs_dir = home_dir +'assembly/spades/contigs'
    skesa_assembly_contigs_dir = home_dir +'assembly/skesa/contigs'
    idba_assembly_contigs_dir = home_dir +'assembly/idba/contigs'
    abyss_assembly_contigs_dir = home_dir +'assembly/abyss/contigs'
    
    #quast output directories
    spades_quast_dir = home_dir +'quast/spades'
    skesa_quast_dir = home_dir +'quast/skesa'
    idba_quast_dir = home_dir +'quast/idba'
    abyss_quast_dir = home_dir +'quast/abyss'
    
    dir_list = [assembly_dir, qc_output_dir, trimmed_output_dir, multiqc_op_path, trimmed_multiqc_op_path, spades_assembly_dir, skesa_assembly_dir, idba_assembly_dir, abyss_assembly_dir, spades_assembly_contigs_dir, skesa_assembly_contigs_dir, idba_assembly_contigs_dir, abyss_assembly_contigs_dir, spades_quast_dir, abyss_quast_dir, skesa_quast_dir, idba_quast_dir ]
    if logging_enabled:
        print('[+] creating the directory structure to store the results')
    create_dirs(dir_list)

    if logging_enabled:
        print('[+] creating a dictionary with all the samples and the path of each pair of reads in the sample')
    files_dict = find_fastq_filenames(dir_path)
    #print(len(files_dict))
    #print(files_dict)
    
    if logging_enabled:
        print('[+] running fastqc on the samples')
    run_fastqc(files_dict, qc_output_dir)
    
    if logging_enabled:
        print('[+] running multiqc on the samples')
    run_multiqc(qc_output_dir, multiqc_op_path)
    
    #qc_dir_path = home_dir +'fastqc' 
    #multiqc_op_path = qc_dir_path + '/' + 'multiqc_output'

    #running the fastp for the reads   
    if logging_enabled:
        print('[+] running fastp trimming on all the reads uploaded')
    run_fastp(files_dict, trimmed_output_dir)

    if logging_enabled:
        print('[+] running multiqc on the trimmed reads')
    run_multiqc(trimmed_output_dir, trimmed_multiqc_op_path)

    #some kind of validation need here between the two multiqc's right?
        
    #read the trimmed files to run with the assemblers
    trimmed_reads_dict = find_trimmed_filenames(trimmed_output_dir)

    #check the flag for the assemblers and call the functions for each of the assemblers
    if spades_flag:
        if logging_enabled:
            print('[+] Initiating the SPAdes assembler!!')
        run_spades(trimmed_reads_dict, spades_assembly_dir)
    
    if skesa_flag:
        if logging_enabled:
            print('[+] running the SKESA assembler')
        run_skesa(trimmed_reads_dict, skesa_assembly_dir)

    if idba_flag:
        if logging_enabled:
            print('[+] running the IDBA assembler')
        run_idba(trimmed_reads_dict, idba_assembly_dir)
    
    if abyss_flag:
        if logging_enabled:
            print('[+] running the ABYSS assembler')
        run_abyss(trimmed_reads_dict, abyss_assembly_dir)

    #moving all the contigs to the contig directories
    move_contigs(spades_assembly_dir, spades_assembly_contigs_dir)
    move_contigs(skesa_assembly_dir, skesa_assembly_contigs_dir)
    move_contigs(abyss_assembly_dir, abyss_assembly_contigs_dir)
    move_contigs(idba_assembly_dir, idba_assembly_contigs_dir)
    
    #quast implementation based on flag values. 
    if spades_flag:
        if logging_enabled:
            print('[+] running quast on the assemblies from SPAdes')
        run_quast(spades_assembly_contigs_dir, spades_quast_dir )


    if skesa_flag:
        if logging_enabled:
            print('[+] running quast on the assemblies from SPAdes')
        run_quast(skesa_assembly_contigs_dir, skesa_quast_dir )


    if idba_flag:
        if logging_enabled:
            print('[+] running quast on the assemblies from SPAdes')
        run_quast(ibda_assembly_contigs_dir, ibda_quast_dir )

    if abyss_flag:
        if logging_enabled:
            print('[+] running quast on the assemblies from SPAdes')
        run_quast(abyss_assembly_contigs_dir, abyss_quast_dir)







