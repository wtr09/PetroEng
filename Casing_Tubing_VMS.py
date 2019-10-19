# -*- coding: utf-8 -*-
"""
Tyler Ragan
10/17/2019
Casing and Tubing Design

"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.cm import coolwarm
import numpy as np
import math
import seaborn as sns
import pandas as pd



def valid(user):
    i = 0
    while i == 0:
        try:
            value = float(user)
            return float(user)
            i = 1
        except ValueError:
            user = input("Please Enter Valid Value:")
#verifies input is in correct format
            
def area(do,di):
    return (do**2 - di**2)*(3.1415/4)
#returns cross sectional area of casing

def tstress(ri,ro,r,po,pi):
    return -(((ri**2)*(ro**2)*(po-pi))/((ro**2)-(ri**2))*(1/(r**2)) + ((po*ro**2)-(pi*ri**2))/(ro**2-ri**2))
#returns tangential stress in casing
def rstress(ri,ro,r,po,pi):
    return -(-((ri**2)*(ro**2)*(po-pi))/((ro**2)-(ri**2))*(1/(r**2)) + ((po*ro**2)-(pi*ri**2))/(ro**2-ri**2))
#returns radial stress in casing




def main():
    do = valid(input("Enter Outside Diameter:"))
    di = valid(input("Enter Inside Diameter:"))
    fz = valid(input("Enter Tension:"))
    MYS = valid(input("Enter Minimum Yield Strength:"))
    po = valid(input("Enter External Pressure:"))
    pi = valid(input("Enter Internal Pressure:"))
    DLS = valid(input("Enter Dogleg Severity:"))
    ro = do/2
    ri = di/2
    ra = (do + di)/2


    if DLS > 0:
        astress = fz/area(do,di) + 218*DLS*ra
        astresscom = fz/area(do,di) - 218*DLS*ra
    else:
        astress = fz/area(do,di)
        astresscom = fz/area(do,di) 
    #adds bending stress to axial stress if applicable
    
    count = 0
    rlist = []
    for i in np.arange(ri,ro,.01):
        count = count + 1
        rlist.append(i)
    #creates through wall thickness points

    vmslist = []
    vmslistcom = []
    for i in rlist:
        x = rstress(ri,ro,i,po,pi)
        y = tstress(ri,ro,i,po,pi)
        vms = (.5*((y-x)**2+(x-astress)**2+(astress-y)**2))**.5
        vmslist.append(vms)
        vmscom = (.5*((y-x)**2+(x-astresscom)**2+(astresscom-y)**2))**.5
        vmslistcom.append(vmscom)
   #calculates von mises stress state based on various points in casing call (incorporates tension and compression for bending if applicable)

    xxlist = []
    yylist = []
    vmsxyz = []

    for i in np.arange(0.000,6.281,.15):
        for ii in rlist:
            xx = ii*math.cos(i)
            yy = ii*math.sin(i)
            xxlist.append(xx)
            yylist.append(yy)
    #creates  x and y data points for various wall thickness points (in circle)
    
    
    t = int(len(xxlist)/2)
    tt = int(len(xxlist)/len(vmslist))
   
    for i in range(0,tt):
        for iii in vmslist:
            vmsxyz.append(iii)   
    del vmsxyz[0:t] 

    for i in range(0,tt):
        for iiii in vmslistcom:
            vmsxyz.append(iiii)   
    del vmsxyz[len(xxlist):]    
   #creates stress states (half of tube) of compression and tension if bending is applicable 

    d = []
    dd = []
    ddd = []
    for i in range(0,int(MYS),1000):
        d.append(0)
        dd.append(0)
        ddd.append(i)
    #creates center axis for casing

    df = pd.DataFrame(vmslist,index = rlist)
    sns.heatmap(df, cmap="Greens")   
    plt.savefig('Wall Thickness Stress (Tension).png')
    df2 = pd.DataFrame(vmslistcom,index = rlist)
    sns.heatmap(df2, cmap="Blues")   
    plt.savefig('Wall Thickness Stress (Compression).png')
    #plots von mises stress state for various wall thickness points 
    
    colors = range(len(xxlist))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    s= ax.scatter(xxlist, yylist, vmsxyz, c=colors, cmap = coolwarm,alpha=0.9)
    ax.scatter(d,dd,ddd,'-o')
    ax.set_xlabel('X(In)')
    ax.set_ylabel('Y(In)')
    ax.set_zlabel('Von Mises Stress (psi)')
    ax.set_zlim([0,MYS])
    #cbar = plt.colorbar(s, orientation='horizontal')
    #cbar.set_label('Von Mises Stress (psi)')
    plt.show()
    fig.savefig('Stress State.png')
    #plots von mises stress state in geometric position of tube 

    df = pd.DataFrame({"Radius":rlist,"Stress (psi)-T":vmslist,"Stress (psi)-C":vmslistcom})
    df.to_csv("vmsoutput.csv", index=False)
    #saves stress states to CSV file
if __name__ == "__main__":
    main()