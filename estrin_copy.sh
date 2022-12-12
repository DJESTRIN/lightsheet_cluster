#!/bin/bash
SEARCHPATH=$1
base_name=${basename $SEARCHPATH}
mkdir -p /athena/listonlab/scratch/dje4001/lightsheet/raw/
rsync -av --exclude '*MIP*' --info=progress2 ${SEARCHPATH} /athena/listonlab/scratch/dje4001/lightsheet/raw/$base_name/ #Copy folders but exclude max intensity projections. 


