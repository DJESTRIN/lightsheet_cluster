#!/bin/bash
sample=$1
output_path=/athena/listonlab/store/dje4001/lightsheet/rabies/$2/
mkdir -p $output_path
rsync -av --remove-source-files --info=progress2 $sample $output_path

