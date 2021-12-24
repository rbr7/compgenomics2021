import argparse
import os
import subprocess
import run_tools

parser=argparse.ArgumentParser()
parser.add_argument('-i',nargs='+')
parser.add_argument('-d')
parser.add_argument('-m',default=1.0)
parser.add_argument('-b')
parser.add_argument('-p',default=90)
parser.add_argument('-f')

args=parser.parse_args()

files=args.i
diamond_db=args.d
min_overlap=args.m
blast_db=args.b
min_pident=args.p
infernal_db=args.f

comm='diamond makedb --in ' + diamond_db + ' -d ' + diamond_db
subprocess.call(comm,shell=True)
comm='makeblastdb -in ' + blast_db + ' -dbtype prot'
subprocess.call(comm,shell=True)
if not os.path.isfile(infernal_db+'.i1i'):
	comm='cmpress ' + infernal_db
	subprocess.call(comm,shell=True)

for path in files:
	path_toks=path.split('/')
	filename=path_toks[-1]
	filename_toks=filename.split('.')
	subject=filename_toks[0]
	subject_dirpath='/'.join(path_toks[0:-1])
	subject_dirpath=subject_dirpath+'/genepredictionresults'
	if not os.path.isdir(subject_dirpath):
		os.mkdir(subject_dirpath)
	subject_dirpath=subject_dirpath+'/'+subject
	if not os.path.isdir(subject_dirpath):
		os.mkdir(subject_dirpath)
		
	final_output_path=subject_dirpath+'/'+'finaloutputs'
	if not os.path.isdir(final_output_path):
		os.mkdir(final_output_path)
	
	prodigal_path=run_tools.run_prodigal(subject,path,subject_dirpath)
	gms2_path=run_tools.run_gms2(subject,path,subject_dirpath)
	prdgms2intersect_path=run_tools.bedtools_intersect(min_overlap,subject,prodigal_path,gms2_path,subject_dirpath,'prdgms2intersect',False)
	abinitiocoding_path=run_tools.run_blast(blast_db,min_pident,path,subject,prdgms2intersect_path,subject_dirpath,'abinitiocoding')
	diamond_path=run_tools.run_diamond(diamond_db,subject,path,subject_dirpath)
	diamondonly_path=run_tools.bedtools_intersect(min_overlap,subject,diamond_path,abinitiocoding_path,subject_dirpath,'diamondonly',True)
	codingmerged_path=run_tools.merge(subject,abinitiocoding_path,diamondonly_path,subject_dirpath,'codingmerged')
	coding_path=run_tools.bedtools_sort(subject,codingmerged_path,subject_dirpath,'coding')
	
	aragorn_path=run_tools.run_aragorn(subject,path,subject_dirpath)
	barrnap_path=run_tools.run_barrnap(subject,path,subject_dirpath)
	infernal_path=run_tools.run_infernal(subject,path,subject_dirpath)
	arabarmerged_path=run_tools.merge(subject,aragorn_path,barrnap_path,subject_dirpath,'arabarmerged')
	arabarsorted_path=run_tools.bedtools_sort(subject,arabarmerged_path,subject_dirpath,'arabarsorted')
	infernalonly_path=run_tools.bedtools_intersect(min_overlap,subject,infernal_path,arabarsorted_path,subject_dirpath,'infernalonly',True)
	noncodingmerged_path=run_tools.merge(subject,arabarsorted_path,infernalonly_path,subject_dirpath,'noncodingmerged')
	noncoding_path=run_tools.bedtools_sort(subject,noncodingmerged_path,subject_dirpath,'noncoding')
	
	codingnoncoding_path=run_tools.merge(subject,coding_path,noncoding_path,subject_dirpath,'codingnoncoding')
	final_path=run_tools.bedtools_sort(subject,codingnoncoding_path,subject_dirpath,'final')
	
	coding_path,coding_getfasta_path=run_tools.naming(subject,coding_path,subject_dirpath,'coding')
	final_path,final_getfasta_path=run_tools.naming(subject,final_path,subject_dirpath,'final')
	coding_fna_path=run_tools.bedtools_getfasta(path,subject,coding_getfasta_path,subject_dirpath,'coding')
	final_fna_path=run_tools.bedtools_getfasta(path,subject,final_getfasta_path,subject_dirpath,'final')
	
	coding_faa_path=run_tools.transeq(subject,coding_fna_path,subject_dirpath,'coding')
	coding_faa_path=run_tools.filter_faa(coding_path,coding_faa_path)
	
	comm1='mv '+final_path+' '+final_output_path
	comm2='mv '+final_fna_path+' '+final_output_path
	comm3='mv '+coding_faa_path+' '+final_output_path
	subprocess.call(comm1,shell=True)
	subprocess.call(comm2,shell=True)
	subprocess.call(comm3,shell=True)
	
	comm='rm '+subject_dirpath+'/*.*'
	subprocess.call(comm,shell=True)
	comm='mv '+final_output_path+'/* '+subject_dirpath
	subprocess.call(comm,shell=True)
	comm='rmdir '+final_output_path
	subprocess.call(comm,shell=True)

