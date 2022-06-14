
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

  def __repr__(self):
    return self.__str__()
  
  def __eq__(self, other):
    return self.id == other.id
  
  def __hash__(self):
    return hash(self.id)
  
  def __lt__(self, other):
    return self.id < other.id

  def __gt__(self, other):
    return self.id > other.id
  
  def __le__(self, other):
    return self.id <= other.id

  def __ge__(self, other):
    return self.id >= other.id

  def __ne__(self, other):
    return self.id != other.id

  def __cmp__(self, other):
        return self.id - other.id