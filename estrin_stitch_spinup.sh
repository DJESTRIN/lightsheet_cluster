#!/bin/bash/
#Passed variables from previous script
code_directory=$1
scratch_directory=$2
store_finish_directory=$3

# Create folder for terastitcher output
scratch_stitch=${scratch_directory}"lightsheet/stitched/"
scratch_destriped=${scratch_directory}"lightsheet/destriped/"
mkdir -p $scratch_stitch

#Update sample list (in the case of any issues)
cd $code_directory

# Stitch images using terastitcher
for i in $scratch_destriped*/
do
TMP=$(echo $i)
sbatch --job-name=stitch_files --mem=100G --partition=sackler-gpu --gres=gpu:1 --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash ./estrin_stitch.sh '$TMP' '$scratch_directory'"

done

sbatch --mem=5G --partition=scu-cpu --dependency=singleton --job-name=stitch_files --wrap="bash estrin_cloudreg_spinup.sh '$code_directory' '$scratch_directory' '$store_finish_directory'"

exit
