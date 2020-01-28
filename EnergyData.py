
# Import some libraries
import urllib.request
from lxml import objectify

import pandas as pd

import matplotlib.pyplot as plt

from datetime import datetime
from datetime import timedelta


def GetKey():
    #Read in the API key 
    file = open('API_Key.txt', 'r') 
    Key = file.read()
    return Key


Key=GetKey()

if 'xml' in locals():
    print('everywhere')
    StoredTime = datetime.strptime(root.INST[0].attrib['AT'],'%Y-%m-%d %H:%M:%S')
    print(StoredTime)
    NowTime = datetime.now()
    print(NowTime)
    Diff = NowTime-StoredTime
    print(Diff)
    FiveMin = timedelta(minutes=5)
    if Diff > FiveMin:
        print('Here')
        #Data can be accessed from the API at the Elexon portal: https://www.elexonportal.co.uk/scripting
        url='https://downloads.elexonportal.co.uk/fuel/download/latest?key='+Key
        xml = objectify.parse(urllib.request.urlopen(url))
        root=xml.getroot()

else:
    print('There')
    #Data can be accessed from the API at the Elexon portal: https://www.elexonportal.co.uk/scripting
    url='https://downloads.elexonportal.co.uk/fuel/download/latest?key='+Key
    xml = objectify.parse(urllib.request.urlopen(url))
    root=xml.getroot()

#Initialise lists for extracting data from
Fuel =[]
Energy =[]
Pct =[]

#
for child in root.INST:
    for e in child.getchildren():
        Fuel.append(e.attrib['TYPE'])
        Energy.append(e.attrib['VAL'])
        Pct.append(e.attrib['PCT'])

plt.pie(Energy, labels=Fuel, autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()