#!/bin/bash
ss=$1
ss+="/*.tif"
echo "$ss"
bash /home/dje4001/Downloads/ilastik-1.4.0-gpu-Linux/run_ilastik.sh --headless --project=/athena/listonlab/scratch/dje4001/DhritiTest.ilp --stack_along="z" "$ss" --output_format=numpy

