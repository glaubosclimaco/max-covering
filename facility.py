class Facility:
  def __init__(region, population, neighborhoods, coordinatesX, coordinatesY):
    self.region = region
    self.population = population
    self.neighborhoods = neighborhoods
    self.coordinatesX = coordinatesX
    self.coordinatesY = coordinatesY

  def __str__(self):
    return "Facility(region={}, population={}, neighborhoods={}, coordinatesX={}, coordinatesY={})".format(self.region, self.population, self.neighborhoods, self.coordinatesX, self.coordinatesY)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    return self.region == other.region and self.population == other.population and self.neighborhoods == other.neighborhoods and self.coordinatesX == other.coordinatesX and self.coordinatesY == other.coordinatesY

  def __hash__(self):
    return hash(self.__str__())

  def __lt__(self, other):
    return self.population < other.population