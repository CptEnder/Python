"""
Created on Wed 30 Oct 17:05 2019
Finished on Fri 01 Nov 09:41 2019
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
max_num_of_neighbors = 6
lst = [random.randrange(2, max_num_of_neighbors, 2) for _ in range(0, Num_even_ver)] + \
      [random.randrange(3, max_num_of_neighbors, 2) for _ in range(0, Num_odd_ver)]
random.shuffle(lst)


class points:
    def __init__(self, c_i):
        self.pos = [R * math.cos(c_i * th), R * math.sin(c_i * th)]
        self.name = 'city_' + str(c_i)
        self.neigh = []
        self.num_neigh = lst[c_i]


# Creating Vertices
def vetrefication(N):
    vertices = []
    for i in range(N):
        vertices.append(points(i))
    return vertices


cities = vetrefication(Num_of_cities)


# Connecting the cities - Creating Edges
def addedge(a, b):  # a = random city, b = current city
    if a.name not in b.neigh:
        b.neigh.append(a.name)
        a.neigh.append(b.name)
        return True
    return False


S = sum(lst)
count = count2 = 0
while S > 0:
    for c in cities:
        av = []
        m = Num_of_cities
        l_c = c.neigh.__len__()
        if l_c < c.num_neigh:  # if the current city can take more neighbors
            for ci in cities:
                l = ci.neigh.__len__()
                # if the selected city is not the same as the current one
                # and it can take more neighbors
                if ci != c and l < ci.num_neigh:
                    # Appends to a list the cities with
                    # the least neighbors
                    if l < m:
                        av = [ci]
                        m = l
                    elif l == m:
                        av.append(ci)

        if av and addedge(random.choice(av), c):
            S -= 2

    count += 1
    if count > Num_of_cities * max_num_of_neighbors:
        count2 += 1
        print(count2)
        count = 0
        S = sum(lst)
        cities = vetrefication(Num_of_cities)
        remaining = 0
        for c in cities:
            remaining += c.num_neigh - c.neigh.__len__()
            if c.num_neigh > c.neigh.__len__():
                c.num_neigh -= 1
        print("Cities remaining: ", remaining)
        if remaining == 0:
            break

for c in cities:
    plt.plot(c.pos[0], c.pos[1], '.')
    for ni in c.neigh:
        plt.plot([c.pos[0], cities[int(ni[ni.__len__() - 1])].pos[0]],
                 [c.pos[1], cities[int(ni[ni.__len__() - 1])].pos[1]], '-o')
    plt.text(c.pos[0], c.pos[1] + 0.2, str(cities.index(c)) + str([c.num_neigh]))
