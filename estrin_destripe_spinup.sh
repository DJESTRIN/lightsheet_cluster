#!/bin/bash/
#Passed variables from previous script
code_directory=$1
scratch_directory=$2
store_finish_directory=$3

#Update sample list (in the case of any issues)
scratch_raw=${scratch_directory}"lightsheet/raw/"
scratch_destriped=${scratch_directory}"lightsheet/destriped/"

# Python script replacing 0 byte files with empty images.
source ~/.bashrc
conda activate regular
cd $code_directory
python ./replaceempty.py --pathway $scratch_raw

# Create folder for destripe output
mkdir -p $scratch_destriped

#Loop through samples for zipping
for folder in $scratch_raw*/
do
	TMP=$(echo $folder)
	echo The following folder is being zipped: $TMP

	#Create output for the zip file
	tag="zipped_data/"
	sample_on_hand_basename=$(basename $TMP)
	zip_final_output="$store_finish_directory$tag$sample_on_hand_basename/"
	sbatch --job-name=zip_raw_lightsheet --mem=100G --partition=sackler-cpu --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash $code_directory/estrin_zip_raw.sh '$TMP' '$zip_final_output' '$scratch_directory'"
done

#Loop through samples
for folder in $scratch_raw*/
do
	TMP=$(echo $folder)
	echo $TMP
	sbatch --job-name=destripe_files --mem=300G --partition=scu-cpu --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash $code_directory/estrin_destripe.sh '$TMP' '$scratch_directory'"
done

sbatch --mem=50G --partition=scu-cpu --dependency=singleton --job-name=destripe_files --wrap="bash estrin_stitch_spinup.sh '$code_directory' '$scratch_directory' '$store_finish_directory'"


