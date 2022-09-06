# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 12:18:07 2020

@author: pierre.blanchard

Retrieve GeoJSON of isochrones. 

Input : DEPCOM (centroids)
Output : GeoJSON of areas accessible by road transportation in a given time and traffic 

VERY IMPORTANT TO VISIT BEFORE LAUCNHING TO SEE PARAMETERS MODALITIES!!!!!!!!!
https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-an-isochrone#examples
"""

#IMPORT LIBRARIES
import requests
import pandas as pd
import os
import json
import time
from time import sleep
import string


# 1 Specify API key
API_KEY = '' #specify here your API KEY

#2 Import your data
path = 'C:/'
df = pd.read_csv(path,sep=',',encoding='1252')

#3 Set the path you want the isochrones to be stored 
outputpath = ''

#4 Set / remove useful/useless parameters 

address = df['address']

df["address"] = df['address'].str.replace('[^\w\s]','')


#can be longitude + latitude or adress , see more about geographic coverage here https://docs.microsoft.com/en-us/bingmaps/coverage/geographic-coverage
max_time = 15 #integer
time_unit = 'minute'
date_time = '03/01/2020' # 03/01/2011 05:42:00 OR 05:42:00 [assumes the current day] OR 03/01/2011 [assumes the current time]
max_distance = '' #integer
distance_unit =''
optimize = 'timeWithTraffic' #https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-an-isochrone#examples
travel_mode = 'walking' #trucks because of height limits and road limitations

#Functions definition

def url_params(address,max_time,time_unit,date_time,max_distance,distance_unit,optimize,travel_mode):
    url_get_asynchronoous = 'http://dev.virtualearth.net/REST/v1/Routes/IsochronesAsync?waypoint='+str(address)+'&maxTime='+str(max_time)+'&timeUnit='+time_unit+'&optimize='+optimize+'&maxDistance='+str(max_distance)+'&distanceUnit='+distance_unit+'&dateTime='+date_time+'&travelMode='+travel_mode+'&key='+API_KEY
    response = requests.get(url_get_asynchronoous)
    response = response.json()
    if (response['statusCode']==200):
        requestID = response['resourceSets'][0]['resources'][0]['requestId']
        return requestID
    else:
        print('Issue in get url')

def url_callback(requestID):
    sleep(2)
    url_get_callback ='http://dev.virtualearth.net//REST//v1//Routes//IsochronesAsyncCallback?key='+API_KEY+'&requestId='+requestID
    sleep(2)
    callback = requests.get(url_get_callback)
    callback = callback.json()
    if (callback['statusCode']==200):
        resultURL = callback['resourceSets'][0]['resources'][0]['resultUrl']
        return resultURL
    else:
        print('Issue in callback url')
        
def url_results(resultURL):
    result = requests.get(resultURL)
    result = result.json()
    if ('polygons' in result['resourceSets'][0]['resources'][0]):
        coordinates = result['resourceSets'][0]['resources'][0]['polygons'][0]['coordinates'][0]
        return coordinates
    else:
        print('No polygons')

def invert_latlong(coordinates):
    inverted_coord = []
    for index in coordinates:
        index = index[::-1]
        inverted_coord.append(index)
        coordinates = inverted_coord
    return coordinates

def fill_json(coordinates):
    skeleton ={'type':'MultiPolygon','coordinates':[]}
    skeleton['coordinates']=[[coordinates]]
    return skeleton

def export_iso(skeleton,address):
    with open(os.path.join(outputpath,'iso_BING_TEST_adresse_'+str(address)+'.json'), 'w')  as f:
                f.write(json.dumps(skeleton))

#Function to raise exception in case of failure
def my_throw(str):
    raise Exception(str)


#LOOP FOR 3 BOUNDARIES 


def main():
        for address in (zip(df.address)):
            print(address)
            
            requestID = url_params(address,max_time,time_unit,date_time,max_distance,distance_unit,optimize,travel_mode)
            print('RequestID is: '+requestID)
            
            resultURL = url_callback(requestID)
            print('resultURL is: '+resultURL)
            
            coordinates = url_results(resultURL)
            print('coordinates are computed')
            
            if (coordinates):
                coordinates = invert_latlong(coordinates)
                print('results are ready')
            
                skeleton = fill_json(coordinates)
                print('JSON is filled with results')
            
                export_iso(skeleton,address)
                print('JSON is exported')
                
            else:
                continue

main()









