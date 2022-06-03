import csv

class Facility:
  def __init__(self,region, population, neighborhoods, coordinatesX, coordinatesY):
    self.region = region
    self.population = population
    self.neighborhoods = neighborhoods
    self.coordinatesX = coordinatesX
    self.coordinatesY = coordinatesY

  def __str__(self):
    return "Facility(region={}, population={}, neighborhoods={}, coordinatesX={}, coordinatesY={})".format(self.region, self.population, self.neighborhoods, self.coordinatesX, self.coordinatesY)



# arq = open("bairros.txt", 'r')

facilities=[]

# for line in arq:
#     splitLine = line.split(',')
#     print(splitLine)
#     region = splitLine[0]
#     population = float(splitLine[1])
#     neighborhoods = splitLine[2]
#     coordinatesX = float(splitLine[3])
#     coordinatesY = float(splitLine[4])
#     facilities.append(Facility(region, population, neighborhoods, coordinatesX, coordinatesY))

with open('bairros.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(row)
        region = row[0]
        population = float(row[1])
        neighborhoods = row[2]
        coordinatesX = float(row[3])
        coordinatesY = float(row[4])
        facilities.append(Facility(region, population, neighborhoods, coordinatesX, coordinatesY))



for i in facilities:
    print(i)
