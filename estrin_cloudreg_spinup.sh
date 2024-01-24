#!/bin/bash
#Passed variables from previous script
code_directory=$1
scratch_directory=$2
store_finish_directory=$3

# destriped data no longer needed. Send back to storage
#bash /home/dje4001/lightsheet_cluster/estrin_sendback_spinup.sh $scratch_directory/lightsheet/destriped/ $store_finish_directory destriped

# Create folder for terastitcher output
scratch_stitch=${scratch_directory}"lightsheet/stitched/"
scratch_cloudreg=${scratch_directory}"lightsheet/cloudreg/"
mkdir -p $scratch_cloudreg

#Update sample list (in the case of any issues)
cd $code_directory

# Calculate precomputed volumes for each sample
for sample in $scratch_stitch*/
do

		sbatch --job-name=precomputed_volume --mem=200G --partition=scu-gpu --gres=gpu:2 --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash ./estrin_cloudreg.sh '$sample' '$scratch_directory'"
done

sbatch --mem=5G --partition=scu-cpu --dependency=singleton --job-name=precomputed_volume --wrap="bash estrin_registration_spinup.sh '$code_directory' '$scratch_directory' '$store_finish_directory'"

exit


