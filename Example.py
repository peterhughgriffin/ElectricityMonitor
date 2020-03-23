# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:49:59 2020

@author: Peter
"""


# Import some libraries
import urllib.request
from lxml import objectify

# Used to import Sheffield Solar data
import requests

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import datetime as dt

from UKEnergy_Class import UKEnergy

#%%


LiveData = GetLiveData()

# Sort the data Descending in terms of energy contribution
LiveData = LiveData.sort_values(by='Energy', ascending=False)


# Plot pie chart
ax1 = LiveData.plot.pie(y='Energy', autopct='%1.1f%%', shadow=False, startangle=0, legend=False)
ax1.set_title('Current Percentage Share of UK Electricity mix')
ax1.set_ylabel('')





