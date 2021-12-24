#!/usr/bin/env python2

# -*- encoding: utf-8 -*-

# Standard Imports
import os
import time
import subprocess
import tempfile
import pandas as pd
import csv
import optparse


# clustering with USearch
def comp_cluster(fpath,filelist, identity, u_path, output_path):
    
    fh = open(output_path + "/all.cfinal.fna","w")
    for file in filelist:
        rh=open(fpath+"/"+file,"r")
        for line in rh:
            if line.startswith(">"):
                tag = ">"+file+line[1:]
                fh.write(tag)
            else:
                fh.write(line)
        rh.close()
    fh.close()

    #sample commands to execute the tool ->>
    # path_to_usearch -cluster_fast temp/all.cfinal.fna -id 0.97 -centroids temp/centroids.fa -uc temp/label_seq.fa
    # (for amino acids file) path_to_usearch -cluster_fast temp/all.cfinal.faa -id 0.9 -centroids temp/centroids.fa -uc temp/label_seq.fa
    run_cmd = [u_path, "-cluster_fast", output_path+"/all.cfinal.fna", "-id", str(identity),"-centroids",output_path+"/centroids.fa","-uc",output_path+"/label_seq.fa"]  
    subprocess.call(run_cmd)
    
# tool : Phobius 
def comp_phobius(toolx_path,file_path,output_path):
    #
    if os.path.exists(file_path):
        # ->>
        run_cmd = ["perl",toolx_path,"-short",file_path,">",output_path+"/result.out"]
        subprocess.call(run_cmd)
    else:
        print("input fasta file for the sequence is missing!!")

    

# tool : InterproScan
def comp_interproscan(toolx_path,centroid_file,output_path):
    #
    #
    if os.path.exists(centroids_file):
        # sample ->> ./interproscan.sh -i /home/team2/03.functional.annotation/rb_clustering/clust_faa/faa_fmt/xyz.faa -f gff3 -o results/xyz.gff  
        run_cmd = [toolx_path,"-i",centroid_file,"-f gff3","-o",output_path]
        subprocess.call(run_cmd)
    else:
        print("fasta file for the clustered data/centroids is missing!!")

# tool : Deeparg
def comp_deeparg(toolx_path, seq_type,centroid_file,output_path):
    #
    if os.path.exists(centroid_file):
        #deeparg predict --model [SS or LS] --type [nucl or prot] --input /path/file.fasta --out /path/filename
        run_cmd= [toolx_path,"predict", "--model", "SS", "--type", seq_type, "--input", centroid_file, "--output", output_path]
        subprocess.call(run_cmd)
    else:
        print("fasta file for the clustered data/centroids is missing!!")
        
# tool : CRT
def comp_crt(toolx_path,file_path,output_path):
    #
    if os.path.exists(file_path):
        #
        run_cmd=["java","-cp",toolx_path,"crt",file_path,output_path]
        subprocess.call(run_cmd)
    else:
        print("fasta file for the input data is missing!!")
        
# tool : PlasmidSeeker 
def comp_plasmidseeker(file_path):
    #
    final_outputs_directory = file_path
    for filename in os.listdir(final_outputs_directory):
        if filename.endswith(".fna"):
            period_index = filename.find(".")
            file_prefix = filename[:period_index]
            os.system("./seqtk/seqtk seq -F '40' " + filename + " > " + file_prefix + "../fastq")

    final_outputs_directory = "../"
    concatenated_prefix = "concatenated"
    concatenated = final_outputs_directory + concatenated_prefix + ".fastq"
    os.system("cat \"\" > " + concatenated)
    for filename in os.listdir(final_outputs_directory):
        if filename.endswith(".fastq"):
            os.system("cat " + final_outputs_directory + filename + " >> " + concatenated)
    os.system("perl plasmidseeker.pl --ponly -d db_w20 -i " + concatenated + " -b e_coli_sakai_ref.fna -o ./Outputs/" + concatenated_prefix + ".txt")

# tool : SignalP
def comp_signalP(toolx_path,file_path):
    #
    if os.path.exists(file_path):
        #
        run_cmd = [toolx_path,"-fasta",file_path,"-org gram- -gff3 -format short"]
    else:
        print("fasta file for the input data is missing!!")

# method : to convert crt outputs to gff format
def crt_gff(dir_path):
    #
    directory = dir_path
    count_list = []

    for entry in os.scandir(directory):
        if entry.is_file() and entry.name.endswith('.txt'):
            tool ="CrisprRecognitionTool"
            typ ="CRISPR"
            score="."
            phase ="."
            attributes = "."
            strand = "."
            data_list = []
            entry_list = []
            file_name_list = entry.name.split("_")
            output_file_name = file_name_list[2] + "_" + file_name_list[0] + "_" + file_name_list[1] + ".gff"
            with open(entry) as f:
                lines = f.readlines()
                for i in lines:
                    data = i.split()
                    data_list.append(data)
                name = data_list[0][1]
                data_list = [ele for ele in data_list if ele != []]
                for i in data_list:  
                    if i[0] == "CRISPR":
                        start = i[3]
                        end = i[5]
                        entry_list.append([start, end])
            with open(output_file_name, 'w') as file:
                file.write("##gff-version 3" + "\n")
            for i in entry_list: 
                with open(output_file_name, 'a') as f:
                    f.write(name + "\t" + tool + "\t" + typ + "\t" + i[0] + "\t" + i[1] + "\t" + score + "\t" + strand + "\t" + phase + "\t" + attributes + "\n")
    f.close()
    
# method : accepts user input values/parameters for running functional annotation methods
def prog_opts():
    parser = optparse.OptionParser()
    parser.add_option('-I',"--input_dir",dest="files")
    parser.add_option('-i','--iden',default = 0.97,dest="clust_idtny",help="cluster identity value")
    parser.add_option('-U',"--usearch_path",dest="usearch_path",help="uSearch absolut path")
    parser.add_option("-N", "--interproscan", dest="ipscan",help = "interproscan abs path")
    parser.add_option("-b", "--phobius",dest='phbs',help='phobius abs path')
    parser.add_option("-d", "--deeparg",dest="deeparg",help = 'deeparg abs path')
    parser.add_option('-c','--CRT',dest='crt',help='crt abs path')
    parser.add_option('-c','--plasmid_seeker',dest='plmd',help='plasmid seeker abs path')
    parser.add_option('-O',"--output_dir",dest="outputpath",help = "output file dir path")
    parser.add_option("-p","--signalp", dest="signP", help = "signalP path")
    parser.add_option("-s","--seq_type", dest="itype", help = "input type")
    parser.add_option("-F","--filelist", dest="filest", help = "files list")
    
    return(parser.parse_args()) 

# main method : for running the functional annotation pipeline.
def main():
    # accept user inputs and then run separate programs accordingly
    options, args = prog_opts()
    file_path = options.files
    clust_identity = options.clust_idtny
    
    input_files = os.listdir(file_path)
    uSearch = options.usearch_path
    phobis = options.phbs
    crt = options.crt
    interpro = options.ipscan
    deeparg = options.deeparg
    sigP = options.signP
    out = options.outputpath
    seq = options.itype
    filelist = options.filest
    
    comp_cluster(file_path,filelist, clust_identity, uSearch, out)
    comp_signalP(sigP, out)
    comp_plasmidseeker(file_path)
    comp_crt(crt,file_path,out)
    comp_deeparg(deeparg, seq_type=seq,file_path,out)
    comp_interproscan(interpro,file_path,out)
    comp_phobius(phobis,file_path,out)
    
    

if __name__ == "__main__":
    main()
