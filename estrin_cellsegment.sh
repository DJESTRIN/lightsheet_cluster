#!/bin/bash
code_directory=$1
sample_directory=$2
output_directory=$3

source ~/.bashrc
conda activate new_cell_counting
module load cuda

cd $code_directory
python ./cellsegmentation.py --lifecanvas_code_directory /home/dje4001/LIGHTSHEET_CLUSTER/SA_files/ --input_dir $sample_directory --output_dir $output_directory


