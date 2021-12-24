#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import os

def mergeGFF(directory, contig):
  # Assuming all gff files are tab delimited and are in appropriate 9 column format
  with open(contig + '_merged.gff','w') as fh1:
    for filename in os.listdir(directory):
      
      if filename.endswith(".gff") or filename.endswith(".gff3"):

        if filename[0:7] ==  contig:

          with open(directory + '/' + filename,'r') as fh2:
            for line in fh2:

              if line[0:3] == 'CGT':
                print('true')
                fh1.write(line)
                
# Obtaining annotations
def get_gff_annotations(gfffilename):
  gff_dict = {}
  with open(gfffilename, 'r') as fh:
        for line in fh:
          if line[0:3] == 'CGT':
            line = line.strip().split("\t")
            if line[0] not in gff_dict:
              if line[1] == "SignalP-5.0":
                gff_dict.update({line[0]: "|" + line[1]+"|"+line[2]+"|"+line[8]})
              else:
                gff_dict.update({line[0]: "|" + line[1]+"|"+line[8]})
            else:
              if line[1] == "SignalP-5.0":
                gff_dict.update({line[0]: "|" + gff_dict.get(line[0])+"|"+line[1]+"|"+line[2]+"|"+line[8]})
              else:
                gff_dict.update({line[0]: "|" + gff_dict.get(line[0])+"|"+line[1]+"|"+line[8]})

  return gff_dict

          
# Annotating FASTA files (can be done for both .fna and .faa)
def fna_annotation(fastafilename,gff_dict):
  with open(fastafilename+"_fully_annotated.out","w") as fh1:
    with open(fastafilename, 'r') as fh2:
          for line in fh2:
            if line[0] == '>':
              print(line[1:-1])
              if line[1:-1] in gff_dict.keys():
                fh1.write(line[0:-1]+gff_dict.get(line[1:-1])+'\n')
              else:
                fh1.write(line)
            else:
              fh1.write(line)
      
def faa_annotation(fastafilename,gff_dict):
  with open(fastafilename+"_fully_annotated.out","w") as fh1:
    with open(fastafilename, 'r') as fh2:
          for line in fh2:
            if line[0] == '>':
              print(line[1:-3])
              if line[1:-3] in gff_dict.keys():
                fh1.write(line[0:-1]+gff_dict.get(line[1:-3])+'\n')
              else:
                fh1.write(line)
            else:
              fh1.write(line)        
      
