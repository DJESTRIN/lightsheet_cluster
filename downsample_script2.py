#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Downsample Image Stack """
from skimage.io import imread, imsave
from scipy.ndimage import zoom
import numpy as np
import glob
import os
import re
from multiprocessing import Pool
import warnings
import random
import argparse
warnings.filterwarnings("ignore")


class post_stitch_manipulations(object):
    def __init__(self, input_path, output_path,*args):
        #input path contains all channels for a single sample
        #output path should be a folder in storage. 
        self.input_path=input_path
        self.output_path=output_path

        #Get image list
        os.chdir(self.input_path)
        self.image_log=glob.glob('*.tif*')
        self.image_log=sorted(self.image_log,key=self.custom_sort)
        
        
        #Get image properties
        image_oh=imread(self.image_log[0])
        (self.x,self.y)=image_oh.shape
        self.z=len(self.image_log)

        
    def generate_cubes(self,*args):
        if not args:
            self.get_cubes()
        else:
            self.get_cubes(list(args))
        self.make_output_dirs()
        self.grab_cube()
        
    def get_cubes(self,*args):
        if not args:
            # Generates 15 cube data sets for the given sample. 
            cubes=[]
            for u in range(15):
                x,y,z=random.randint(0,(self.x-500)),random.randint(0,(self.y-500)),random.randint(0,(self.z-500))
                cube_oh=[x,x+500,y,y+500,z,z+500]
                cubes.append(cube_oh)
            
            self.cubes=cubes
            
        else:
            cubes=[]
            for u in args:
                cube_oh=u
                cubes.append(cube_oh)
                
            self.cubes=list(cubes)
            self.cubes=list(self.cubes[0][0][0])
            print(self.cubes)
        return
    
    def make_output_dirs(self):
        #Generates a new path for each cube
        for u in range(15):
            output_sub=self.output_path+str(u)+"/"
            if not os.path.exists(output_sub):
                os.mkdir(output_sub)
        
    def custom_sort(self,x):
        return int(re.sub(r'[^0-9]','',(os.path.basename(x))))

    def parallel_crop(self,x):
        filename=x[0]
        cube=x[1]
        output_num=x[2][0]
        output_path=self.output_path+str(output_num)+"/"
        image_oh=imread(filename)
        crop_image_oh=image_oh[cube[0]:cube[1],cube[2]:cube[3]]
        imsave(output_path+filename,crop_image_oh)
        return

    def grab_cube(self):
        
        for i,cube in enumerate(self.cubes):
            #Loop through images on z stack
            self.image_log_oh=self.image_log[cube[4]:cube[5]]
            cube_repeated=np.tile(np.array(cube),(cube[5]-cube[4],1))
            cube_repeated=cube_repeated.tolist()
            
            output_repeated=np.tile(np.array(i),(cube[5]-cube[4],1))
            output_repeated=output_repeated.tolist()
            inputs=list(zip(self.image_log_oh,cube_repeated,output_repeated))
            with Pool() as p:
                p.map(self.parallel_crop,inputs)
                
        return
    
    def parrallel_downsample(self,x):
        filename=x[0]
        output_path=x[1]
        image_oh=np.array(imread(filename))
        ds_image_oh=zoom(image_oh,(0.2,0.2))
        imsave(output_path+str(x[2])+".tif",ds_image_oh)
        return
    
    def custom_sort_ds(self,x):
        return int(x[:-4])
    
    def downsample_image(self):
        # downsample images in parrallel
        inputs=[]
        for k,filename in enumerate(self.image_log):
            inputs.append([filename,self.output_path,k])
        self.inputs=inputs
        with Pool() as p:
            p.map(self.parrallel_downsample,inputs)
        
        # Load in semi final image stack
        os.chdir(self.output_path)
        self.output_image_log=glob.glob('*.tif*')
        self.output_image_log=sorted(self.output_image_log,key=self.custom_sort_ds)
        self.image_stack=[]
        for image in self.output_image_log:
            image_oh=imread(image)
            self.image_stack.append(image_oh)
        
        for f in self.output_image_log:
            os.remove(f)
        
        #Downsample the z axis. 
        self.image_stack=np.array(self.image_stack)
        self.image_stack=zoom(self.image_stack,(0.2,1,1))
        
        #Write image stack to outputpath
        for i,filename in enumerate(self.output_image_log):
            imsave(self.output_path+str(i)+'.tif',self.image_stack[i])
            if (i+1)==self.image_stack.shape[0]:
                break
            
        return
    
    
    
#input_path='/athena/listonlab/store/dje4001/lightsheet/puja_gcamp/stitched/20220925_15_33_31_Cage_AnimalF83_VirusAAVrgNAcAAV1GCAMP7_PUJAPAREKH/20220925_15_33_31_Cage_AnimalF83_VirusAAVrgNAcAAV1GCAMP7_PUJAPAREKH/Ex_647_Em_680/'
#output_path='/athena/listonlab/store/dje4001/lightsheet/puja_gcamp/downsampled/20220925_15_33_31_Cage_AnimalF83_VirusAAVrgNAcAAV1GCAMP7_PUJAPAREKH/Ex_647_Em_680/'


parser=argparse.ArgumentParser()
parser.add_argument("--input_path",type=str,required=True)
parser.add_argument("--output_path",type=str,required=True)
parser.add_argument("--function",type=str,required=True)
 
if __name__=="__main__":
    args=parser.parse_args()
    data=post_stitch_manipulations(args.input_path,args.output_path)

    # Seperate code into functions
    if args.function=='generate_cubes':
        data.generate_cubes()
    
    elif args.function=='crop_cube':
        data.generate_cubes()
    
    elif args.function=='downsample_image':
        data.downsample_image()

