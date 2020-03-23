# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 22:44:54 2020

TO view the xml structure see:
    https://api.bmreports.com/BMRS/FUELHH/v1?APIKey=____Key____

@author: Peter
"""


# Import some libraries
import datetime as dt

import urllib.request
from lxml import objectify

# Used to import Sheffield Solar data
import requests

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Set Dates for the period to be plotted
Start = '2020-01-28'
End = '2020-01-29'

#%% Download BMRS data

def GetKey():
    #Read in the API key 
    with open('API_Key.txt', 'r') as file:
        Key = file.read()
    return Key

#Get API Key
Key = GetKey()


# BMRS url
url = 'https://api.bmreports.com/BMRS/FUELHH/v1?APIKey='+Key+'&FromDate='+Start+'&ToDate='+End+'&ServiceType=xml'
print('Fetching new BMRS data')

xml = objectify.parse(urllib.request.urlopen(url))
root=xml.getroot()

#%% Download Sheffield Solar data
# The Sheffield API only allows one days worth of data in a request, so we need to request each day individually

start_date = dt.datetime.strptime(Start, '%Y-%m-%d')
end_date = dt.datetime.strptime(End, '%Y-%m-%d')
delta = dt.timedelta(days=1)

response =[]

while start_date <= end_date:
    endpoint = 'https://api0.solar.sheffield.ac.uk/pvlive/v2?start='+start_date.strftime("%Y-%m-%d")+'T00:00:00&data_format=json'
    response.extend(requests.get(endpoint).json()['data'])
    # Remove last entry, which is midnight the following morning (In order to avoid duplication)
    del response[-1]
    start_date += delta

# Clear out region and datetime data
Solar=[]
for row in response:
    Solar.append(row[2])
    



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
        'Wind': wind,
        'Nuclear': nuclear,
        'Biomass': biomass,
        'Coal': coal,
        'Pumped Storage': ps,
        'Non-Pumped_Hydro': npshyd,
        'OCGT': ocgt,
        'Oil': oil,
        'Other': other,
        'Int_France': intfr,
        'Int_Ireland': intirl,
        'Int_Netherlands': intned,
        'Int_EastWest': intew,
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


ax1 = df.plot.bar(y='Other',stacked=True)
ax1.set_title('Total energy generated over the period '+Start+' to '+End)
ax1.set_xlabel('Period')
ax1.set_ylabel('Energy MWh')




