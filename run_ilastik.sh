#!/bin/bash
for d in $(find /athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/training_data/ -maxdepth 2 -type d -name '*Ex*Em*');
do
	echo $d
	sbatch --mem=60G --partition=scu-cpu,sackler-cpu --job-name=ilastik_segment --requeue --wrap="bash /athena/listonlab/scratch/dje4001/lightsheet_cluster/ilastik.sh $d"
done 
