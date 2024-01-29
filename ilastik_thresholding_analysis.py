#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
To do:
    generate a plot of real image, gt, and ilastik segmentation, and ilastik counts (all seperated and all together)
    Incorporate argparse
    save results to numpy files
    
"""
import glob
import ipdb
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from PIL import Image
import random
import tqdm
from multiprocessing import Pool
import math
import argparse
    
def get_cells(np_path,threshold):
    #Import numpy array
    data=np.load(np_path)
    
    #Threshold cell body counts segmentation channel
    data=data[:,:,:,2]
        
    data[data<=threshold]=0
    data[data>threshold]=1
    blobs=label(data)
    return data,blobs

def calculate_f1(pred,gt):
    gt=np.asarray(gt)
    pred=np.asarray(pred)
    #Calculate Number of TP,TN,FP,FN
    if gt.size==0 and pred.size>0:
        TN=1 #A blank cube meaning true negative
        FP=len(pred) #Number of wrong counts
        TP=0
        FN=0
    elif gt.size>0 and pred.size==0:
        FN=len(gt)
        TN=0
        TP=0
        FP=0
    elif gt.size>0 and pred.size>0:
        TN=0
        TP=0
        FN=0
        for real in gt:
            min_dist=10
            
            for pot in pred:
                dist=math.dist(real,pot)
                if dist<min_dist:
                    min_dist=dist
            
            if min_dist<10:
                TP+=1
            else:
                FN+=1
        FP=len(pred)-TP
      
    elif gt.size==0 and pred.size==0:
        TN=1
        FP=0
        TP=0
        FN=0
        
    if (TP+FP)==0 or (TP+FN)==0:
        if TN==1:
            F1=TN/(TN+FP)
        else:
            ipdb.set_trace()
    else:
        Precision=TP/(TP+FP)
        Recall=TP/(TP+FN)
        F1=(Precision*Recall*2)/(Recall+Precision)
    return F1,TP,FP,TN,FN
            
def blobs_to_coordinates(blobs):
    #From blobs, get coordinates of potential cells in 3D space
    cell_coordinates=[]
    for hypo_cell in np.unique(blobs)[1:]:
        coordinates=np.asarray(np.where(blobs==hypo_cell))
        coordinates=np.mean(coordinates.T,axis=0)
        cell_coordinates.append(coordinates)
        
    cell_coordinates=np.asarray(cell_coordinates)
    
    #Eliminate double counts
    final_coordinates=cell_coordinates
    for i,cell1 in enumerate(cell_coordinates):
        temp_list=[cell1]
        for cell2 in cell_coordinates:
            dist=math.dist(cell1,cell2)
            if dist<7 and dist != 0:
                temp_list.append(cell2)
                try:
                    final_coordinates=np.delete(final_coordinates,(np.where(final_coordinates==cell2)[0][0]),axis=0)
                except:
                    final_coordinates=final_coordinates
                
        if len(temp_list)>1:
            temp_list=np.asarray(temp_list)
            new_coordinate=np.mean(temp_list,axis=0)
            if np.asarray(np.where(final_coordinates==cell1)).size!=0:
                final_coordinates[(np.where(final_coordinates==cell1)[0][0]),:]=new_coordinate
    
    
    return final_coordinates
 

def analyze(gt_file,pred_file):
    #From numpy file, calculate F1 score of cells labeled by ilastik
    gt=np.load(gt_file,allow_pickle=True,encoding="bytes")
    gt=gt.item()
    gt=gt['Red']
    
    F1s=[]
    print("Looping through thresholds, calculating F1 score")
    for threshes in tqdm.tqdm(range(50,100),total=len(range(50,100))):
        threshes=threshes/100
        preds,cells=get_cells(pred_file,threshes)
    
        if len(np.unique(cells))>1:
            cell_coordinates=blobs_to_coordinates(cells)
            F1,TP,FP,TN,FN=calculate_f1(cell_coordinates,gt)
            F1s.append([threshes,F1,TP,FP,TN,FN])
        else:
            F1,TP,FP,TN,FN=calculate_f1([],gt)
            F1s.append([threshes,F1,TP,FP,TN,FN])

    F1s=np.asarray(F1s)
    return F1s 

def save_f1s(array,syglass_file):
    folder,filename=syglass_file.split('syg_drop/')
    folder+="output_results/"
    filename,_=filename.split('syglass.np')
    filename+="results.npy"
    output_path=folder+filename
    np.save(output_path,array)
    return

def main(syglass_file):
    ilastik_files=glob.glob("/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/training_data/**/**/*.npy")
    _,filename=syglass_file.split('syg_drop/')
    filename,_=filename.split('syglass')
    cageanimal,channel=filename.split('Ex')
    cage,animal=cageanimal.split('_')
    channel="Ex"+channel
    
    #convert all to upper
    cage=cage.upper()
    animal=animal.upper()
    channel=channel.upper()
    
    for ilastik_file in ilastik_files:
        ilastik_fileup=ilastik_file.upper()
        if (cage in ilastik_fileup) and (animal in ilastik_fileup) and (channel in ilastik_fileup):
            F1s=analyze(syglass_file,ilastik_file)
            #Save F1 results to numpy
            save_f1s(F1s,syglass_file)
               
# syglass_files=glob.glob("/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/*syg*/*.npy")
# main(syglass_files[37])

parser=argparse.ArgumentParser()
parser.add_argument("--syglass_file",type=str,required=True)

if __name__=='__main__':
    args=parser.parse_args()
    main(args.syglass_file)

        
    
    


