"""
Created on Wed 30 Sep 23:03 2020
Finished on Sat 03 Oct 11:00 2020
@author: Cpt.Ender

https://www.codechef.com/INOIPRAC/problems/INOI1402
Indian National Olympiad in Informatics 2014
Nikhil’s slogan has won the contest conducted by Drongo Airlines and
he is entitled to a free ticket between any two destinations served by the airline.
All cities served by Drongo Airlines can be reached from each other by some sequence of connecting flights.
Nikhil is allowed to take as many connecting flights as needed,
but he must take the cheapest route between his chosen destinations.

Each direct flight between two cities has a fixed price.
All pairs of cities connected by direct flights have flights in both directions
and the price is the same in either direction.
The price for a sequence of connecting flights is the sum of the prices of the direct flights along the route.

Nikhil has information about the cost of each direct flight.
He would like to maximize the value of his prize,
so he would like to choose a pair of cities on the network
for which the cost of the cheapest route is as high as possible.

For instance, suppose the network consists of four cities {1, 2, 3, 4}, connected as shown on the right.

In this case, Nikhil should choose to travel between 1 and 4,
where the cheapest route has cost 19. You can check that for all other pairs of cities,
the cheapest route has a smaller cost. For instance,
notice that though the direct flight from 1 to 3 costs 24,
there is a cheaper route of cost 12 from 1 to 2 to 3.

Sample Input:
4 5
1 2 10
1 3 24
2 3 2
2 4 15
3 4 7
Sample Output:
19

                                  """
_in = input().split(' ')
C = int(_in[0])
F = int(_in[1])

minimumDistance = [[float('inf') for _ in range(C)] for _ in range(C)]

# Set each node's path to itself to 0
for vertex in range(C):
    minimumDistance[vertex][vertex] = 0

# Set the values for the weighted edges
for _ in range(F):
    _in = input().split(' ')
    x, y, p = int(_in[0]) - 1, int(_in[1]) - 1, int(_in[2])
    minimumDistance[x][y] = p
    minimumDistance[y][x] = p

for i in range(C):
    for j in range(C):
        for k in range(C):
            if minimumDistance[i][k] != float('inf') and minimumDistance[j][i] != float('inf'):
                if minimumDistance[j][k] > minimumDistance[j][i] + minimumDistance[i][k]:
                    minimumDistance[j][k] = minimumDistance[j][i] + minimumDistance[i][k]

maximumCheapestCost = -float('inf')
for row in minimumDistance:
    if maximumCheapestCost < max(row):
        maximumCheapestCost = max(row)

print(maximumCheapestCost)
