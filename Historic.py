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

#%% Download data

def GetKey():
    #Read in the API key 
    with open('API_Key.txt', 'r') as file:
        Key = file.read()
    return Key

#Get API Key
Key = GetKey()

# Set Dates for the period to be plotted
Start = '2020-01-01'
End = '2020-01-02'

# BMRS url
url = 'https://api.bmreports.com/BMRS/FUELHH/v1?APIKey='+Key+'&FromDate='+Start+'&ToDate='+End+'&ServiceType=xml'

print('Fetching new data')

xml = objectify.parse(urllib.request.urlopen(url))
root=xml.getroot()

#%% Extract data

# Initialise lists for data collection
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

# Loop through xml structure to get data
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

#%% Plotting

## Can plot basic line graph of df
#df.plot()

#Better is a stacked bar plot
ax1 = df.plot.bar(stacked=True)
ax1.set_title('Total energy generated over the period '+Start+' to '+End)
ax1.set_xlabel('Period')
ax1.set_ylabel('Energy MWh')


