#!/bin/bash
for i in $(find /athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/syg_drop -type f -name '*syglass.npy');
do 

sbatch --job-name=F1analysis --mem=60G --partition=scu-cpu,sackler-cpu --mail-type=BEGIN,END,FAIL --mail-user=dje4001@med.cornell.edu --wrap="bash /athena/listonlab/scratch/dje4001/lightsheet_cluster/ilastik_f1.sh $i"

done 
