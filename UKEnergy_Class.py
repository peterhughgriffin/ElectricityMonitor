# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:21:08 2020

This code defines two functions and one class.
    GetKey - This function is to get the API key used to get data from Elexon
    GetLiveData - This function grabs the live UK energy mix and returns it as raw data and percentage

    UKEnergy - This is a class for analysing historic UK energy data

@author: Peter Hugh Griffin
"""

# Import some libraries
import urllib.request
from lxml import objectify

# Used to import Sheffield Solar data
import requests

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

#from datetime import datetime
#from datetime import timedelta
import datetime as dt
#%%

def GetKey():
    #Read in the API key 
    with open('API_Key.txt', 'r') as file:
        Key = file.read()
    return Key

def GetLiveData():
    
    Key=GetKey()
        
    if 'xml' in locals():
        print('Fetching data')
        with open('LastAccessed.txt', 'r') as file:
            StoredTime = dt.datetime.strptime(file.read(),'%Y-%m-%d %H:%M:%S')
        NowTime = dt.datetime.now()
        Diff = NowTime-StoredTime
        print('Data last accessed '+ str(Diff)[0:-7]+' ago')
        FiveMin = dt.timedelta(minutes=5)
        if Diff > FiveMin:
            print('Refreshing data')
            with open('LastAccessed.txt', 'w') as file:
                file.write(str(NowTime)[0:-7])
            #Data can be accessed from the API at the Elexon portal: https://www.elexonportal.co.uk/scripting
            url='https://downloads.elexonportal.co.uk/fuel/download/latest?key='+Key
            xml = objectify.parse(urllib.request.urlopen(url))
            root=xml.getroot()
    else:
        print('Fetching new data')
        #Data can be accessed from the API at the Elexon portal: https://www.elexonportal.co.uk/scripting
        url='https://downloads.elexonportal.co.uk/fuel/download/latest?key='+Key
        xml = objectify.parse(urllib.request.urlopen(url))
        root=xml.getroot()
        
    #Initialise lists for extracting data to
    Fuel =[]
    Energy =[]
    Pct =[]
    
    #Extract data
    for child in root.INST:
        for e in child.getchildren():
            Fuel.append(e.attrib['TYPE'])
            Energy.append(int(e.attrib['VAL']))
   
    # Add in Solar data
    endpoint = "https://api0.solar.sheffield.ac.uk/pvlive/v2"
    response = requests.get(endpoint)
    Fuel.append("Solar")
    Energy.append(response.json()['data'][0][2])
    
    Total=sum(Energy)
    for i in Energy:
        Pct.append(100*i/Total)
        
    # Place data into a Pandas Dataframe
    Data = {'Energy': Energy, 'Pct': Pct}
    df = pd.DataFrame(Data, index = Fuel)
    
    return(df)


class UKEnergy:
    def __init__(self):
        pass

    def GetData(self,Start,End):
        
        #Get API Key
        Key = GetKey()
        
        
        # BMRS url
        url = 'https://api.bmreports.com/BMRS/FUELHH/v1?APIKey='+Key+'&FromDate='+Start+'&ToDate='+End+'&ServiceType=xml'
        print('Fetching new BMRS data')
        
        xml = objectify.parse(urllib.request.urlopen(url))
        root=xml.getroot()
        
        # Download Sheffield Solar data
            # The Sheffield API only allows one days worth of data in a request
            # so we need to request each day individually
        
        start_date = dt.datetime.strptime(Start, '%Y-%m-%d')
        end_date = dt.datetime.strptime(End, '%Y-%m-%d')
        delta = dt.timedelta(days=1)
        
        response =[]
        # Iterate through days and request data
        while start_date <= end_date:
            endpoint = 'https://api0.solar.sheffield.ac.uk/pvlive/v2?start='+start_date.strftime("%Y-%m-%d")+'T00:00:00&data_format=json'
            response.extend(requests.get(endpoint).json()['data'])
            # Remove last entry, which is midnight the following morning (In order to avoid duplication)
            del response[-1]
            start_date += delta
        
        # Clear out region and datetime data
        solar=[]
        for row in response:
            solar.append(row[2])
            
        # Extract BMRS data
        
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
                'Solar': solar,
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
        
        self.data = pd.DataFrame(Data, index = Period)
        


