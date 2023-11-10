#!/bin/bash/
#Passed variables from previous script
code_directory=$1
scratch_directory=$2
store_finish_directory=$3

#Update sample list (in the case of any issues)
scratch_raw=${scratch_directory}"lightsheet/raw/"
scratch_converted=${scratch_directory}"lightsheet/converted/"

mkdir -p $scratch_converted

#Loop through samples
for folder in $scratch_raw*/
do
        TMP=$(echo $folder)
        echo $TMP
        sbatch --job-name=convert_png_to_tiff --mem=300G --partition=scu-cpu --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash /home/fs01/dje4001/lightsheet_cluster/convert.sh $code_directory $TMP"
done

#sbatch --mem=50G --partition=scu-cpu --dependency=singleton --job-name=destripe_files --wrap="bash estrin_destripe_spinup.sh '$code_directory' '$scratch_directory' '$store_finish_directory'"



