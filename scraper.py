import bs4 as bs
import urllib.request
import re
import  csv

apartmentScrapeList = [[]]
URLsToScrape = []
pagesToScrape = []
bsPages = []

#open the CSV that lists the pages that I want to scrape
with open('ApartmentData/URLsToScrape.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter = ',')
    for row in readCSV:
        for column in row:
            URLsToScrape.append(column)

#open the page(s) and add the HTML to pages to scrape
for URL in URLsToScrape:
    client = urllib.request.urlopen(URL)
    rawSource = client.read()
    pagesToScrape.append(rawSource)
    client.close()

#make the HTML into a BS object
for x in range(0, len(pagesToScrape)):
   bsPages.append(bs.BeautifulSoup(pagesToScrape[x], 'lxml'))

#their website is stupid and has different names for the div class listings for some reason
#i used a regular expression. they're very cool. this finds everything that begins with "level"
for page in bsPages:
    allListings = page.find_all("div", {"class":re.compile("^level")})

    for listing in allListings:
        tempDataSet = []
        #regular expressions are so good
        propInfo = listing.find_all("div", {"class":re.compile("^propertyInfo xs-")})

        #get the rent. i opted to just grab the cheapest one, also i removed commas
        tempR = propInfo[0].find_all("span", {"class": "altRentDisplay"})[0].text.strip().replace(',', '')
        tempR = tempR.split(' -', 1)[0]
        tempDataSet.append(tempR)

        #get the address, i removed the commas to help put it in a .csv
        tempDataSet.append(propInfo[0].find_all("span", {"itemprop":"address"})[0].text.strip().replace(',', ''))

        #get the name of the apartment
        for name in propInfo[0].find_all('a'):
            tempDataSet.append(name.get('title'))

        #get the page link
        for link in propInfo[0].find_all('a'):
            tempDataSet.append(link.get('href'))

        apartmentScrapeList.append(tempDataSet)

print(apartmentScrapeList)

scrapeOutput = open('ApartmentData/scrapedData.csv', 'w')
string = 'PRICE,ADDRESS,NAME,URL'
for x in apartmentScrapeList:
    for y in x:
        string += (y + ', ')
    string+= '\n'

scrapeOutput.write(string)
scrapeOutput.close()