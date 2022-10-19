
"""
SA Model classes test script
"""
from ModelClasses import Model_DetectOnly
import pickle 
import argparse
import os

parser=argparse.ArgumentParser()
parser.add_argument('--lifecanvas_code_directory',type=str,required=True)
parser.add_argument('--sample_directory',type=str,required=True)

if __name__=='__main__':
    args=parser.parse_args()
    lifecanvas_code_directory=args.lifecanvas_code_directory
    sample_directory=args.sample_directory
    output_directory=sample_directory+"cell_detect_test.json"
    os.chdir(lifecanvas_code_directory)
    model = Model_DetectOnly(detectorPath = "./Models/tf-models/ViralFluorescence_detect_2021_5_4_85",
        detectionThreshold=0.9,
        modelName="ViralFluorescence (detect only)",
        modelDescription="A Model made by lifecanvas I think",)

    with open('./Models/ViralFluorescence_model.pkl','wb') as f:
        pickle.dump(model,f)
    
    model.execute_on_dataset(data_path=sample_directory, out_path=output_directory, z_step=4)