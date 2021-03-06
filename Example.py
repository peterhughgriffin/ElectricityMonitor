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
Start = '2020-01-01'
End = '2020-01-31'

# Initialise data frame of energy date
df = EnG.UKEnergy()
# Get the energy data and load into the dataframe
df.GetData(Start,End)

# Merge the interconnectors into one item
# By List of headings
#df.merge(['Int_Belgium','Int_EastWest','Int_Netherlands','Int_Ireland','Int_France'],'Interconnectors')
# Or by search string
df.merge('Int_','Interconnectors')
#%%
# Select data range of interest
Beg='2020-01-01'
End='2020-01-08'

# Plot the data
df.demandplot(1,Beg,End)

# Select data range of interest
Beg='2020-01-09'
End='2020-01-16'

df.barplot(1,True,Beg,End)

#%%



