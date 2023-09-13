#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#takes png and converts to tiff via Pillow

import argparse
import os
import glob
from PIL import Image
from tqdm import tqdm

def pngtotiff(input_dir, output_dir):
        
    #finding all the .png files
    os.chdir(input_dir)
    files = glob.glob('**/*.png', recursive=True)

    #progress bar
    progress_bar = tqdm(total = len(files), desc = '.png to .tiff conversion progress')

    #iterate through all files
    for file in files:
        input_path = os.path.join(input_dir, file)
        output_file = os.path.splitext(file)[0] + ".tiff"
        output_path = os.path.join(output_dir, output_file)
        
        #converting and saving
        img = Image.open(input_path)
        img.save(output_path, "TIFF")

        #update progress bar
        progress_bar.update()
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert a .png file to a .TIFF file")
    parser.add_argument("--input_directory", type=str, help="the directory containing the input .png files")
    parser.add_argument("--output_directory", type=str, help="The directory containing the output .tiff files",required=False)
    args = parser.parse_args()
    pngtotiff(args.input_directory, args.output_directory)
