#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 17:03:20 2023

@author: dje4001
"""
import json
import numpy as np 
import scipy
import math
import os
from skimage.io import imread
import sys
sys.path.insert(0,'/home/dje4001/CloudReg/')
sys.path.insert(0,'/home/dje4001/lightsheet_cluster/')
from CloudReg.cloudreg.scripts.ARA_stuff.parse_ara import *
from princeton_ara import *
import argparse
import itertools
from tqdm import tqdm
import ipdb
import re
from multiprocessing import Pool
import ipdb
import pandas as pd

# Generate a tree strucutre from Allen Registered Atlas file. Used for parsing
ara_file="/home/dje4001/CloudReg/cloudreg/scripts/ARA_stuff/ara_ontology.json"
with open(atlas_json_file,'r') as infile:
    ontology_dict = json.load(infile)

class mouse_brain(object):
    def __init__(self,name,coexpression_threshold,Tree):
        self.mouse_name=name
        self.coexpression_threshold=coexpression_threshold
        self.Tree=Tree
        self.all_children=self.Tree.get_progeny(nodename='root')
    
    def add_channel(self,channel):
        self.channels=self.channels.append(channel)
        
        if len(self.channels)>1:
            self.cell_coexpression(cell_list1, cell_list2)
        
    def cell_coexpression(self,cell_list1,cell_list2):
        """Checks for coexpression. also used to eliminate double counts"""
        flag=np.zeros(len(cell_list1))
        index=0
        
        for c1 in tqdm(cell_list1,total=len(cell_list1)):
            for c2 in cell_list2:
                distance=math.dist(c1,c2)
                if distance<self.coexpression_threshold:
                    if distance>0:
                        flag[index]=1
            index+=1
        return flag
    

class sample_channel(mouse_brain):
    def __init__(self, image_path, atlas_path, cell_counts_path, output_path,coexpression_threshold,Tree,ara_file):
        #self.channel_name=(basename image_path)
        self.image_path=image_path
        self.atlas_path=atlas_path
        self.cell_counts_path=cell_counts_path 
        self.output_path=output_path
        self.coexpression_threshold=coexpression_threshold
        self.Tree=Tree
        self.all_children=self.Tree.get_progeny(nodename='root')
        self.ara_file=ara_file
    
    def forward(self):
        self.parse_file_names()
        self.load_cell_corrdinates()
        self.registration()
        self.levels=[]
        for u in range(10):
            self.levels.append(self.level_registration(u+1))
        self.build_tall_format()
        return print("finished")
        
    def load_cell_corrdinates(self):
        with open(self.cell_counts_path,'r') as f:
            self.cells = json.load(f)
        self.cells=self.cells[1:1000]
        self.eliminate_double_counts()
        self.total_cells=len(self.cells)

    def eliminate_double_counts(self):
        doubled_counts=self.cell_coexpression(self.cells, self.cells)
        self.cells=np.delete(self.cells,np.where(doubled_counts==1),axis=0)
        
    def parrallel_registration(self,inputs):
        (x,y,z),index=inputs
        if z<3900: #### DELETE AFTER TEST ###
            image_name=self.atlas_path+str(z)+".tiff"
            image_oh=np.array(imread(image_name))
            
            try: #DELETE LATER
                brain_region=image_oh[x,y]
            except:
                brain_region=image_oh[-1,-1]
            return index,brain_region
    
    def registration(self):
        """ Get all the registration infromation regarding each neuron"""
        # Get cell atlas IDS
        inputs=list(zip(self.cells,range(len(self.cells))))
        with Pool() as p:
            self.cell_atlas_ids=p.map(self.parrallel_registration,inputs)
        
        dt=np.dtype('float,float')
        self.cell_atlas_ids=np.array(self.cell_atlas_ids,dt)
        self.cell_atlas_ids=self.cell_atlas_ids['f1']
        self.cell_atlas_ids=self.cell_atlas_ids[~np.isnan(self.cell_atlas_ids)]
        self.cell_atlas_ids=self.cell_atlas_ids[self.cell_atlas_ids!=0]
        #Get atlas names
        self.cell_atlas_names=[]
        self.not_on_list=[]
        for c in self.cell_atlas_ids:
            try:
                self.cell_atlas_names.append(self.all_children[0][self.all_children[1].index(c)])
            except:
                self.not_on_list.append(c)
        return
    
    def level_registration(self,level):
        """ Takes the registration list, and converts it to different level 
            Example: converting crebellar cortex, purkinje layer to cerebellum
            input and output should be a column that is the same size"""
        #Separate ara into groups by level, get names of children
        names,__=get_children_names(self.ara_file,level)
        
        #Generate new list of names where new names must be member of level.
        cell_atlas_names_leveled=self.cell_atlas_names[:]
        for i,current_name in enumerate(self.cell_atlas_names):
            Found=False
            for key in names:
                for child in names[key]:
                    if current_name == child:
                        cell_atlas_names_leveled[i]=key
                        Found=True
                        break
                if Found==True:
                    break
            if Found==False:
                cell_atlas_names_leveled[i]=current_name
        return cell_atlas_names_leveled
    
    def move_up_tree(self,steps):
        #Generate new list of names where new names must be member of level.
        self.cell_atlas_names_step=[]
        index=[]
        for current_name in self.cell_atlas_names:
            if steps>1:
                for u in range(steps):
                    try:
                        current_name=Tree.get_parent(current_name)
                    except:
                        if current_name==None:
                            break
                self.cell_atlas_names_step.append(current_name)
            elif steps<1:
                print("steps for move_up_tree method is incorrect, please fix")
                return self.cell_atlas_names_step
            else:
                self.cell_atlas_names_step.append(Tree.get_parent(current_name))
        return self.cell_atlas_names_step
    
    def parse_file_names(self):
        """ Parse Image path for tall format. 
            Common naming scheme for all animals:
            20220622_14_59_40_CAGE3752774_ANIMAL02_VIRUSRABIES_BEHAVIORNONE_CORTEXPERIMENTAL"""
        #Set to empty in the case they are not used
        self.cage=""
        self.subjectid=""
        self.virus=""
        self.behavior=""
        self.treatment=""
        
        #Split path
        _,_,_,_,_,self.experiment,_,_,_,self.channel_name,_=self.image_path.split('/')
        
        #Get mouse info details
        for ggg in self.image_path.split("_"):
            ggg=ggg.split('/')[0]
            if "CAGE" in ggg:
                self.cage=ggg
            if "ANIMAL" in ggg:
                self.subjectid=ggg
            if "VIRUS" in ggg:
                self.virus=ggg
            if "BEHAVIOR" in ggg:
                self.behavior=ggg
            if "CORT" in ggg:
                self.treatment=ggg
        return

    def build_tall_format(self):
        """ Take cdata regarding cells and put them into tall format. 
        
            cage, subjectid, virus, behavior, treatment, channel,number_of_cell_index,
            brain_region_lf,l2,l3,l4,l5,l6, etc.
        """
        ipdb.set_trace()
        cell_array=np.asarray(self.cell_atlas_names)
        level_array=np.asarray(self.levels)
        cell_array=cell_array.T
        cell_array=np.expand_dims(cell_array,axis=1)
        level_array=level_array.T
        onemat=np.ones(cell_array.shape[0])
        
        
        mouse_info=[self.experiment,self.channel_name,self.cage,self.subjectid,self.virus,self.behavior,self.treatment]
        mouse_info=np.asarray(mouse_info)
        mouse_info2=np.tile(mouse_info.T,(cell_array.shape[0],1))
        data=np.hstack((mouse_info2,cell_array,level_array))

        df=pd.DataFrame(data,columns=['experiment','channel','cage','subjectid','virus','behavior','treatment','location','lv1','lv2','lv3','lv4','lv5','lv6','lv7','lv8','lv9','lv10'])
        df['n']=onemat
        filename=self.output_path+"tall.csv"
        df.to_csv(filename)
        #Save to drop path, one csv file per brain
        return
      
""" 
Testing code:
    02/15 cell counts and atlas are different brains, just testing to see if it runs....
"""
image_path = "/athena/listonlab/scratch/dje4001/rabies_cort_experimental_restain/lightsheet/stitched/20221104_10_02_32_CAGE4094795_ANIMAL1_VIRUSRABIES_CORTEXPERIMENTAL/Ex_647_Em_680/"
atlas_path = "/athena/listonlab/scratch/dje4001/rabies_cort_experimental/lightsheet/registered/20220925_12_49_48_CAGE3752774_ANIMAL04_VIRUSRABIES_CORTEXPERIMENTAL/tiffsequence/"
cell_counts_path = "/athena/listonlab/scratch/dje4001/rabies_cort_experimental_restain/lightsheet/segmented/20221104_10_02_32_CAGE4094795_ANIMAL1_VIRUSRABIES_CORTEXPERIMENTAL/Ex_647_Em_680/cell_detect_test.json"
output_path = "/athena/listonlab/scratch/dje4001/rabies_cort_experimental_restain/lightsheet/tallformat/20221104_10_02_32_CAGE4094795_ANIMAL1_VIRUSRABIES_CORTEXPERIMENTAL/"
Tree=Graph(ontology_dict)
channel=sample_channel(image_path,atlas_path,cell_counts_path,output_path,5,Tree,ara_file)
channel.forward()

""" 
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument("--image_path",type=str,required=True)
    parser.add_argument("--atlas_path",type=str,required=True)
    parser.add_argument("--cell_counts_path",type=str,required=True)
    parser.add_argument("--output_path",type=str,required=True)
    Tree=Graph(ontology_dict)
    channel=sample_channel(parser.image_path,parser.atlas_path,parser.cell_counts_path,parser.output_path,5,Tree,ara_file)
    channel.forward()

"""



              