"""
Created on Wed 02 Dec 00:18 2020
Finished on
@author: Cpt.Ender
                                  """
from Drawing_Module import Board


def algorithm(angle: float):
    hitPoint = Graph.lineCreator(angle)
    if hitPoint:
        Graph.pivotPoint = hitPoint
        Graph.hullPointsList.append(hitPoint)
    return hitPoint


if __name__ == "__main__":
    Graph = Board('Convex Hull Algorithm Visualization', [600, 600], 30)
    startingAngle = -89.9999
    point = []
    counter = 0
    while Graph.running():
        if point != Graph.hullPointsList[0]:
            point = algorithm(startingAngle)
            counter += 1
        else:
            Graph.draw()
        startingAngle += 0.005
        if not counter % 10:
            Graph.draw()
        # Graph.clock.tick(200)
