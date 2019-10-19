# -*- coding: utf-8 -*-
"""
Tyler Ragan
10/2/2019
"""

import numpy as np
import pandas as pd
       
df = pd.read_csv('survey.csv')
#reads surveys into dataframe

MD = []
MDFT = []
INC =[]
AZI = []
TVD = []
NORTH = []
EAST = []
VS = []
GEAST = []
GNORTH = []


for i in df['Measured Depth (ft)']:
    MD.append(int(i))

x = len(MD) 

for i in range(MD[x-1]+1):
    MDFT.append(i)
#turns surveys into one foot increments

for i in df['Inclination (deg)']:
    INC.append(float(i))    

for i in df['Azimuth (deg)']:
    AZI.append(float(i))  

for i in df['True Vertical Depth(ft)']:
    TVD.append(float(i)) 

for i in df['Northing(ft)']:
    NORTH.append(float(i)) 

for i in df['Easting(ft)']:
    EAST.append(float(i)) 
    
for i in df['Vertical Section(ft)']:
    VS.append(float(i)) 

for i in df['Grid East(ft)']:
    GEAST.append(float(i))

for i in df['Grid North(ft)']:
    GNORTH.append(float(i))
    
#creates lists of dataframe array, makes value float

mdx = np.array(MDFT)
#turns list into array

incx = np.interp(MDFT, MD, INC, period = len(MDFT))
azix = np.interp(MDFT, MD, AZI, period = len(MDFT))
tvdx = np.interp(MDFT, MD, TVD, period = len(MDFT))
northx = np.interp(MDFT, MD, NORTH, period = len(MDFT))
eastx = np.interp(MDFT, MD, EAST, period = len(MDFT))
vsx = np.interp(MDFT, MD, VS, period = len(MDFT))
geastx = np.interp(MDFT, MD, GEAST, period = len(MDFT))
gnorthx = np.interp(MDFT, MD, GNORTH, period = len(MDFT))
#interpolates XX value for each list based on MD survey points and one foot increments, assigns numpy array


df = pd.DataFrame({"GRID EAST":geastx,"GRID NORTH":gnorthx,"MD":mdx, "INC" : incx, "AZI":azix,"TVD" : tvdx, "North":northx, "East":eastx,"VS":vsx})
df.to_csv("outputsurveydata.csv", index=False)
#saves numpy arrays into dataframe, saves dataframe to CSV

print("Complete")

