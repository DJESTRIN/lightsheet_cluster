#!/bin/bash
SEARCHPATH=$1
base_name=${basename $SEARCHPATH}
mkdir -p /athena/listonlab/scratch/dje4001/lightsheet/raw/
rsync -av --info=progress2 ${SEARCHPATH} /athena/listonlab/scratch/dje4001/lightsheet/raw/$base_name/


