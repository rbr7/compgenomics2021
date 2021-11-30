#!/bin/bash

for i in *_r1.fq ; do
	sid=$(basename $i _r1.fq)
	fq2fa --merge --filter $i ${sid}_r2.fq ${sid}.fa
done
