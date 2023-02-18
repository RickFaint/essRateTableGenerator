import pandas as pd
from haversine import haversine, Unit
import numpy as np

# fixed variables
NUMBER_OF_THINGS = 26 # number of things e.g. pallets
MIN_CHARGE = 25.67 # the min charge
RPM = 1.95 #ppm
MIN_FULL_LOAD_CHARGE = 200 # the min for any load
IMPORT_FILE = "C:/Users/faintr/Desktop/locations/rategenimp.csv"
EXPORT_FILE = "C:/Users/faintr/Desktop/locations/rategenimpDist.csv"
WIGGLE = 1.2 # to adjust for crows fly
CAP_NUMBER = 20 #the point where full load rates kick in


def loadData(filelocation):
    # read in file
    df = pd.read_csv(filelocation)
    # create column to hold haversine distance
    df['Hdistance'] = pd.Series(dtype='int')
    # create array to hold distances
    distance = []

    #loop through the dataframe and calculate the haversine for each entry and place into array
    for ind in df.index:
        distance.append(haversine((df['fromlat'][ind], df['fromlong'][ind]), (df['tolat'][ind], df['tolong'][ind]),
                                  unit=Unit.MILES)*WIGGLE)
    # convert haversine distance to an np.array as easier to add to data from then add to data frame
    np_distance = np.array(distance)
    df['Hdistance'] = np_distance.tolist()
    # add a min cost column
    df['mincost'] = pd.Series(dtype='float')
    # create new column for the max cost
    df = df.assign(MaxCost=lambda x: (x['Hdistance'] * RPM))
    # if the max cost is less than the min full load charge then replace with the min full load
    df.loc[df['MaxCost'] < MIN_FULL_LOAD_CHARGE, 'MaxCost'] = MIN_FULL_LOAD_CHARGE
    #round max cost to 2 decimals
    df['MaxCost'] = df['MaxCost'].round(decimals = 2)

    # loop through adding a rate for each pallet or HU (number of things)
    i = 1


    while i < CAP_NUMBER + 1:
        # temp array
        temp = []
        # loop through the dataframe
        for ind in df.index:
            # calculate the cost as Max cost / number of pallets
            temp.append(round(df['MaxCost'][ind]*(i / (CAP_NUMBER+1)),2))

        # convert the array to NP array so as to add to df
        np_temp = np.array(temp)
        # before adding to the dataframe remove any entries that are less than the per pallet charge
        np_temp = np.where(np_temp <MIN_CHARGE, MIN_CHARGE, np_temp)

        df[i] = np_temp.tolist()
        i += 1


    z = CAP_NUMBER+1



    while z < NUMBER_OF_THINGS:
        df[z] = df["MaxCost"]

        z += 1





    df['mincost'] = df[1]


    # save to file location
    df.to_csv(EXPORT_FILE)
    print("finished")


def num(num):
    return str(num)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    loadData(IMPORT_FILE)
# "C:\Users\faintr\Desktop\locations\rategenimp.csv"
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
