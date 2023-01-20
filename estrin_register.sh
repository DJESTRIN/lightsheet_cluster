#!/bin/bash
# This script is currently not automated 

# Remember to first edit the following variables:
# atlas oreintation
# orientation
# rotation
# translation
# fixed scale

# THEN run an interactive slurm session with GPU: 
#srun --job-name=registration --mem=200G --parition=scu-gpu,sackler-gpu --gres=gpu:2 --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu 
#screen
#bash ./estrin_register.sh input output


#Variables passed from previous script
input_path=$1
output_path=$2

source ~/.bashrc
module load matlab
conda activate cloudreg
cd ~/CloudReg
python3 -m cloudreg.scripts.registration -input_s3_path file://$input_path --output_s3_path file://$output_path -log_s3_path file://$output_path --atlas_s3_path https://open-neurodata.s3.amazonaws.com/ara_2016/sagittal_50um/average_50um --parcellation_s3_path https://open-neurodata.s3.amazonaws.com/ara_2016/sagittal_10um/annotation_10um_2017 --atlas_orientation ASR -orientation LPS --rotation 5 0 23 --translation 0 0 0 --fixed_scale 0.9 --missing_data_correction True --grid_correction False --bias_correction True --regularization 5000.0 --iterations 3000 --registration_resolution 100
