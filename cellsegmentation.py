
"""
SA Model classes test script
"""
import pickle 
import argparse
import os
import sys

sys.path.insert(0,'/home/dje4001/LIGHTSHEET_CLUSTER/SA_files/')

parser=argparse.ArgumentParser()
parser.add_argument('--lifecanvas_code_directory',type=str,required=True)
parser.add_argument('--input_dir',type=str,required=True)
parser.add_argument('--output_dir',type=str,required=True)

if __name__=='__main__':
    args=parser.parse_args()
    lifecanvas_code_directory=args.lifecanvas_code_directory
    sample_directory=args.input_dir
    output_directory=args.input_dir+"cell_detect_test.json"
    os.chdir(lifecanvas_code_directory)
    from ModelClasses import Model_DetectOnly
    model = Model_DetectOnly(detectorPath = "/home/dje4001/LIGHTSHEET_CLUSTER/SA_files/Models/tf-models/ViralFluorescence-classify",
        detectionThreshold=0.6,
        modelName="ViralFluorescence (detect only)",
        modelDescription="A Model made by lifecanvas I think",)

    with open('/home/dje4001/LIGHTSHEET_CLUSTER/SA_files/Models/ViralFluorescence_model.pkl','wb') as f:
        pickle.dump(model,f)
        
    print(str(sample_directory))
    model.execute_on_dataset(data_path=sample_directory, out_path=output_directory, z_step=4)
