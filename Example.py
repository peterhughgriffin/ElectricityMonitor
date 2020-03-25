# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:49:59 2020

@author: Peter
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt


#from UKEnergy_Class import UKEnergy
import UKEnergy_Class as EnG

#%% Live Data
#
#LiveData = EnG.GetLiveData()
#
## Sort the data Descending in terms of energy contribution
#LiveData = LiveData.sort_values(by='Energy', ascending=False)
#
#
## Plot pie chart
#ax1 = LiveData.plot.pie(y='Energy', autopct='%1.1f%%', shadow=False, startangle=0, legend=False)
#ax1.set_title('Current Percentage Share of UK Electricity mix')
#ax1.set_ylabel('')


#%% Historic Data
#
# Set Dates for the period to be plotted
Start = '2020-01-29'
End = '2020-02-01'


df = EnG.UKEnergy()

df.GetData(Start,End)

df.merge(['Int_Belgium','Int_EastWest','Int_Netherlands','Int_Ireland','Int_France'],'Interconnectors')

df.plot(24,False)




