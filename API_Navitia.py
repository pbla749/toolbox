Navitia.py
L'année dernière
17 Déc. 2021

Vous avez importé un élément
Texte
Navitia.py
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:18:07 2020

@author: pierre.blanchard

Retrieve GeoJSON of isochrones. 

Input : DEPCOM (centroids)
Output : GeoJSON of areas accessible by public transportation in a given time

http://doc.navitia.io/#isochrones-currently-in-beta
"""

#IMPORT LIBRARIES
import requests
import pandas as pd
import os
import json


#TO BE MODIFIED
df = pd.read_csv('S:/SPALLIAN/CLIENTS/MNT/GESTION DE PROJET/Agences_geocodees.csv',sep=',',encoding='1252')
outputpath = 'C:/Users/pierre.blanchard/Desktop/isochrones'
boundary_duration =[3000] #Set the different periods en seconds 
token='00873bad-adfd-4082-bed7-10858467f303' #the token to be used to access the API

#NOTHING TO DO HERE
head = {'Authorization': token} 
date = input("Enter a date (YYYYMMDD):")
print("Date is: " + date)
mydate= date+'T000000'
print(mydate)

longitude = 2.35511
latitude = 48.88933

for longitude, latitude,result_city in (zip(df.longitude,df.latitude,df.result_city)):
    print(longitude, latitude,result_city)
    url = 'https://api.navitia.io/v1/coverage/fr-idf/isochrones?from='+str(longitude)+';'+str(latitude)+'&boundary_duration[]='+str(boundary_duration[0])#+'&boundary_duration[]='+str(boundary_duration[1])#+'&boundary_duration[]='+str(boundary_duration[2])+'&boundary_duration[]='+str(boundary_duration[3])
    response = requests.get(url,headers=head)
    response = response.json()
    if len(response)>1:
        response = response['isochrones']
        for bound in range(len(boundary_duration)):
            print(bound)
            mygeojson = response[bound]['geojson']
            with open(os.path.join(outputpath, 'iso_Navitia_'+str(boundary_duration[bound])+'_'+result_city+'.json'), 'w')  as f:
                f.write(json.dumps(mygeojson))
