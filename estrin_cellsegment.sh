#!/bin/bash
sample_directory=$1
code_directory=$2

source ~/.bashrc
conda activate new_cell_counting
module load cuda

cd $code_directory
python ./cellsegmentation.py --lifecanvas_code_directory /home/dje4001/LIGHTSHEET_CLUSTER/SA_files/ --sample_directory $sample_directory


