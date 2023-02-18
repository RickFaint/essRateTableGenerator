import requests
import pandas as pd
import numpy as np
import json

IMPORT_FILE = "C:/Users/faintr/Desktop/locations/postcodes.csv"
EXPORT_FILE = "C:/Users/faintr/Desktop/locations/postlats.csv"
API = "http://api.postcodes.io/postcodes/"



def loadData(filelocation):
    # read in file
    df = pd.read_csv(filelocation)



    lat = []
    long = []
    status = []

    #loop through the dataframe and calculate the haversine for each entry and place into array
    for ind in df.index:
        response = requests.get(API+df['postcode'][ind].replace(" ",""))
        if response.status_code == 200:
            tempjson = response.json()
            long.append(tempjson["result"]["longitude"])
            lat.append(tempjson["result"]["latitude"])
            status.append(response.status_code)
        else:
            status.append(response.status_code)
            long.append(0.00)
            lat.append(0.00)





    np_lat = np.array(lat)
    np_long = np.array(long)
    np_status = np.array(status)
    df['latitude'] = np_lat.tolist()
    df['longitude'] = np_long.tolist()
    df['status'] = np_status.tolist()
    df.to_csv(EXPORT_FILE)
    print("finished")

if __name__ == '__main__':
    loadData(IMPORT_FILE)