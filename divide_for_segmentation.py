#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Divide Images
https://stackoverflow.com/questions/5953373/how-to-split-image-into-multiple-pieces-in-python
"""
import os,glob
import argparse
from PIL import Image
from itertools import product
#import ipdb
from tqdm import tqdm

def tile(image_path, slice_folder, block_size,z):
    img = Image.open(image_path)
    w, h = img.size
    grid = product(range(0, h-h%block_size, block_size), range(0, w-w%block_size, block_size))
    for i, j in grid:
        drop_path = slice_folder + str(i) + '_' + str(j) +"/"
        box = (j, i, j+block_size, i+block_size)
        
        # Create subfolder if not created and save image to it
        if os.path.exists(drop_path):
            out = drop_path+"image"+str(z)+".tiff"
            img.crop(box).save(out)
        else:
            os.mkdir(drop_path)
            out = drop_path+"image"+str(z)+".tiff"
            img.crop(box).save(out)
        

def divide_image_stack(stitched_input,output_parent,block_size):
    image_search=stitched_input+'*.tif*'
    images=glob.glob(image_search) #Does glob sort the files correctly??
    images=sorted(images)
 
    slices=range(0,len(images)-len(images)%block_size,block_size)
    for slice_start,slice_stop in zip(slices[:-1],slices[1:]):
        # Create subfolder based on slice
        slice_folder=output_parent+"slice"+str(slice_start)+"/"
        if not os.path.exists(slice_folder):
            os.mkdir(slice_folder)
        
        # Loop through images in the current slice and tile them
        for z in tqdm(range(slice_start,slice_stop)):
            image_oh=images[z]
            tile(image_oh,slice_folder,block_size,z)
        

if __name__=='__main__':
    stitched_input="/athena/listonlab/scratch/dje4001/lightsheet_scratch/rabies_cort_experimental_restain/lightsheet/stitched/20221107_12_37_06_CAGE3811492_ANIMAL4_VIRUSRABIES_CORTEXPERIMENTAL/Ex_647_Em_680/"
    output_parent="/athena/listonlab/scratch/dje4001/lightsheet_scratch/rabies_cort_experimental_restain/lightsheet/ilastik/20221107_12_37_06_CAGE3811492_ANIMAL4_VIRUSRABIES_CORTEXPERIMENTAL/"
    if not os.path.exists(output_parent):
        os.mkdir(output_parent)
    divide_image_stack(stitched_input,output_parent,500)











