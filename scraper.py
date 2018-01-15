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

#open the page(s) and add the HTML to pages to scrape. then make it a BS object
c = 0
for URL in URLsToScrape:
    c += 1
    client = urllib.request.urlopen(URL)
    rawSource = client.read()
    bsPages.append(bs.BeautifulSoup(rawSource, 'lxml'))
    client.close()
    print('Loaded URL #', c, '!', sep='')

#so in this, the outer loop goes through all the beautiful soup pages. the inner loop looks through everything
#and stores it.
c = 0
for page in bsPages:
    #this is a regular expression. it finds everything that begins with "level". their site was weird and they all started with different things
    allListings = page.find_all("div", {"class":re.compile("^level")})

    #goes through every listing in the list of all apartment listings. lol.
    for listing in allListings:
        c += 1
        #this will store the data for a single apartment. will later be appended to a list of lists that has all apartments
        tempDataSet = []
        #regular expressions are so good
        propInfo = listing.find_all("div", {"class":re.compile("^propertyInfo xs-")})[0]

        #get the rent. i opted to just grab the cheapest one, also i removed commas
        rent = propInfo.find_all("span", {"class": "altRentDisplay"})[0].text.strip().replace(',', '')
        rent = rent.split(' -', 1)[0]
        rent = rent.split('$',1)[1]

        # get the city
        city = propInfo.find_all("span", {"itemprop": "addressLocality"})[0].text.strip()

        #get the address, i removed the commas to help put it in a .csv
        address = propInfo.find_all("span", {"itemprop":"address"})[0].text.strip().replace(',', '')

        #get the name of the post
        name = ''
        for na in propInfo.find_all('a'):
           name = na.get('title')

        #get the link to the actual main apartment page
        link = ''
        for li in propInfo.find_all('a'):
            link = li.get('href')

        #now we open the link to get the square footage and possible extra data.
        client = urllib.request.urlopen(link)
        subPage = client.read()
        client.close()
        SPBS = bs.BeautifulSoup(subPage, 'lxml')

        #narrow the search a bit because when I did it before, I got square footage from tons of other apartment sizes
        narrowedSearch = SPBS.find("div", {"data-beds":"2"})
        squareFeet = narrowedSearch.find("div", "xs-12 md-4 sqft").text.strip().replace(',','')
        squareFeet = squareFeet.split(' ',1)[0]

        tempDataSet.append(rent)
        tempDataSet.append(squareFeet)
        tempDataSet.append(city)
        tempDataSet.append(address)
        tempDataSet.append(link)
        tempDataSet.append(name)
        #add it to the list of apartments found
        apartmentScrapeList.append(tempDataSet)

        #a little info to tell us when we're done with each apartment
        print('Apartment #', c, ' done!', sep='')

#i know there's better ways to write to a .csv, but eh
scrapeOutput = open('ApartmentData/scrapedData.csv', 'w')
string = 'RENT,SQUARE FEET,CITY,ADDRESS,URL,NAME'
for x in apartmentScrapeList:
    for y in x:
        string += (y + ', ')
    string+= '\n'

scrapeOutput.write(string)
scrapeOutput.close()