#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#attempt 1

"""

imports subprocess
ss
# command to change into correct directory
command_one = "cd /home/dje4001/Downloads/ilastik-1.4.0-gpu-Linux/"

# running the ilastik file
# calling the project file
# stack along z axis (for 3D data in the form of tiff stack)
# output file format + filename
# access all the images from the directory
command_two = "./run_ilastik.sh --headless \
                                --project=DhritiTest.ilp \
                                --stack_along='z' \
                                --output_format=numpy \
                                --output_filename_format=/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/training_data/output_data/{nickname}_results.numpy \
                                '/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/training_data/*.tif'" 

subprocess.run(command_one)
subprocess.run(command_two)

# should have successfully ran the ilastik file on images and produced numpy output

"""

# attempt 2

import subprocess
import glob
import os

# command to change into correct directory
command_one = "cd /home/dje4001/Downloads/ilastik-1.4.0-gpu-Linux/"
subprocess.run(command_one)

# directory with all the subfolders that contain images
image_directory_main = "/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/training_data"

# create new directory to hold output files
new_path = os.mkdir("/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/ilastik_segmentation_output_data")

# go through each folder in the directory and get each file
for i in glob.glob("/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/training_data"): #accesses each of the folders
    for j in i: # access each subfolder
        newer_path = os.mkdir(new_path + "/" + i + "/" + j)
        command_two = "./run_ilastik.sh --headless \
                                        --project=DhritiTest.ilp \
                                        --stack_along='z' \
                                        --output_format=numpy \
                                        --output_filename_format=" + newer_path + "/{nickname}_results.numpy \
                                        --'*.tif'" # possible problem line
        subprocess.run(command_two) # runs command for each tif file in subfolder for all folders

# once for loop is complete it should have iterated and ran on each of the tif files in each subfolder and created same folders in new larger folder with outputs






