"""
Created on Fri 02 Oct 18:30 2020
Finished on Fri 02 Oct 19:00 2020
@author: Cpt.Ender

Floyd Warshall All Pairs Shortest Path Algorithm
                                                    """
C = 4
F = 5
lst_of_connections = [[1, 2, '10'], [1, 3, '24'], [2, 4, '15'], [2, 3, '2'], [3, 4, '7']]

minimumDistance = [[float('inf') for _ in range(C)] for _ in range(C)]

# Set each node's path to itself to 0
for vertex in range(C):
    minimumDistance[vertex][vertex] = 0

# Set the values for the weighted edges

for i in range(1, C + 1):
    for j in range(i, C + 1):
        if i != j:
            for connection in lst_of_connections:
                if connection.count(i) and connection.count(j):
                    minimumDistance[i-1][j-1] = int(connection[2])
                    minimumDistance[j-1][i-1] = int(connection[2])
                    break

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
