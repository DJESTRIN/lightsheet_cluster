#!/bin/bash
# Activate pystripe conda environemnt
code_directory=~/lightsheet_cluster/
scratch_directory=/athena/listonlab/scratch/dje4001/lightsheet_scratch/rabies_cort_experimental_cohort2/
store_start_directory=/athena/listonlab/scratch/dje4001/lightsheet_store/pseudorabies/CORTEXPERIMENTAL/
store_finish_directory=/athena/listonlab/scratch/dje4001/lightsheet_store/pseudorabies/CORTEXPERIMENTAL_drop/

mkdir -p $scratch_directory
mkdir -p $scratch_directory/lightsheet
mkdir -p $store_finish_directory
cd $code_directory

# Get a list of samples
samples=$(find $store_start_directory -maxdepth 1 -mindepth 1 -type d)

# Copy all pending data to the scratch drive
for i in $samples
do
    TMP=$(echo $i)
    echo $TMP
    sbatch --job-name=copying_files --mem=300G --partition=scu-cpu --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash estrin_copy.sh '$TMP' '$scratch_directory'"
done

sbatch --mem=50G --partition=scu-cpu --dependency=singleton --job-name=copying_files --wrap="bash convert_tiff_spinup.sh '$code_directory' '$scratch_directory' '$store_finish_directory'"

exit
