import subprocess

def run_prodigal(subject,inpath,outpath):
	comm='prodigal -q -i ' + inpath + ' -d ' + outpath + '/' + subject + '.prodigal.fnn' + ' -f gff -o ' + outpath + '/' + subject + '.prodigal.gff'
	subprocess.call(comm,shell=True)
	prodigal_path=outpath + '/' + subject + '.prodigal.gff'
	return prodigal_path
	
def run_gms2(subject,inpath,outpath):
	comm='~/geneprediction/Tools/genemarks2/gms2.pl -seq ' + inpath + ' -genome-type bacteria -output ' + outpath + '/' + subject + '.gms2.gff -format gff -fnn ' + outpath + '/' + subject + '.gms2.fnn'
	subprocess.call(comm,shell=True)
	gms2_path=outpath + '/' + subject + '.gms2.gff'
	return gms2_path

def run_aragorn(subject,inpath,outpath):
	comm='aragorn -t -l -gc1 -w -o ' + outpath + '/' + subject + '.aragorn.out ' + inpath
	comm2='~/geneprediction/Tools/cnv_aragorn2gff.pl -i ' + outpath + '/' + subject + '.aragorn.out -o ' + outpath + '/' + subject + '.aragorn.gff'
	subprocess.call(comm,shell=True)
	subprocess.call(comm2,shell=True)
	aragorn_path=outpath + '/' + subject + '.aragorn.gff'
	return aragorn_path

def run_barrnap(subject,inpath,outpath):
	comm='barrnap --quiet ' + inpath + ' > ' + outpath + '/' + subject + '.barrnap.gff'
	subprocess.call(comm,shell=True)
	barrnap_path=outpath + '/' + subject + '.barrnap.gff'
	return barrnap_path

def run_infernal(subject,inpath,outpath):
	comm='~/geneprediction/Code/infernal.sh -s ' + subject + ' -i ' + inpath + ' -o ' + outpath
	subprocess.call(comm,shell=True)
	infernal_path=outpath + '/' + subject + '.infernal.gff'
	line_list=[]
	with open(infernal_path,'r') as fh:
		for line in fh:
			geneid=line.split('\t')[2]
			if 'tRNA' in geneid:
				line_list.append(line)
			elif 'rRNA' in geneid:
				line_list.append(line)
	with open(infernal_path,'w') as oh:
		for line in line_list:
			oh.write(line)

	keeplines=[]
	keepinds=[]
	with open(infernal_path,'r') as fh:
		line1=fh.readline()
		line1=line1.split('\t')
		keeplines.append(line1)
		keepinds.append((line1[0],line1[3],line1[4]))
		for line in fh:
			line=line.split('\t')
			currind=(line[0],line[3],line[4])
			if currind not in keepinds:
				keepinds.append(currind)
				keeplines.append(line)
	with open(infernal_path,'w') as oh:
		for line in keeplines:
			line='\t'.join(line)
			oh.write(line)
	return infernal_path

def run_diamond(db,subject,inpath,outpath):
	comm='~/geneprediction/Code/diamond.sh -d ' + db + ' -s ' + subject + ' -i ' + inpath + ' -o ' + outpath
	subprocess.call(comm,shell=True)
	diamond_path=outpath + '/' + subject + '.diamond.gff'
	
	keeplines=[]
	keepinds=[]
	with open(diamond_path,'r') as fh:
		line1=fh.readline()
		line1=line1.split('\t')
		keeplines.append(line1)
		keepinds.append((line1[0],line1[3],line1[4]))
		for line in fh:
			line=line.split('\t')
			currind=(line[0],line[3],line[4])
			if currind not in keepinds:
				keepinds.append(currind)
				keeplines.append(line)
	with open(diamond_path,'w') as oh:
		for line in keeplines:
			line='\t'.join(line)
			oh.write(line)

	seq_dict={}
	line_num=1
	line_list=[]
	with open(diamond_path,'r') as fh:
		for line in fh:
			line_list.append(line)
			line=line.strip()
			line=line.split('\t')
			node_info=line[0].split('_')
			node_num=node_info[1]
			if node_num in seq_dict.keys():
				seq_dict[node_num][line_num]=(line[3],line[4],line[5])
			else:
				seq_dict[node_num]={}
				seq_dict[node_num][line_num]=(line[3],line[4],line[5])
			line_num+=1
	keeplines=[]
	for node in seq_dict.keys():
		keys=list(seq_dict[node].keys())
		overlap_sets=[[keys[0]]]
		for key in keys[1:]:
			for overlap_set in overlap_sets:
				overlap_list=[]
				for possible_overlap in overlap_set:
					start1=int(seq_dict[node][key][0])
					stop1=int(seq_dict[node][key][1])
					start2=int(seq_dict[node][possible_overlap][0])
					stop2=int(seq_dict[node][possible_overlap][1])
					if min(stop1,stop2)-max(start1,start2)>0:
						overlap_list.append(1)
					else:
						overlap_list.append(0)
				if 1 in overlap_list:
					overlap_set.append(key)
			any_sets=[]
			for overlap_set in overlap_sets:
				if key in overlap_set:
					any_sets.append(1)
				else:
					any_sets.append(0)
			if 1 not in any_sets:
				overlap_sets.append([key])
		for overlap_set in overlap_sets:
			scores=[]
			for gene in overlap_set:
				scores.append(float(seq_dict[node][gene][2]))
			ind=scores.index(max(scores))
			keepline=overlap_set[ind]
			keeplines.append(keepline)
	with open(diamond_path,'w') as oh:
		for ind in keeplines:
			oh.write(line_list[ind-1])
	return diamond_path

def bedtools_intersect(min_overlap,subject,inpath1,inpath2,outpath,outhandle,is_v):
	if not is_v:
		comm='bedtools intersect -f ' + str(min_overlap) + ' -r -a ' + inpath1 + ' -b ' + inpath2 + ' > ' + outpath + '/' + subject + '.' + outhandle + '.gff'
	else:
		comm='bedtools intersect -v -r -a ' + inpath1 + ' -b ' + inpath2 + ' > ' + outpath + '/' + subject + '.' + outhandle + '.gff'
	subprocess.call(comm,shell=True)
	intersect_path=outpath + '/' + subject + '.' + outhandle + '.gff'
	return intersect_path

def run_blast(db,min_pident,fasta_inpath,subject,inpath,outpath,outhandle):
	comm='bedtools getfasta -fi ' + fasta_inpath + ' -bed ' + inpath + ' -fo ' + outpath + '/' + subject + '.blastx.fasta'
	comm2='blastx -db ' + db + ' -query ' + outpath + '/' + subject + '.blastx.fasta' + ' -out ' + outpath + '/' + subject + '.blastx.out -outfmt 6 -max_target_seqs 1'
	comm3='python3 gff_purge.py -b ' + outpath + '/' + subject + '.blastx.out -g ' + inpath + ' -o ' + outpath + '/' + subject + '.' + outhandle + '.gff -min ' + str(min_pident)
	subprocess.call(comm,shell=True)
	subprocess.call(comm2,shell=True)
	subprocess.call(comm3,shell=True)
	blast_path=outpath + '/' + subject + '.' + outhandle + '.gff'
	return blast_path

def merge(subject,inpath1,inpath2,outpath,outhandle):
	comm='cat ' + inpath1 + ' ' + inpath2 + ' > ' + outpath + '/' + subject + '.' + outhandle + '.gff'
	subprocess.call(comm,shell=True)
	merge_path=outpath + '/' + subject + '.' + outhandle + '.gff'
	return merge_path

def bedtools_sort(subject,inpath,outpath,outhandle):
	comm='bedtools sort -i ' + inpath + ' > ' + outpath + '/' + subject + '.' + outhandle + '.gff'
	subprocess.call(comm,shell=True)
	sort_path=outpath + '/' + subject + '.' + outhandle + '.gff'
	return sort_path

def bedtools_getfasta(fasta_inpath,subject,inpath,outpath,outhandle):
	comm='bedtools getfasta -fi ' + fasta_inpath + ' -bed ' + inpath + ' -fo ' + outpath + '/' + subject + '.' + outhandle + '.fna -nameOnly'
	subprocess.call(comm,shell=True)
	getfasta_path=outpath + '/' + subject + '.' + outhandle + '.fna'
	return getfasta_path

def transeq(subject,inpath,outpath,outhandle):
	comm='transeq -sequence ' + inpath + ' -outseq ' + outpath + '/' + subject + '.' + outhandle + '.faa -table 11 -sformat pearson -frame 6'
	subprocess.call(comm,shell=True)
	transeq_path=outpath + '/' + subject + '.' + outhandle + '.faa'
	return transeq_path

def naming(subject,inpath,outpath,outhandle):
	final_lines=[]
	getfasta_lines=[]
	with open(inpath,'r') as fh:
		for line in fh:
			line=line.strip()
			line=line.split('\t')
			node_info=line[0].split('_')
			node_num=node_info[1]
			tool=line[1]
			genetype=line[2]
			start=line[3]
			stop=line[4]
			name_pieces=[subject,'Node',node_num,tool,genetype,start,stop]
			name='_'.join(name_pieces)
			attributes=line[-1]
			if attributes=='.':
				attributes='Name='+name
			elif attributes[-1]==';':
				attributes=attributes+'Name='+name
			else:
				attributes=attributes+';Name='+name
			final_line=line[0:-1]
			final_line.append(attributes)
			final_line='\t'.join(final_line)
			final_lines.append(final_line)
			line[2]=name
			getfasta_line='\t'.join(line)
			getfasta_lines.append(getfasta_line)

	with open(inpath,'w') as oh:
		oh.write('##gff-version 3\n')
		for line in final_lines:
			oh.write(line+'\n')
	
	forgetfastaonly_path=outpath+'/'+subject+'.forgetfastaonly.'+outhandle+'.gff'
	with open(forgetfastaonly_path,'w') as oh:
		for line in getfasta_lines:
			oh.write(line+'\n')
	return inpath,forgetfastaonly_path

def filter_faa(gffpath,inpath):
	reading_frames=[]
	with open(gffpath,'r') as fh:
		fh.readline()
		for line in fh:
			line=line.split('\t')
			strand=line[6]
			frame=line[7]
			rf=strand+frame
			if rf=='+0':
				rf=1
			elif rf=='+1':
				rf=2
			elif rf=='+2':
				rf=3
			elif rf=='-0':
				rf=4
			elif rf=='-1':
				rf=5
			elif rf=='-2':
				rf=6
			reading_frames.append(rf)

	frame_ind=0
	gene_ind=0
	seq_dict={}
	currseq=''
	with open(inpath,'r') as fh:
		for line in fh:
			line=line.strip()
			if line[0]=='>':
				currseq=line
				frame_ind+=1
				if frame_ind>6:
					gene_ind+=1
					frame_ind=1
				if reading_frames[gene_ind]==frame_ind:
					seq_dict[line]=[]
			else:
				if currseq in seq_dict.keys():
					seq_dict[currseq].append(line)

	with open(inpath,'w') as oh:
		for key in seq_dict:
			oh.write(key+'\n')
			for seq in seq_dict[key]:
				oh.write(seq+'\n')
	return inpath

