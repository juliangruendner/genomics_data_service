FROM openjdk:8
ARG nodata
LABEL maintainer="Nicolas Wolf <nicolas.wolf@fau.de>"

# RUN DEBIAN_FRONTEND=noninteractive
# RUN apt-get update -y
# RUN apt-get install -y apt-utils build-essential less wget gzip bzip2 git tabix bedtools autoconf pkg-config libpng-dev zlib1g-dev unzip python2.7 python-pip python-dev python3 python3-pip libbz2-dev liblzma-dev libcurl3-dev libssl-dev libgsl0-dev

# RUN mkdir /usr/local/share/ref_file
# WORKDIR /usr/local/share/ref_file
# COPY ref_file/fasta_conv.py .
# COPY ref_file/get_ref_file.sh .
# RUN if [ "$nodata" = "" ] ; then ./get_ref_file.sh ; fi

# WORKDIR /usr/src/snpeff

# RUN wget http://sourceforge.net/projects/snpeff/files/snpEff_latest_core.zip && \
#     unzip snpEff_latest_core.zip

# WORKDIR /usr/src

# RUN git clone https://github.com/vcftools/vcftools.git && \
#     cd vcftools && \
#     ./autogen.sh && \
#     ./configure && \
#     make && \
#     make install

# WORKDIR /usr/src

# RUN git clone git://github.com/samtools/htslib.git && \
#     git clone git://github.com/samtools/bcftools.git && \
#     cd bcftools && \
#     make && \
#     make install

# WORKDIR /usr/src

# RUN git clone https://github.com/atks/vt.git && \
#     cd vt && \
#     make && \
#     make test

WORKDIR /usr/src/app

# RUN pip install pybedtools
# RUN wget https://raw.github.com/arq5x/gemini/master/gemini/scripts/gemini_install.py -P /usr/tmp/
# RUN mkdir /usr/local/share/gemini
# RUN python2 /usr/tmp/gemini_install.py ${nodata} /usr/local /usr/local/share/gemini

RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD uwsgi --ini uwsgi.ini