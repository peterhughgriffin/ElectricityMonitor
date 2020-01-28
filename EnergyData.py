
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

def GetLiveData():
    
    Key=GetKey()
    
    if 'xml' in locals():
        print('Fetching data')
        with open('LastAccessed.txt', 'r') as file:
            StoredTime = datetime.strptime(file.read(),'%Y-%m-%d %H:%M:%S')
        NowTime = datetime.now()
        Diff = NowTime-StoredTime
        print('Data last accessed '+ str(Diff)[0:-7]+' ago')
        FiveMin = timedelta(minutes=5)
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
    
    #%%
    #Initialise lists for extracting data to
    Fuel =[]
    Energy =[]
    Pct =[]
    
    #Extract data
    for child in root.INST:
        for e in child.getchildren():
            Fuel.append(e.attrib['TYPE'])
            Energy.append(int(e.attrib['VAL']))
            Pct.append(float(e.attrib['PCT']))
    
    # Place data into a Pandas Dataframe
    Data = {'Energy': Energy, 'Pct': Pct}
    df = pd.DataFrame(Data, index = Fuel)
    
    return df

#%%


LiveData = GetLiveData()

# Sort the data Descending in terms of energy contribution
LiveData = LiveData.sort_values(by='Energy', ascending=False)


# Plot pie chart
ax1 = LiveData.plot.pie(y='Energy', autopct='%1.1f%%', shadow=False, startangle=0, legend=False)
ax1.set_title('Current Percentage Share of UK Electricity mix')
ax1.set_ylabel('')





