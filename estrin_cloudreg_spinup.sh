#!/bin/bash
#Passed variables from previous script
code_directory=$1
scratch_directory=$2
store_finish_directory=$3

# Create folder for terastitcher output
scratch_stitch=${scratch_directory}"lightsheet/stitched/"
scratch_cloudreg=${scratch_directory}"lightsheet/cloudreg/"
mkdir -p $scratch_cloudreg

#Update sample list (in the case of any issues)
cd $code_directory

# Calculate precomputed volumes for each sample
for sample in $scratch_stitch*/
do
	TMP=$(echo $sample)
	
	for channel in $sample*/
	do
		sbatch --job-name=precomputed_volume --mem=80G --partition=sackler-gpu --gres=gpu:1 --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash ./estrin_cloudreg.sh '$channel' '$scratch_directory'"
	done
done

#Send raw and destriped data back to storage
sbatch --mem=5G --partition=scu-cpu --dependency=singleton --job-name=precomputed_volume --wrap="bash send_back.sh '$code_directory' '$scratch_directory' '$store_finish_directory'"

exit


