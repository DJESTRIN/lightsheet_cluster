#!/bin/bash
#Passed variables from previous script
code_directory=$1
scratch_directory=$2
store_finish_directory=$3

scratch_stitch=${scratch_directory}"lightsheet/stitched/"

#Update sample list (in the case of any issues)
cd $code_directory

# Calculate precomputed volumes for each sample
for sample in $scratch_stitch*/
do
        TMP=$(echo $sample)
        echo $TMP
        for channel in $sample*/
        do
        echo $channel
                sbatch --job-name=cellsegmentation --mem=200G --partition=scu-gpu --gres=gpu:1 --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash ./estrin_cellsegment.sh $channel $code_directory"
        done
done
exit


