import csv
from apartment import Apartment



#creates a list of apartments
ApartmentList = []

#reads the .csv data, I hand copied this from a website
#Later I might web scrape it? I'm not sure
with open('ApartmentData/apartments.csv') as csvFile:
    readCSV = csv.reader(csvFile, delimiter = ',')

    for row in readCSV:
        ApartmentList.append(Apartment(int(row[0]), row[1], int(row[2]), int(row[3])))



#calculuate min and max for normalization
#very long and if statement-y. basically finds the ranges of the apartments
newMinP = 100000
newMinS = 100000
newMinR = 100000
newMaxP = 0
newMaxS = 0
newMaxR = 0
for ap in ApartmentList:
    newMinP = ap.price if (ap.price < newMinP) else newMinP
    newMaxP = ap.price if (ap.price > newMaxP) else newMaxP
    newMinS = ap.size if (ap.size < newMinS) else newMinS
    newMaxS = ap.size if (ap.size > newMaxS) else newMaxS
    newMinR = ap.rating if (ap.rating < newMinR) else newMinR
    newMaxR = ap.rating if (ap.rating > newMaxR) else newMaxR


#sets the mins and maxes we just found and calculates the weighted number to sort the apartments
for ap in ApartmentList:
    ap.setMinMax(newMinP, newMaxP, newMinS, newMaxS, newMinR, newMaxR)
    ap.calculateWeight()



#dumb and bad insertion sort. however its so small doesn't matter
for x in range(1, len(ApartmentList)):
    ap2 = ApartmentList[x]
    y = x - 1
    while (y >= 0) and (ApartmentList[y].weightedNum < ap2.weightedNum):
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
    string = str(ap.price) + ',' + str(ap.name) + ',' + str(ap.size) + ',' + str(ap.rating) + ',' + str(ap.weightedNum) + '\n'
    outputSorted.write(string)

outputSorted.close()