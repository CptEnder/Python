"""
Created on Mon 03 Aug 12:03 2020
Finished on
@author: Cpt.Ender
                                  """
from matplotlib import pyplot as plt
import perlin_noise as perl
import noise

width = 100
height = 100
points = [[], [], []]
for i in range(width):
    for j in range(height):
        # color = [perl.scale(noise.pnoise2(i / width * 6, j / width * 6, 100), -1, 1, 0, 1)] * 3
        # color = [perl.scale(perl.perlin(i/width*6, j/width*6, 100), -1, 1, 0, 1)] * 3
        # color = 0
        # a = 1
        # f = 0.0005
        # for octave in range(8):
        #     v = a * perl.perlin2D(i * f, j * f)
        #     color += v
        #     a *= 0.5
        #     f *= 2
        PNF = perl.PerlinNoiseFactory(2, 2)
        color = [perl.scale(PNF(i + 0.1, j + 0.1), -1, 1, 0, 1)] * 3
        points[0].append(i)
        points[1].append(j)
        points[2].append(color)
        # print(color)

plt.scatter(points[0], points[1], color=points[2])

plt.show()
# pygame.init()
# pygame.display.set_caption("Noise Visualization.py")
# scrn = pygame.display.set_mode((width, height))
# pygame.mouse.set_visible(True)
# clock = pygame.time.Clock()
# def running():
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             return False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_ESCAPE:
#                 return False
#     return True
#
#
# def draw():
#     scrn.fill(black)  # Background Colour
#     for p in points:
#         pygame.draw.ellipse(scrn, p[2], [p[0], p[1], 1, 1])
#     pygame.display.update()
#
#
# draw()
# while running():
#     pass
#
# pygame.quit()
