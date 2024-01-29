#!/bin/bash
file=$1
source ~/.bashrc
conda activate spyder-env
python /athena/listonlab/scratch/dje4001/lightsheet_cluster/ilastik_thresholding_analysis.py --syglass_file $file
