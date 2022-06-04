import csv
from dis import dis
import math
import gurobipy as grb
import numpy as np
from pkg_resources import add_activation_listener
from scipy.spatial import distance


class Point:
  def __init__(self,id,region, population, neighborhoods, coordinatesX, coordinatesY):
    self.id = id
    self.region = region
    self.population = population
    self.neighborhoods = neighborhoods
    self.coordinatesX = coordinatesX
    self.coordinatesY = coordinatesY

  def __str__(self):
    return "Point(region={}, population={}, neighborhoods={}, coordinatesX={}, coordinatesY={})".format(self.region, self.population, self.neighborhoods, self.coordinatesX, self.coordinatesY)



# arq = open("bairros.txt", 'r')

points=[]

nPoints = 0  # number of rows in the input file
nFields=6 # number of columns in the input file
with open('bairros.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        points.append(Point(int(nPoints),row[0], row[1], row[2], float(row[3]), float(row[4])))
        nPoints += 1
        

distanceMatrix = np.zeros((nPoints, nPoints))

# compute euclidian distance between points

for i in range(nPoints):
      for j in range(nPoints):
          if i != j:
                p1 = (points[i].coordinatesX, points[i].coordinatesY)
                p2 = (points[j].coordinatesX, points[j].coordinatesY)
                distanceMatrix[i][j] = 100* distance.euclidean(p1, p2) # 100* to normalize the distance
             
            
print(distanceMatrix)

print(np.average(distanceMatrix))  # compute average distance


# GUROBI

def solver(K, coverageDistance):

  # K=2 # number of points
  # coverageDistance= np.average(distanceMatrix) # distance threshold

  model = grb.Model()

  ### variables ###   
  x={}
  y={}
  aMap={} # map of points to real locations
  for i in range(nPoints):
    x[i] = model.addVar(vtype=grb.GRB.BINARY, name='x_'+str(points[i].id))
    y[i] = model.addVar(vtype=grb.GRB.BINARY, name='y_'+str(points[i].id))
    aMap['x_'+str(points[i].id)] = points[i].id


  ### objective function ###
  foj =   grb.quicksum(y[i] for i in range(nPoints))
  model.setObjective(foj, sense=grb.GRB.MAXIMIZE)

  ### constraints ###

  sum=0
  for i in range(nPoints):
    sum=sum+x[i]
  model.addConstr(sum==K)


  for i in range(nPoints):
    sum=0
    empty=True
    for j in range(nPoints):
        if i != j:
          if distanceMatrix[i][j] <= coverageDistance:
                sum=sum+x[j]
                empty=False
    if empty==False:
      model.addConstr(sum>=y[i])
    

  model.update()
  model.write("max-covering-SJC.lp")
  model.optimize()

  model.write("max-covering-SJC.sol")

  # printing the solution
  print("Facilities:")
  for v in x.values():
    if(v.X==1):
      print("{}:\t{}".format(v.varName, v.X))
      id = int(v.varName.split('_')[1])
      print(points[id].neighborhoods)

  print("Covered:")
  for v in y.values():
    if(v.X==1):
      print("{}:\t{}".format(v.varName, v.X))
   


solver(2, np.average(distanceMatrix))