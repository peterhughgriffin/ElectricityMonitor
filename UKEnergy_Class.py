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

#For all your plotting needs
import matplotlib.pyplot as plt
# To manage dates on axis labels
import matplotlib.dates as mdates

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
        """
        This function imports the UK electricity mix from Elexon plus Solar data from Sheffield Solar
        Start gives the date of the beginning of the period imported.
        End gives the date of the end of the period imported.
        """

        self.Start = dt.datetime.strptime(Start, '%Y-%m-%d')
        self.End = dt.datetime.strptime(End, '%Y-%m-%d')
        
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
        
        print('Fetching new Solar data')
        start_date = self.Start
        delta = dt.timedelta(days=1)
        
        response =[]
        # Iterate through days and request data
        while start_date <= self.End:
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
            
        # Make period into a datetime object
        Periods=[]
        for item in Period:
            [item_Date,item_HH] = item.split('_')
            Time=dt.datetime.strptime(item_Date,'%Y-%m-%d')
            # Add half hours to datetime
            Time=Time+dt.timedelta(0,(int(item_HH)-1)*30*60)
            Periods.append(Time)
        # Place data into a Pandas Dataframe
        Data = {'Period':Periods,
                'CCGT': ccgt, 
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

        Data = pd.DataFrame(Data)

        # Make demand column 
        Data.loc[:,'Demand'] = Data.sum(axis=1)
        self.data = Data
        
    def plot(self,HHs,Demand,Beg,End):
        """
        Plots data as specified
            HHs groups data in bins of HHs half hours
            Demand is a switch that plots just the demand or the energy source breakdown
            Beg defines the start time for the plot
            End defines the End time for the plot
        """
        # Find position of Start and end time, divide by HHs and cast as integers
        BegPos = int(self.data.loc[self.data['Period'] == Beg].index.values[0]/HHs)
        EndPos = int(self.data.loc[self.data['Period'] == End].index.values[0]/HHs)
       
        # HHs defines the number of HHs to merge together, i.e, the binning of the displayed data
        if HHs<1 or type(HHs) != int:
            raise Exception("HHs must be a positive integer")
        elif HHs==1:
            RedData=self.data.iloc[BegPos:EndPos]
        else:
            RedData=self.data.groupby(self.data.index // HHs).sum()
            periods = self.data['Period'][0::HHs]
            RedData['Period']=periods.tolist()
            RedData=RedData.iloc[BegPos:EndPos]
        
        # Choose whether to plot just the demand or the generation sources 
        if Demand:
            # Plot 
            ax1=RedData.plot(x='Period',y='Demand',kind='bar', stacked=True)
            ax1.set_title('Total energy demand over the period '+self.Start.strftime("%Y-%m-%d")+' to '+self.End.strftime("%Y-%m-%d"))
        else:
            # Plot a stacked bar plot
            ax1=RedData.drop(['Demand'],axis=1).plot(x='Period',kind='bar', stacked=True)
            ax1.set_title('Total energy generated over the period '+self.Start.strftime("%Y-%m-%d")+' to '+self.End.strftime("%Y-%m-%d"))

        # Add axis labels
        ax1.set_xlabel('Period')
        ax1.set_ylabel('Power MW')
        
        # Tell matplotlib to interpret the x-axis values as dates
#        ax1.xaxis_date()
#        fmt = mdates.DateFormatter('%Y-%m-%d')
#        ax1.xaxis.set_major_formatter(fmt)
#        ax1.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    
        #Nice orientation of x axis dates        
        fig1=plt.gcf()
        fig1.autofmt_xdate()
        
        # Reduce the number of x-axis labels given
        ax1.locator_params(axis='x', nbins=13)
        # Make Plot Fullscreen
        manager = plt.get_current_fig_manager()
        manager.window.showMaximized()


    def merge(self,Subs,Label):
        """
        This function merges given categories on the given dataframe
        Subs is a list of the headings that are to be merged or a search string to find columns
        Head is a string to be the new name for the heading
        """
        # If Subs is a string then find columns containing that string
        if type(Subs)==str:
            Subs = [col for col in self.data.columns if Subs in col]
        
        self.data[Label]=self.data[Subs].sum(axis=1).tolist()
        
        self.data=self.data.drop(Subs,1)

