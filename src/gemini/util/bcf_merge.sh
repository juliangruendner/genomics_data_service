#!/bin/sh
first_arg=$1
shift
second_arg=$1
shift
bcftools merge $@ -F $second_arg -o $first_arg