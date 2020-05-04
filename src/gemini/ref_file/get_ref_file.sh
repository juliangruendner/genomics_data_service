wget http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/hg19.2bit
wget http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/twoBitToFa
chmod +x twoBitToFa
./twoBitToFa hg19.2bit hg19.fa
python3 fasta_conv.py hg19.fa hg19_upper.fa
rm hg19.2bit
rm hg19.fa