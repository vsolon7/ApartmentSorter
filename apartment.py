#The apartment object. stores the relevant info for the apartment
class Apartment:
    priceWeight = .55
    sizeWeight = .45
    ratingWeight = 0

    #these are the starting values out of all the apartments. for normalization
    minP = 0
    maxP = 0
    minS = 0
    maxS = 0
    minR = 0
    maxR = 0

    def __init__(self, p, n, s, r):
        self.price = p
        self.name = n
        self.size = s
        self.rating = r

    def calculateWeight(self):
        self.nPrice = (self.price - self.minP) / (self.maxP - self.minP)
        self.nSize = (self.size - self.minS) / (self.maxS - self.minS)
        self.nRating = (self.rating - self.minR) / (self.maxR - self.minR)

        self.weightedNum = ((1-self.nPrice) * self.priceWeight) + (self.nSize * self.sizeWeight) + (
        self.nRating * self.ratingWeight)

    def setMinMax(self, miP, maP, miS, maS, miR, maR):
        self.minP = miP
        self.maxP = maP
        self.minS = miS
        self.maxS = maS
        self.minR = miR
        self.maxR = maR