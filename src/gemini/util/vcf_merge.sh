#!/bin/sh
first_arg=$1
shift
vcf-merge $@ > $first_arg