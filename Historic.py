# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 22:44:54 2020

TO view the xml structure see:
    https://api.bmreports.com/BMRS/FUELHH/v1?APIKey=____Key____

@author: Peter
"""


# Import some libraries
import urllib.request
from lxml import objectify

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime
from datetime import timedelta
#%%

def GetKey():
    #Read in the API key 
    with open('API_Key.txt', 'r') as file:
        Key = file.read()
    return Key


def GetFuelMix(root):
    Fuel =[]
    Energy =[]
    Pct =[]
    
    #Extract data
    for child in root:
        for e in child.getchildren():
            Fuel.append(e.attrib['TYPE'])
            Energy.append(int(e.attrib['VAL']))
            Pct.append(float(e.attrib['PCT']))
    
    # Place data into a Pandas Dataframe
    Data = {'Energy': Energy, 'Pct': Pct}
    df = pd.DataFrame(Data, index = Fuel)
    return df


Key = GetKey()

Start = '2020-01-01'
End = '2020-01-02'


url = 'https://api.bmreports.com/BMRS/FUELHH/v1?APIKey='+Key+'&ServiceType=xml'
#+'&FromDate='+Start+'&ToDate='+End+'&ServiceType=xml'

print('Fetching new data')

xml = objectify.parse(urllib.request.urlopen(url))
root=xml.getroot()

    #%%
    
GetFuelMix(root.responseBody.responseList.item[1])


#%%

Pos=root.responseBody.responseList.item

Fuel =[]
Energy =[]
Pct =[]

#Extract data
for e in Pos.getchildren():
    Fuel.append(e.attrib['wind'])
    Energy.append(int(e.attrib['ccgt']))
    Pct.append(float(e.attrib['ocgt']))

Data = {'Energy': Energy, 'Pct': Pct}
df = pd.DataFrame(Data, index = Fuel)




#%%


Period =[]
ccgt =[]
oil =[]
coal =[]
nuclear =[]
wind =[]
ps =[]
npshyd =[]
ocgt =[]
other =[]
intfr =[]
intirl =[]
intned =[]
intew =[]
biomass =[]
intnem =[]

for HH in root.responseBody.responseList.findall('item'):
    #Half hour period is given by the date and the period number
    Period.append(HH.startTimeOfHalfHrPeriod+'_'+str(HH.settlementPeriod))
    #Energy generated from each source in that period is captured
    ccgt.append(int(HH.ccgt))
    oil.append(int(HH.oil))
    coal.append(int(HH.coal))
    nuclear.append(int(HH.nuclear))
    wind.append(int(HH.wind))
    ps.append(int(HH.ps))
    npshyd.append(int(HH.npshyd))
    ocgt.append(int(HH.ocgt))
    other.append(int(HH.other))
    intfr.append(int(HH.intfr))
    intirl.append(int(HH.intirl))
    intned.append(int(HH.intned))
    intew.append(int(HH.intew))
    biomass.append(int(HH.biomass))
    intnem.append(int(HH.intnem))
    
# Place data into a Pandas Dataframe
Data = {'CCGT': ccgt, 
        'Oil': oil,
        'Coal': coal,
        'Nuclear': nuclear,
        'Wind': wind,
        'Pumped Storage': ps,
        'Non-Pumped_Hydro': npshyd,
        'OCGT': ocgt,
        'Other': other,
        'Int_France': intfr,
        'Int_Ireland': intirl,
        'Int_Netherlands': intned,
        'Int_EastWest': intew,
        'Biomass': biomass,
        'Int_Belgium': intnem}

df = pd.DataFrame(Data, index = Period)
