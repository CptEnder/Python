"""
Created on Mon 05 Oct 20:33 2020
Finished on
@author: Cpt.Ender
                                  """
import math
import random
import matplotlib.pyplot as plt

plt.close()

Num_of_cities = 5
R = 5
th = 2 * math.pi / Num_of_cities
Num_odd_ver = random.randrange(0, Num_of_cities, 2)  # Number of vertices of odd order
Num_even_ver = Num_of_cities - Num_odd_ver  # Number of vertices of even order
max_num_of_neighbors = Num_of_cities
lst = [random.randrange(2, max_num_of_neighbors, 2) for _ in range(0, Num_even_ver)] + \
      [random.randrange(3, max_num_of_neighbors, 2) for _ in range(0, Num_odd_ver)]
random.shuffle(lst)


class point:
    def __init__(self, c_i):
        self.pos = [R * math.cos(c_i * th), R * math.sin(c_i * th)]
        # self.name = 'city_' + str(c_i)
        self.neigh = []
        self.num_neigh = lst[c_i]


# Creating Vertices
def vetrefication(N):
    vertices = []
    for i in range(N):
        vertices.append(point(i))
    return vertices


# Connecting the cities - Creating Edges
def addedge(a, b):  # a = random city, b = current city
    if a.name not in b.neigh:
        b.neigh.append(a.name)
        a.neigh.append(b.name)
        return True
    return False


# def numOfNeighbors():
#     city: point
#     return city.num_neigh


cities = vetrefication(Num_of_cities)

# Plot the Graph
for c in cities:
    plt.plot(c.pos[0], c.pos[1], '.')
    plt.text(c.pos[0], c.pos[1] + 0.2, str(cities.index(c)) + str([c.num_neigh]))

# cities.sort(key=numOfNeighbors())
