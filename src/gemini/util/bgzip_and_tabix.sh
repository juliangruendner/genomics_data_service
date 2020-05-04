#!/bin/sh
bgzip < $1 > $1.gz
tabix -p vcf $1.gz