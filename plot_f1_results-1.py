#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 20:12:46 2023

@author: dje4001
"""
import numpy as np
import matplotlib.pyplot as plt
import glob
import ipdb
import sys
sys.path.append("/athena/listonlab/scratch/dje4001/lightsheet_cluster/")
from generate_zprojection import ZProjection

files=glob.glob("/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/output_results/*npy")

alldata=[]
for file in files:
    """ Manually skip files I did not have time to score """
    if "Cage3976688_Animal3Ex_647_Em_6806results.npy" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6805results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_68014results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6808results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6800results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6802results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6803results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6804results" in file:
        continue
    if "Cage3976688_Animal2Ex_647_Em_68014results" in file:
        continue
    
    array=np.load(file)
    array[array[:,1] == 8675309,1]=1
    array=array[~np.isnan(array).any(axis=1)]
    if array.size<1:
        continue
    #if array[:,1].sum()==0:
     #   continue
    else:
        alldata.append(array[:,:2])
    
a=np.vstack(alldata)
means = []
errors=[]
for i in np.unique(a[:,0]):
    tmp = a[np.where(a[:,0] == i)]
    means.append(np.mean(tmp[:,1]))
    errors.append(np.std(tmp[:,1])/(np.sqrt(len(tmp))))
    
means=np.array(means)
errors=np.array(errors)
plt.figure()
plt.scatter(x=a[:,0],y=a[:,1],alpha=0.5)
plt.plot(np.unique(a[:,0]),means,linewidth=3,color="red")
plt.fill_between(np.unique(a[:,0]), means-errors, means+errors,color="red",alpha=0.6,linewidth=3)
MaxX=np.unique(a[:,0])[np.where(means==np.max(means))[0][0]]
MaxF1=np.max(means)
message1="Max F1: "+str(round(MaxF1*100)/100)+" at Threshold:" +str(MaxX)
plt.text(MaxX,MaxF1+0.05,message1,horizontalalignment='right',weight='bold')
#plt.axvline(x=MaxX, color='black', label='axvline - full height',ls='--',alpha=0.9)
#plt.axhline(y=MaxF1, color='black', label='axvline - full height',ls='--',alpha=0.9)
plt.xlabel("Pixel Classification Threshold")
plt.ylabel("F1/Specificity Score")


# Generate Confusion matrix at max threshold (TP,FP,TN,FN)
TP,FP,TN,FN=0,0,0,0
counter=0
for file in files:
    """ Manually skip files I did not have time to score """
    if "Cage3976688_Animal3Ex_647_Em_6806results.npy" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6805results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_68014results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6808results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6800results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6802results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6803results" in file:
        continue
    elif "Cage4022675_Animal2Ex_647_Em_6804results" in file:
        continue
    if "Cage3976688_Animal2Ex_647_Em_68014results" in file:
        continue
    
    try:
        array=np.load(file)
        TPi,FPi,TNi,FNi=array[np.where(array[:,0]==MaxX),2:][0][0]
        TP+=TPi
        FP+=FPi
        TN+=TNi
        FN+=FNi
        counter+=1
    except:
        continue
    
##Generate Images of GT and Predictions
search_string="/athena/listonlab/scratch/dje4001/fostrap_tmtexperimental_training_data/training_data/**/*Ex_647*/"
for image_stack in glob.glob(search_string):
    image_stack=glob.glob(image_stack+"*.tif*")
    ipdb.set_trace()
    image=ZProjection(image_stack)
    image = ((image - image.min()) / (image.max()-image.min())) * 255
    plt.figure()
    plt.imshow(image,cmap="gray")
