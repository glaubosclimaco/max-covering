from ast import arg
import csv
from sys import argv
import gurobipy as grb
import numpy as np
from scipy.spatial import distance
import Point

 
points = []

nPoints = 0  # number of rows in the input file
nFields = 6  # number of columns in the input file
with open('bairros.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        points.append(Point.Point(
            int(nPoints), row[0], row[1], row[2], float(row[3]), float(row[4])))
        nPoints += 1


distanceMatrix = np.zeros((nPoints, nPoints))

# compute euclidian distance between points

for i in range(nPoints):
    for j in range(nPoints):
        if i != j:
            p1 = (points[i].coordinatesX, points[i].coordinatesY)
            p2 = (points[j].coordinatesX, points[j].coordinatesY)
            # 100* to normalize the distance
            distanceMatrix[i][j] = 100 * distance.euclidean(p1, p2)


# print(distanceMatrix)

# print(np.average(distanceMatrix))  # compute average distance


# GUROBI

def solver(K, level):

    # K=2 # number of points
    # coverageDistance= np.average(distanceMatrix) # distance threshold
    avgDistance = np.average(distanceMatrix)
    coverageDistance = avgDistance/ float(level)

    model = grb.Model()

    ### variables ###
    x = {}
    y = {}
    aMap = {}  # map of points to real locations
    for i in range(nPoints):
        x[i] = model.addVar(vtype=grb.GRB.BINARY, name='x_'+str(points[i].id))
        y[i] = model.addVar(vtype=grb.GRB.BINARY, name='y_'+str(points[i].id))
        aMap['x_'+str(points[i].id)] = points[i].id

    ### objective function ###
    foj = grb.quicksum(y[i] for i in range(nPoints))
    model.setObjective(foj, sense=grb.GRB.MAXIMIZE)

    ### constraints ###

    sum = 0
    for i in range(nPoints):
        sum = sum+x[i]
    model.addConstr(sum == K)

    for i in range(nPoints):
        sum = 0
        empty = True
        for j in range(nPoints):
            if i != j:
                if distanceMatrix[i][j] <= coverageDistance:
                    sum = sum+x[j]
                    empty = False
        if empty == False:
            model.addConstr(sum >= y[i])

    model.update()
    model.write("max-covering-SJC.lp")
    model.optimize()

    model.write("max-covering-SJC.sol")

    # printing the solution
    #print line
    print("\nFacilities:\n")
    for v in x.values():
        if(v.X == 1):
            id = int(v.varName.split('_')[1])
            print('Point: {}'.format(id))
            print(points[id].neighborhoods)
            print("\n")

    print("\nCovered:")
    for v in y.values():
        if(v.X == 1):
            id = int(v.varName.split('_')[1])
            print('Point {} '.format(id),end = "\t ")


# main function
if __name__ == "__main__":
  # run solver with input parameters
  args = argv[1:]
  if len(args) == 2:
    solver(int(args[0]), int(args[1]))
  else:
    print('Usage: python3 max-covering-SJC.py K (0 < k <='+ str(nPoints) + ') level (0 < level <= 3)')



