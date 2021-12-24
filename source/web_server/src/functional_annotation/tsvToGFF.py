#!/usr/bin/env python2

import os
import subprocess
import optparse
#import argparse

## format output to gff
outputfilepath = 'deeparg/deepargOutputs.align.daa.tsv'
annotate_list = []
with open(outputfilepath, 'r') as fh:
      for line in fh.readlines()[4:-3]:
          line = line.strip()
          line = line.split("\t")
          query_name = line[0]
          ##this is the ortholog score
          ##if we want to include the e-value then we need line[2]
          score = line[10]
          ## antibiotic resistance gene info
          antibiotic_info = line[1]
          annotate_list.append([query_name, score, antibiotic_info])
  ### assign to seqid of centroid
# print(len(annotate_list))

countDict = {}

for i in range(len(annotate_list)):
        x = annotate_list[i]
        print(countDict)
        query_name = x[0]
        ran = query_name.split('_')
        # print(ran)
        start = ran[-2]
        stop = ran[-1]

        print(ran[0])
        gfffile = ran[0] + '_deeparg_output.gff'

        
        if os.path.isfile(gfffile):
            print(countDict[ran[0]])
            newCount = countDict.get(ran[0]) + 1
            countDict[ran[0]] = newCount
            # fh1 = open(gfffile, 'a')
            # l = query_name + "\t" + "DeepARG" + "\t" + "." + "\t" + start + \
            # "\t" + stop + "\t" + str(x[1]) + "\t"+"."+"\t"+"."+"\t" + str(x[2])
            # fh1.write(l + '\n')
        else:
            countDict[ran[0]] = 1
            print(countDict)
            fh1 = open(gfffile, 'w+')
            fh1.write("##gff-version file" + "\n")
            fh1.write("seqid" + '\t' + "source" + "\t" + "type"+"\t"+"start"+"\t" + \
                      "end"+"\t"+"score"+"\t"+"strand"+"\t"+"phase"+"\t"+"attributes"+"\n")
            l = query_name + "\t" + "DeepARG" + "\t" + "." + "\t" + start + \
            "\t" + stop + "\t" + str(x[1]) + "\t"+"."+"\t"+"."+"\t" + str(x[2])
            fh1.write(l + '\n')
