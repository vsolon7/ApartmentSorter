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

#so in this, the outer loop goes through all the beautiful soup pages. the inner loop looks through everything
#and stores it.
for page in bsPages:
    #this is a regular expression. it finds everything that begins with "level". their site was weird and they all started with different things
    allListings = page.find_all("div", {"class":re.compile("^level")})

    #goes through every listing in the list of all apartment listings. lol.
    for listing in allListings:
        #this will store the data for a single apartment. will later be appended to a list of lists that has all apartments
        tempDataSet = []
        #regular expressions are so good
        propInfo = listing.find_all("div", {"class":re.compile("^propertyInfo xs-")})

        #get the rent. i opted to just grab the cheapest one, also i removed commas
        tempR = propInfo[0].find_all("span", {"class": "altRentDisplay"})[0].text.strip().replace(',', '')
        tempR = tempR.split(' -', 1)[0]
        tempDataSet.append(tempR)

        #get the address, i removed the commas to help put it in a .csv
        tempDataSet.append(propInfo[0].find_all("span", {"itemprop":"address"})[0].text.strip().replace(',', ''))

        #get the name of the post
        for name in propInfo[0].find_all('a'):
            tempDataSet.append(name.get('title'))

        #get the page link
        for link in propInfo[0].find_all('a'):
            tempDataSet.append(link.get('href'))

        #add it to the list of apartments found
        apartmentScrapeList.append(tempDataSet)

#i know theres better ways to write to a .csv, but eh
scrapeOutput = open('ApartmentData/scrapedData.csv', 'w')
string = 'PRICE,ADDRESS,NAME,URL'
for x in apartmentScrapeList:
    for y in x:
        string += (y + ', ')
    string+= '\n'

scrapeOutput.write(string)
scrapeOutput.close()