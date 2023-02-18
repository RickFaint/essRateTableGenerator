# essRateTableGenerator
generatesRateTablesForEss


Generates rate tables for ESS application import lat and longs for the to and from locations and  it uses Haversine distance to calculate distances then applies a cost per mile  and creates a reasonably realistic matrix

LatLongGen takes a list of postcodes and generates their lats and longs and exports a file . if error then it will show in the status column and will show 0.00 for lat and long
