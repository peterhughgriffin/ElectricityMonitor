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


df = UKEnergy()

df.GetData(Start,End)


#%% Plotting

## Can plot basic line graph of df
#df.plot()

#Better is a stacked bar plot
ax1 = df.data.plot.bar(stacked=True)
ax1.set_title('Total energy generated over the period '+Start+' to '+End)
ax1.set_xlabel('Period')
ax1.set_ylabel('Energy MWh')


ax1 = df.data.plot.bar(y='Other',stacked=True)
ax1.set_title('Total energy generated over the period '+Start+' to '+End)
ax1.set_xlabel('Period')
ax1.set_ylabel('Energy MWh')




