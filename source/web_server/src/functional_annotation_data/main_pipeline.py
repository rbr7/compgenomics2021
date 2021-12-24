#!/usr/bin/env python3

# -*- encoding: utf-8 -*-

# Standard Imports
import os
import time
import subprocess
import tempfile
import csv
import optparse
from os import path


#clustering with USearch
def comp_cluster(fpath,filelist, identity, u_path, output_path):
    """
	with open(fpath + "/all.faa", "wb") as fh:
    		for file in filelist:
			with open(fpath+"/"+file, "rb") as rh:
        			for line in rh:
					if line.startswith(">"):
                				tag = ">"+file+line[1:]
                				fh.write(tag)
                			else:
						fh.write(line)
				#rh.close()

    		#fh.close()
    """
    #sample commands to execute the tool ->>
    # path_to_usearch -cluster_fast temp/all.cfinal.faa -id 0.97 -centroids temp/centroids.fa -uc temp/label_seq.fa
    # (for amino acids file) path_to_usearch -cluster_fast temp/all.cfinal.faa -id 0.9 -centroids temp/centroids.fa -uc temp/label_seq.fa
    if not os.path.exists(output_path+"clust/"):
        os.mkdir(output_path+"clust/")
    
    for fil in filelist:
        run_cmd = [u_path, "-cluster_fast", fpath+fil, "-id", str(identity),"-centroids",output_path+"clust/"+"centroids.fasta","-uc",output_path+"clust/"+"label_seq.fa"]  
        subprocess.call(run_cmd)
    print("done")

# tool : Phobius 
def comp_phobius(toolx_path,file_path,output_path,file_list):
    #
    if os.path.exists(file_path):
        # ->>
        for fil in file_list:
            print(fil)
            if fil.endswith(".faa") or fil.endswith(".fasta"):
                print(fil)
                os.system(f"sed -i 's/*//g' {file_path}/{fil}")
                nam , extension = path.splitext(fil)
                if not os.path.exists(output_path+"phb/"):
                    os.mkdir(output_path+"phb/")
                #run_cmd = ["perl ",toolx_path," -short ",file_path+fil," > ",output_path+"phb/"+nam+".out"]
                print(run_cmd)
                os.system("perl "+toolx_path+" -short "+file_path+fil+" > "+output_path+"phb/"+nam+".out")
                #subprocess.call(run_cmd)
                print('ye')
            else:
                continue
    else:
        print("input fasta file for the sequence is missing!!")

    

# tool : InterproScan
def comp_interproscan(toolx_path,centroid_file,output_path):
    #
    #
    if os.path.exists(centroids_file):
        # sample ->> ./interproscan.sh -i /home/team2/03.functional.annotation/rb_clustering/clust_faa/faa_fmt/xyz.faa -f gff3 -o results/xyz.gff  
        run_cmd = [toolx_path," -i ",centroid_file," -f gff3"," -o ",output_path]
        subprocess.call(run_cmd)
    else:
        print("fasta file for the clustered data/centroids is missing!!")

# tool : Deeparg
def comp_deeparg(toolx_path, centroid_file,output_path,file_list,seq_type):
    #
    if os.path.exists(centroid_file):
        for fil in file_list:
            print(fil)
            if fil.endswith(".fa"):
                print(fil)
                nam , extension = path.splitext(fil)
                if not os.path.exists(output_path+"deeparg/"):
                    os.mkdir(output_path+"deeparg/")
        #deeparg predict --model [SS or LS] --type [nucl or prot] --input /path/file.fasta --out /path/filename
                run_cmd= ["deeparg predict", "--model", "SS", "--type", seq_type, "--input", centroid_file, "--output", output_path+"deeparg/"+centroid_file]
                subprocess.call(run_cmd)
            else:
                continue
    else:
        print("fasta file for the clustered data/centroids is missing!!")
        
# tool : CRT
def comp_crt(toolx_path,file_path,output_path,file_list):
    #
    if os.path.exists(file_path):
        #
        for fil in file_list:
            print(fil)
            if fil.endswith(".faa") or fil.endswith(".fasta"):
                print(fil)
                nam , extension = path.splitext(fil)
                if not os.path.exists(output_path+"crt/"):
                    os.mkdir(output_path+"crt/")
                
                run_cmd=["java","-cp",toolx_path,"crt",file_path+"/"+fil,output_path+"crt/"+nam+".txt"]
                print(run_cmd)
                subprocess.call(run_cmd)
                print('done cr')
            else:
                continue
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
def comp_signalP(toolx_path,file_path,output_path):
    #
    if os.path.exists(file_path):
        #
        #run_cmd = [toolx_path,"-fasta",file_path+"/CGT1009.final.fna","-org gram- -gff3 -format short"]
        print('\n\n',toolx_path)
        if not os.path.exists(output_path+"sigp/"):
            os.mkdir(output_path+"sigp/")
        
        os.system(f"cd "{output_path}sigp/";signalp -fasta " + file_path + "/euk10.fsa" + " -org gram- -gff3 -format short")
        print('done with h')
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

def comp_vfdb(toolx_path,file_path,output_path,file_list):
    #
    if os.path.exists(file_path):
        #
        #run_cmd = [toolx_path,"-fasta",file_path+"/CGT1009.final.fna","-org gram- -gff3 -format short"]
        #print('\n\n',toolx_path)
        for fil in file_list:
            print(fil)
            if fil.endswith(".faa") or fil.endswith(".fasta"):
                print(fil)
                nam , extension = path.splitext(fil)
                if not os.path.exists(output_path+"VFDB/"):
                    os.mkdir(output_path+"VFDB/")
                cal = "blastp -db "+toolx_path+" -query "+file_path+fil+" -outfmt 6 > "+output_path+"VFDB/"+nam+"_out.txt"
                print(cal)
                os.system(cal)
                os.system("python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/fa_env/blast2gff.py -b "+output_path+"VFDB/"+nam+"_out.txt"+" > "+output_path+"GFF/"+nam+"_vfdb.gff")
                print('done with h')
            else:
                continue
    else:
        print("fasta file for the input data is missing!!")

def comp_oprdb(toolx_path,file_path,output_path,file_list):
    #
    if os.path.exists(file_path):
        #
        #run_cmd = [toolx_path,"-fasta",file_path+"/CGT1009.final.fna","-org gram- -gff3 -format short"]
        #print('\n\n',toolx_path)
        for fil in file_list:
            print(fil)
            if fil.endswith(".faa") or fil.endswith(".fasta"):
                print(fil)
                nam , extension = path.splitext(fil)
                if not os.path.exists(output_path+"OPR/"):
                    os.mkdir(output_path+"OPR/")

                os.system("blastp -db "+toolx_path+" -query "+file_path+fil+" -outfmt 6 > "+output_path+"OPR/"+nam+"_out.txt")
                os.system("python3 /projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/fa_env/blast2gff.py -b "+output_path+"OPR/"+nam+"_out.txt"+" > "+output_path+"GFF/"+nam+"_operon.gff")
                print('done with h')
            else:
                continue
    else:
        print("fasta file for the input data is missing!!")
    
# method : accepts user input values/parameters for running functional annotation methods
def prog_opts():
    parser = optparse.OptionParser()
    parser.add_option('-I',"--input_dir",dest="files")
    parser.add_option('-i','--iden',default = 0.97,dest="clust_idtny",help="cluster identity value")
    parser.add_option('-U',"--usearch_path",dest="usearch_path",help="uSearch absolut path")
    #parser.add_option("-N", "--interproscan", dest="ipscan",help = "interproscan abs path")
    parser.add_option("-b", "--phobius",dest='phbs',help='phobius abs path')
    parser.add_option("-d", "--deeparg",dest="deeparg",help = 'deeparg abs path')
    parser.add_option('-c','--CRT',dest='crt',help='crt abs path')
    #parser.add_option('-k','--plasmid_seeker',dest='plmd',help='plasmid seeker abs path')
    parser.add_option('-O',"--output_dir",dest="outputpath",help = "output file dir path")
    parser.add_option("-p","--signalp", dest="signP", help = "signalP path")
    parser.add_option("-s","--seq_type", dest="itype", help = "input type")
    parser.add_option("-F","--filelist", dest="filest", help = "files list")
    parser.add_option("-a","--run_all", dest="runall", help = "run all methods")
    parser.add_option("-V","--vfdb", dest="vfdb", help = "vfdb db path")
    parser.add_option("-r","--opr", dest="operon", help = "operon db path")
    
    return(parser.parse_args()) 

# main method : for running the functional annotation pipeline.
def run_main():
    # accept user inputs and then run separate programs accordingly
    options, args = prog_opts()
    file_path = options.files
    clust_identity = 0.97 #options.clust_idtny
    os.chdir(file_path)
    if not os.path.exists('fasta_files'):
        os.makedirs('fasta_files')

    if not os.path.exists('result_files'):
        os.makedirs('result_files')
    
    subprocess.call('mv *.fasta fasta_files', shell=True)

    file_path2 = file_path+"fasta_files"
    input_files = os.listdir(file_path2)
    uSearch = "/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/fa_env/usearch11.0.667_i86linux32" #options.usearch_path
    # /home/kavi/Documents/spr/b7210/webserver/Team2-WebServer/django/genome_assembly/functional_annotation/fa_env/usearch11.0.667_i86linux32
    phobis = "/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/fa_env/phobius101_linux/tmp/tmpwUrHn8/phobius/phobius.pl"#options.phbs
    # /home/kavi/Documents/spr/b7210/webserver/Team2-WebServer/django/genome_assembly/functional_annotation/fa_env/phobius101_linux/tmp/tmpwUrHn8/phobius/phobius.pl
    crt = "/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/fa_env/CRT1.2-CLI.jar" #options.crt
    # /home/kavi/Documents/spr/b7210/webserver/Team2-WebServer/django/genome_assembly/functional_annotation/fa_env/CRT1.2-CLI.jar
    #interpro = options.ipscan
    #deeparg = "" #options.deeparg
    # 
    #sigP = #options.signP
    # /home/kavi/Documents/spr/b7210/webserver/Team2-WebServer/django/genome_assembly/functional_annotation/fa_env/signalp-5.0b/bin/signalp
    out = file_path+"result_files/"
    #options.outputpath
    seq = "prot" #options.itype
    #filelist = options.filest
    vfd = "/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/fa_env/VFDB/VFDB_setB_pro.fas"#options.vfdb
    # /home/kavi/Documents/spr/b7210/webserver/Team2-WebServer/django/genome_assembly/functional_annotation/fa_env/VFDB/VFDB_setB_pro.fas
    oprn = "/projects/team-2/abharadwaj61/django/predictivewebserver/genome_assembly/functional_annotation/fa_env/db_operon/database/db_opr" #options.operon
    # /home/kavi/Documents/spr/b7210/webserver/Team2-WebServer/django/genome_assembly/functional_annotation/fa_env/db_operon/database/db_opr.pdb

    if uSearch:
        comp_cluster(file_path2,input_files, clust_identity, uSearch, out)
        print("done cluster")
    #if sigP:
    #    comp_signalP(sigP, file_path, out)
    #    print("done signalP")
    #comp_plasmidseeker(file_path)
    #print(crt)
    if crt:
        ifiles = out+"clust"
        comp_crt(crt,ifiles,out,["centroids.fasta"])
        print("done crt")

    #if deeparg:
    #    comp_deeparg(deeparg,file_path,out,input_files,seq_type=seq)
    #    print("done deeparg")
    #comp_interproscan(interpro,file_path,out)
    #print("done signalP")
    if phobis:
        comp_phobius(phobis,file_path2,out,input_files)
        print("done phobius")
    
    if vfd:
        ifiles = out+"clust"
        comp_vfdb(vfd,ifiles,out,["centroids.fasta"])
        print("done vf")
    
    if oprn:
        ifiles = out+"clust"
        comp_oprdb(oprn,ifiles,out,["centroids.fasta"])
        print("done vf")
    

if __name__ == "__main__":
    run_main()
