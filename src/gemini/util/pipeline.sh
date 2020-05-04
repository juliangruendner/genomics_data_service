#!/bin/sh
# decompose, normalize and annotate VCF with snpEff.
# NOTE: can also swap snpEff with VEP
zless --buffers=1048576 -B $1 \
   | sed 's/ID=AD,Number=./ID=AD,Number=R/' \
   | /usr/src/vt/vt decompose -s - \
   | /usr/src/vt/vt normalize -r $2 - \
   | java -Xmx4G -jar $3 GRCh37.75 \
   | bgzip -c > $4
tabix -p vcf $4

# load the pre-processed VCF into GEMINI
gemini load --cores 3 -t snpEff -v $4 $5