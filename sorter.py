import csv
from apartment import Apartment



#creates a list of apartments
ApartmentList = []

#reads the .csv data, I hand copied this from a website
#Later I might web scrape it? I'm not sure
with open('ApartmentData/scrapedData.csv') as csvFile:
    readCSV = csv.reader(csvFile, delimiter = ',')

    for row in readCSV:
        price = int(row[0])
        squareFt = row[1]
        city = row[2]
        address = row[3]
        url = row[4]
        name = row[5]
        newSquareFt = 0

        if squareFt == ' ':
            newSquareFt = 1
        else:
            newSquareFt = int(squareFt)

        ApartmentList.append(Apartment(price, newSquareFt, city, address, url, name))



#sets the mins and maxes we just found and calculates the weighted number to sort the apartments
for ap in ApartmentList:
    ap.calculateWeight()



#dumb and bad insertion sort. however its so small doesn't matter
for x in range(1, len(ApartmentList)):
    ap2 = ApartmentList[x]
    y = x - 1
    while (y >= 0) and (ApartmentList[y].weightedNum > ap2.weightedNum):
        ApartmentList[y + 1] = ApartmentList[y]
        y = y - 1
    ApartmentList[y + 1] = ap2
    x = x + 1



#print them all out to me
for ap in ApartmentList:
    print(ap.name,'||', ap.weightedNum)



#put em in the sorted file!
outputSorted = open('ApartmentData/sortedApartments.csv', 'w')

for ap in ApartmentList:
    string = str(ap.price) + ',' + str(ap.size) + ',' + str(ap.city) + ',' + str(ap.address) + ',' + ap.url + ',' + str(ap.weightedNum) + '\n'
    outputSorted.write(string)

outputSorted.close()