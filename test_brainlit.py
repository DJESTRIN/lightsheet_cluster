#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 09:37:26 2023

@author: dje4001
"""

import os, glob
import cv2
import numpy as np
from brainlit.algorithms.detect_somas import find_somas as fs
import matplotlib.pyplot as plt

cube_dir="/athena/listonlab/store/dje4001/lightsheet/test_segmentation_f1/rabies_cort_experimental_training_data/20220923_14_38_30_CAGE3752774_ANIMAL05_VIRUSRABIES_CORTEXPERIMENTALEx_647_Em_680/Ex_647_Em_6803/"
os.chdir(cube_dir)
images=glob.glob("*.tif*")

stack=[]
for image in images:
    img=cv2.imread(image,cv2.IMREAD_GRAYSCALE)
    img=np.asarray(img)
    stack.append(img)
    
stack=np.asarray(stack)
stack=stack.astype(np.uint16)
label,relative_cent,out=fs(stack,[1.83,1.83,2])
print(label)
print(relative_cent)
print(out)


_, axes = plt.subplots(1, 2)

ax = axes[0]
vol_proj = np.amax(stack, axis=2)
ax.imshow(vol_proj, cmap="gray", origin="lower")
# ax.scatter(
#     relative_cent[:, 1],
#     relative_cent[:, 0],
#     c="none",
#     edgecolor="r",
#     label="Ground truth",
# )
# if label == 1:
#     ax.scatter(relative_cent[:, 1], relative_cent[:, 0], c="b", alpha=0.5)
# ax.set_title("Volume")

# ax = axes[1]
# mask_proj = np.amax(out, axis=2)
# ax.imshow(mask_proj, cmap="jet", vmin=0, origin="lower")
plt.savefig('/home/dje4001/brainlit_classifier.pdf')


