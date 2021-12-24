#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-b", help="BLASTx results")
parser.add_argument("-g", help="GFF results to clean")
parser.add_argument("-min", help="Minimum percentage identity in BLAST to keep hit on GFF", default=90)
parser.add_argument("-o",help="Output filename/path")

args=parser.parse_args()

blastName=args.b
gffName=args.g
min_pident=int(args.min)
outfile=args.o

## CONVERT FILES TO A LIST OF LIST

with open(blastName) as f:
        blast_results=f.readlines()
blast_results[:]=[line.rstrip('\n') for line in blast_results]
blast_results[:]=[item for item in blast_results if item !='']
blast_results[:]=[line.split('\t') for line in blast_results]

with open(gffName) as f:
    gff_results= f.readlines()
gff_results[:] = [line.rstrip('\n') for line in gff_results]
gff_results[:] = [item for item in gff_results if item != '']
gff_results[:] = [line.split('\t') for line in gff_results]

## DELETES UNNECESSARY COLUMNS IN BLAST RESULTS

for i in blast_results:
    del i[3:12], i[1]

## OLD CODE THAT MIGHT BE USEFUL IF SOMETHING CHANGES IN THE PIPELINE

#blast_results=[i[0].split(':',1)+[i[1]] for i in blast_results]
#blast_results=[[i[0]]+i[1].split('-',1)+[i[2]] for i in blast_results]

blast_results_curated=[]
gff_results_curated=[]

## KEEPS BLAST RESULTS ONLY ABOVE CERTAIN PIDENT

for i in range(len(blast_results)):
    if float(blast_results[i][1])>min_pident:
        blast_results_curated.append(blast_results[i])

## COMPARES KEPT BLAST RESULTS WITH CURRENT GFF. IF MATCH, APPENDS RESULTS TO A NEW LIST

for i in range(len(gff_results)):
    coord_fix=int(gff_results[i][3])-1 ## BLAST is showing 5' one nucleotide before prediction
    check=gff_results[i][0]+":"+str(coord_fix)+'-'+gff_results[i][4]
    if (any(check in sublist for sublist in blast_results_curated)):
        gff_results_curated.append(gff_results[i])

## WRITES INTO FILE

with open(outfile, 'w') as filehandle:
    filehandle.writelines('\t'.join(i) + '\n' for i in gff_results_curated)
