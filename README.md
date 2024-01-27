# lightsheet_cluster
This repository was written to analyze light sheet data on a SLURM based high performance cluster. 

The pipeline consists of 6 steps: 
(1) Moving the data to a scratch drive
(2) Denoising/destriping the data
(3) Stitching the data
(4) Registering images to allen brain atlas
(5) Segmenting pixels (cells, axons, etc)
(6) calculating the number of counts per region, generating statistics

Packages used in the pipeline have not yet been cited (I will update this soon). 
The primary sources for code are Pystripe, Terastitcher and CloudReg. Segmentation code based on BrainLine package
