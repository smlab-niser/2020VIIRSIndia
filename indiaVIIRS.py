# Importing the required packages
import os
import json
import rasterio
import rasterio.features
import rasterio.mask
import shapely.geometry
import pandas as pd
from affine import Affine
import numpy as np
from matplotlib import pyplot as plt
import csv


'''
Raster function for india to get total luminosity of India  

Open the source image as a raster object, to get India we crop raster by calling rasterio.mask.mask function 
documentation of rasterio.mask.mask:' https://rasterio.readthedocs.io/en/latest/api/rasterio.mask.html#rasterio.mask.raster_geometry_mask'

Input: The function has parameters first is raster object second is geometry of region of interest here it is India's geometry, which is extracted from json file of India,

Output: The outputs of mask function have a tuple which has intensity of India, we sum all elements to get total intensity
'''
    
def raster_array_India(image):
    sumi=0
    data=json.load(open("json/india.json"))
    ind_geom=[data['geometry']]

    with rasterio.open(image) as src:
        out_imageind,out_transform = rasterio.mask.mask(src, ind_geom, all_touched=True, nodata=0.0,crop=True)
    raster_array=out_imageind[0]   
    for row in range (len(raster_array)):
         for col in range(len(raster_array[0])):
                if(raster_array[row][col]<0.0):
                    raster_array[row][col]=0.0
                sumi = sumi + raster_array[row][col]
    return sumi


'''
Raster array function for states, to get luminosity of a state
1. We open the source image as a raster object, to get the reqired state we crop raster by calling rasterio.mask.mask function 
documentation of rasterio.mask.mask:' https://rasterio.readthedocs.io/en/latest/api/rasterio.mask.html#rasterio.mask.raster_geometry_mask'
2. Input : The function has parameters first is raster object second is geometry of region of interest here it is the state's geometry, which is extracted from json file of India's states ,
3. Output : The outputs of mask function have a tuple which has intensity of the state, we sum all elements to get total intensity  
'''

def raster_array_state(image,state):
    sumi=0
    for x in data_states['features']:
        if (x['id']==state):
            state_geo=[x['geometry']]
    
    with rasterio.open(image) as src:
        out_imagest,out_transform = rasterio.mask.mask(src,state_geo , all_touched=True, nodata=0.0,crop=True)   
    raster_array=  out_imagest[0]
    for row in range (len(raster_array)):
            for col in range(len(raster_array[0])):
                if(raster_array[row][col]<0.0):
                    raster_array[row][col]=0.0
                sumi = sumi + raster_array[row][col]
    return sumi

# Store all the VIIRS tif files in "files"
import os
path = '../dataset/'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if 'rade9h.tif' in file:
            files.append(os.path.join(r, file))

# # Print the filename for verification
# for f in files:
#     print(f)


# # Summing for India and saving in Indiadata.csv
# with open('IndiaData.csv','w', newline='') as f:
#     thewriter=csv.writer(f)
#     for vf in files:
#         thewriter.writerow([vf[26:32],raster_array_India(vf)])

# # Sample code to test for 1 file
# sampleF = '../dataset/2012E/SVDNB_npp_20120401-20120430_75N060E_vcmcfg_v10_c201605121456/SVDNB_npp_20120401-20120430_75N060E_vcmcfg_v10_c201605121456.avg_rade9h.tif'
# print(raster_array(sampleF))


''' Makes list a of staes in json file to give as input in raster_array_state function '''

states=[]
data_states=json.load(open("json/states.json"))
for x in data_states["features"]:
    states.append(x['id'])


# Summing for States of India and saving in Indiadata.csv
with open('IndiaState.csv','w', newline='') as f:
    thewriter=csv.writer(f)
    for vf in files:
        for i in states:
            thewriter.writerow([vf[26:32],i,raster_array_state(vf,i)])