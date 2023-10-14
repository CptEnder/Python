"""
Created on Tue 01 Dec 17:17 2020
Finished on Thu
@author: Cpt.Ender
                                  """
import pygame
import math
from random import randint as rint


class Board:
    def __init__(self, name, win_size: list, numOfPoints: int):
        pygame.init()
        self.window_size = win_size
        self.game_size = [self.window_size[0] + 1, self.window_size[1] + 1]
        self.name = name
        pygame.display.set_caption(self.name)
        self.scrn = pygame.display.set_mode(self.game_size)
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()
        self.black = [0] * 3
        self.white = [200] * 3
        self.innerRectangle = [[self.game_size[0] // 6, self.game_size[1] // 6],
                               [self.game_size[0] * 5 // 6, self.game_size[1] * 5 // 6]]
        self.pointsList = [[rint(self.innerRectangle[0][0], self.innerRectangle[1][0]),
                            rint(self.innerRectangle[0][1], self.innerRectangle[1][1])] for _ in range(numOfPoints)]
        # self.pointsList.append([300, 100])
        # self.pointsList.append([15, 100])
        # self.pointsList.append([100, 100])

        self.pivotPoint = self.leftMostPoint()
        self.hitPoint = []
        self.hullPointsList = [self.pivotPoint]

    def leftMostPoint(self):
        tempPoint = self.pointsList[0]
        for point in self.pointsList:
            if point[0] < tempPoint[0]:
                tempPoint = point
        return tempPoint

    def lineCreator(self, angle: float):
        angle = math.radians(angle)
        slope = math.tan(angle)
        b = self.pivotPoint[1] - slope * self.pivotPoint[0]

        self.hitPoint = []
        maxDistance = 1000
        maxPoint = [self.pivotPoint[0] + math.cos(angle) * 1000,
                    self.pivotPoint[1] + math.sin(angle) * 1000]
        for point in self.pointsList:
            if abs(point[1] - slope * point[0] - b) <= 0.2 and point != self.pivotPoint:
                if (maxPoint[0] >= self.pivotPoint[0] and self.pivotPoint[0] <= point[0] <= maxPoint[0]) or \
                        (maxPoint[0] <= self.pivotPoint[0] and self.pivotPoint[0] >= point[0] >= maxPoint[0]):
                    tempDistance = math.sqrt(
                        (self.pivotPoint[0] - point[0]) ** 2 + (self.pivotPoint[1] - point[1]) ** 2)
                    if tempDistance <= maxDistance:
                        self.hitPoint = point
                        maxDistance = tempDistance
                        # break
        if not self.hitPoint:
            self.hitPoint = [self.pivotPoint[0] + math.cos(angle) * 1000,
                             self.pivotPoint[1] + math.sin(angle) * 1000]
            return False
        else:
            return self.hitPoint

    def running(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        return True

    def draw(self):
        self.scrn.fill(self.white)  # Background Colour

        for point in self.pointsList:
            pygame.draw.circle(self.scrn, self.black, point, 2)

        if self.hitPoint:
            pygame.draw.aaline(self.scrn, self.black, self.pivotPoint, self.hitPoint)

        for i in range(len(self.hullPointsList) - 1):
            pointA = self.hullPointsList[i]
            pointB = self.hullPointsList[i + 1]
            pygame.draw.aaline(self.scrn, self.black, pointA, pointB)

        pygame.display.update()
