#The apartment object. stores the relevant info for the apartment
class Apartment:
    priceWeight = .55
    sizeWeight = .45
    ratingWeight = 0

    def __init__(self, p, s, c, a, u, n):
        self.price = p
        self.size = s
        self.city = c
        self.address = a
        self.url = u
        self.name = n


    def calculateWeight(self):
        self.weightedNum = self.price / self.size