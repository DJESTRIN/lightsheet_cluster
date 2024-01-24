#!/bin/bash
input=$1
scratch_directory=$2

#Set up input and output
base_name=$(basename ${input})
echo Base name = ${base_name}
tag=lightsheet/destriped/
output="$scratch_directory$tag$base_name"
mkdir -p $output

# Call pystripe
source ~/.bashrc
conda activate /home/fs01/dje4001/anaconda3/envs/pystripe2
pystripe -i $input -o $output -s1 256 -s2 65
