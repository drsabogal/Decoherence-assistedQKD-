# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 18:02:27 2023

@author: dr.sabogal
"""


import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score




def lin(x,a,b):
    return a*x +b
x2 = np.linspace(0,1.2,20)

#dbmax = np.array([-0.00795954,0.32252109,0.40262459,0.62589104,0.77889491,0.89342833,1.14660171])
dbmax = np.array([0,0.3,0.392,0.632,0.78,0.9,1.168])
daset = np.array([0,0.1845,0.369,0.5535,0.738,0.9225,1.107])
da_error = np.full(7,0.03)
db_error= da_error
print(da_error)
popt_lin,pcov_lin = curve_fit(lin,daset, dbmax)
print(popt_lin)
print(np.sqrt(pcov_lin[0,0]),np.sqrt(pcov_lin[1,1]))
m = str(round(popt_lin[0],2))
dm = str(round(np.sqrt(pcov_lin[0,0]),2))
b = str(round(popt_lin[1],2))
db = str(round(np.sqrt(pcov_lin[1,1]),2))

cm = 1/2.54

fig2 = plt.figure(figsize=(2*8.6*cm, 2*8.6*cm))
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = '16'
plt.scatter(daset,dbmax,s=30)
plt.ylim(-0.1,1.4)
plt.xlim(-0.1,1.4)
plt.errorbar(daset,dbmax,yerr=db_error,xerr=da_error,ls='none')
plt.plot(x2,lin(x2,*popt_lin),c = "green", label =' '+r'$d_{b-Qmin}$=('+m+r'$\pm$' +dm+')$d_{a}$ + (' +b+r'$\pm$'+db+')')
plt.xlabel('$d_{a}$(mm)')
plt.ylabel(r'$d_{b-Q min}$(mm)')
plt.legend(fontsize =16, loc='best')
plt.savefig("lineQBER_svg",dpi =600,format = 'svg')