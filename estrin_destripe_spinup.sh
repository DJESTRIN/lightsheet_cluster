#!/bin/bash/
#Passed variables from previous script
code_directory=$1
scratch_directory=$2
store_finish_directory=$3

#Update sample list (in the case of any issues)
scratch_raw=${scratch_directory}"lightsheet/raw/"
scratch_destriped=${scratch_directory}"lightsheet/destriped/"

# Create folder for destripe output
mkdir -p $scratch_destriped

#Loop through samples
#counter=0
for folder in $scratch_raw*/
do
	#if [[ "$counter" -gt 6 ]]; then
	TMP=$(echo $folder)
	echo $TMP
	sbatch --job-name=destripe_files --mem=300G --partition=scu-cpu --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash $code_directory/estrin_destripe.sh '$TMP' '$scratch_directory'"
	#fi
	#if [[ "$counter" -gt 7 ]]; then
	#break
	#fi
	#counter=$((counter+1))
done

sbatch --mem=50G --partition=scu-cpu --dependency=singleton --job-name=destripe_files --wrap="bash estrin_stitch_spinup.sh '$code_directory' '$scratch_directory' '$store_finish_directory'"


