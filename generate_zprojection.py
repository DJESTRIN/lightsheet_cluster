#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Max intensity projection image, and perform validation of classifier
"""
from PIL import Image, ImageOps
import numpy as np
import os,glob
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/dje4001/lightsheet_cluster/')
import argparse
import ipdb

plt.close("all")

def ZProjection(image_directories):
    init_image=Image.open(image_directories[0])
    init_image=ImageOps.grayscale(init_image)
    init_image=np.asarray(init_image)
    
    counter=0
    for image_oh in image_directories[1:]:
       image_oh=Image.open(image_oh)
       image_oh=ImageOps.grayscale(image_oh)
       image_oh=ImageOps.autocontrast(image_oh,cutoff=99)
       image_oh=np.asarray(image_oh) 
       con_images=np.concatenate((init_image[...,None],image_oh[...,None]),axis=2)
       init_image=np.sum(con_images,axis=2)
       counter+=1
       if counter>=500:
           init_image=init_image[0:500,0:500]/500
           return init_image
       
    return init_image #This is now the max z projection


def normalized_max_projection(image_directories):
    init_image=Image.open(image_directories[0])
    init_image=ImageOps.grayscale(init_image)
    init_image=np.asarray(init_image)
    init_image=init_image[...,None]
    
    counter=1
    for image_oh in image_directories[1:]:
       image_oh=Image.open(image_oh)
       image_oh=ImageOps.grayscale(image_oh)
       #image_oh=ImageOps.autocontrast(image_oh,cutoff=99)
       image_oh=np.asarray(image_oh) 
       init_image=np.concatenate((init_image,image_oh[...,None]),axis=2)
       #init_image=np.amax(con_images,axis=2)
       counter+=1
       if counter>=len(image_directories):
           ipdb.set_trace()
           init_image=init_image-np.min(init_image)/(np.max(init_image)-np.min(init_image))*255
           init_image=np.amax(init_image,axis=2)
           return init_image
       
    return init_image #This is now the max z projection

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--subject_directory',type=str,required=True)
    args=parser.parse_args()
    subject_directory=args.subject_directory+'/'
    folders=glob.glob(subject_directory+'Ex_647_Em_680*/')
    drop_folder=subject_directory+'drop/'
    if os.path.exists(drop_folder):
        print('folder exists')
    else:
        os.mkdir(drop_folder)
    
    for k,folder in enumerate(folders):
        search_string=folder+'*.tif*'
        tiff_images=glob.glob(search_string)
        if len(tiff_images)>1:
            zimage=ZProjection(tiff_images)
    
            #Plot and save z projection
            plt.figure(figsize=(10,10))
            plt.imshow(zimage,cmap='gray')
            plt.axis('off')
            string="zmax_"+str(k)+".png"
            plt.savefig(drop_folder+string)
            plt.close()

