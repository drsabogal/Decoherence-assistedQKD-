#!/usr/bin/env python
# coding: utf-8

# In[143]:


import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


# In[144]:
def loadTimeS(file):    
    data=  np.genfromtxt(file,skip_header=2)
    return data

def loadMPos(file):
    d = open(file)
    motorPosition = d.readlines()[1].split('\t')
    return motorPosition
def QBER(KeyA,KeyB):
    error = 0
    for i in range(len(KeyA)):
        error = error + (int(KeyA[i])^int(KeyB[i]))
    error  = error/len(KeyA)
    print(len(KeyA))
    return error*100


# In[145]:


def AliceBobBit(dat):
    data = np.copy(dat)
##time stamps in seconds 
    data[:,0] = data[:,0]*81*10**(-12)
#clack data without time
    y = data[:,1]
    cero = y==0 
    one = y==1
    two = y==2
    three = y==3
#AliceData taking into acount time
    Alicedata = data[cero+one]
#BobData
    Bobdata = data[two+three]

##Alice and Bob indexes
    Aliceindex = np.arange(0,len(Alicedata))
    Bobindex = np.arange(0,len(Bobdata))

## Join indexes with time and clicks
    AliceTime = Alicedata[:,0]
    BobTime = Bobdata[:,0]
    AliceClick = Alicedata[:,1]
    BobClick = Bobdata[:,1]
##Definition of taus and stds
    n = 10**(-9)
    tau1_4 = 3.587*n
    std1_4 = 0.379*n*2
    tau1_3 = 4.14*n
    std1_3 = 0.321*n*2
    tau2_4= 3.888*n
    std2_4 = 0.387*n*2
    tau2_3 = 4.318*n
    std2_3 = 0.386*n*2
##method to obtain the index in which Alice and Bob acquired a coincidence
    AliceI = []
    BobI = [] 
    fin = False
    if(len(Bobdata)!=0):
        for i in range(len(Aliceindex)):
            for j in range(len(Bobindex)):
                tau = np.absolute(AliceTime[i]-BobTime[j])
                if(np.absolute(tau-tau1_4)<std1_4):
                    AliceI.append(i)
                    BobI.append(j)

                    break               
                if(np.absolute(tau-tau1_3)<std1_3):
                    AliceI.append(i)
                    BobI.append(j)

                    break
                if(np.absolute(tau-tau2_4)<std2_4):
                    AliceI.append(i)
                    BobI.append(j)

                    break
                if(np.absolute(tau-tau2_3)<std2_3):
                    AliceI.append(i)
                    BobI.append(j)

                    break
                if(i == (len(Aliceindex)-1) and j == (len(Bobindex)-1) and len(AliceI)<1):
                    AliceI = None
                    BobI = None
            if(fin == True):
                break 
    if(len(Bobdata)==0):
          AliceI = None
          BobI = None
 ##appoint Alice and Bob bits

    AliceBit = []
    BobBit = []

    if(AliceI == None or BobI == None):
        AliceBit.append(None)
        BobBit.append(None)     

##    if(AliceI != None and BobI != None):
##        if(AliceClick[AliceI] ==0):
#            AliceBit = 0
#        if(AliceClick[AliceI] ==1):
#            AliceBit = 1
#       if(BobClick[BobI] == 3):
#            BobBit = 0
#        if(BobClick[BobI] == 2):
#            BobBit = 1
#    return AliceBit,BobBit 

    if(AliceI != None and BobI != None):
        BobClick = np.abs(BobClick-3)
        AliceBit = AliceClick[AliceI]
        BobBit = BobClick[BobI]
        
    return AliceBit,BobBit




d =[]
QBERS = []

TBDA = "0,0000"
for l in tqdm(range(0,40)):
    n = len(str(round(l*0.0075,4)).split(".")[1])
    d.append(round(l*0.0075,4))
    global label
    global qber
    AliceMatriz = []
    BobMatriz = []
    AliceKey =np.array([])
    BobKey = np.array([])
    for p in range(0,199):
        if(n==1):
            label = 'QBER_'+str(round(l*0.0075,4)).replace(".",",") +'000_'+TBDA+'_C0_B'+str(p)+'.txt'
        if(n==3):
            label ='QBER_'+str(round(l*0.0075,4)).replace(".",",") +'0_'+TBDA+'_C0_B'+str(p)+'.txt'
        if(n==2):
            label ='QBER_'+str(round(l*0.0075,4)).replace(".",",") +'00_'+TBDA+'_C0_B'+str(p)+'.txt'
        if(n>3):
            label ='QBER_'+str(round(l*0.0075,4)).replace(".",",") +'_'+TBDA+'_C0_B'+str(p)+'.txt'

        if(loadMPos(label)[4]==loadMPos(label)[5]):
            if(None not in AliceBobBit(loadTimeS(label))[0] ):
                AliceKey = np.append(AliceKey,AliceBobBit(loadTimeS(label))[0])
                BobKey = np.append(BobKey,AliceBobBit(loadTimeS(label))[1])
    qber = QBER(AliceKey,BobKey)
    QBERS.append(qber)

d = np.array(d)
QBERS = np.array(QBERS)
print(QBERS)
QBERS.tofile('QBERS'+TBDA+'3.dat')
d.tofile('d.dat')
plt.scatter(d,QBERS)
'''
        AliceMatriz.append([loadMPos(label)[4],AliceBobBit(loadTimeS(label))[0]])
        BobMatriz.append([loadMPos(label)[5],AliceBobBit(loadTimeS(label))[1]])
    AliceKey = []
    BobKey = []

    for k in range(len(AliceMatriz)):
        if(AliceMatriz[k][1] != None and BobMatriz[k][1]!=None):
            if(float(AliceMatriz[k][0]) ==  float(BobMatriz[k][0])):
                AliceKey.append(AliceMatriz[k][1])
                BobKey.append(BobMatriz[k][1])
    qber = QBER(AliceKey,BobKey)
    QBERS.append(qber)
print(QBERS)

d = np.array(d)
QBERS = np.array(QBERS)

QBERS.tofile('QBERS'+TBDA+'.dat')
d.tofile('d.dat')

plt.scatter(d,QBERS)

        if(loadMPos(label)[4]==loadMPos(label)[5]):
            AliceKey = np.append(AliceKey,AliceBobBit(label)[0])
            BobKey = np.append(BobKey,AliceBobBit(label)[1])
    qber = 100*np.sum(np.logical_xor(AliceKey,BobKey))/len(AliceKey)     
    print(qber) 


print(AliceBobBit(loadTimeS("QB_0,0000_0,0000_C0_B0.txt")))
          
'''
