# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 10:54:01 2023

@author: dr.sabogal
"""

import numpy as np
from scipy.optimize import curve_fit

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.metrics import r2_score
dload= '0.225'
Error0 =np.round(np.array(np.fromfile('QBERS'+dload+'.dat')),2)

dis = np.array(np.fromfile('d.dat'))
dis = (np.round((dis),3))*4


print(dis[np.where(Error0 == Error0.min())[0][0]])
dab = dis[np.where(Error0 == Error0.min())[0][0]]

print(Error0.min())

def QBERTeo(db,q0y):
    x =100*(1/4)*(1-np.exp(-(2*((dab-db)*(dab-db)))/(0.8*0.8))*np.cos(2*(dab-db)*q0y +2*np.pi))+3.9
    return x


popt0, pcov0 = curve_fit(QBERTeo, dis, Error0,p0=[7], method = "lm")
line = np.linspace(0,60,20)
distance = np.linspace(0,1.2,1000)
print(popt0)
print(np.sqrt(pcov0[0]))
cm = 1/2.54
fig = plt.figure(figsize=(5*cm,5*cm))
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = '9'
plt.scatter(dis,Error0,label = " $d_{a}$="+str(round(float(dload)*4.1,2))+' mm',s=3)
plt.plot(distance,QBERTeo(distance,popt0[0]),c = "green")
plt.ylim(0,60)
plt.xlabel('$d_{b}$ (mm)')
plt.ylabel('QBER %')

plt.savefig("QBERsvg"+dload.replace('.',',')+'.svg',dpi =600,format = 'svg',transparent=True)
