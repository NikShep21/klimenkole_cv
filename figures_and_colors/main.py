import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import label
from collections import defaultdict
from skimage.measure import regionprops

image = plt.imread('balls_and_rects.png')

pixels = image.reshape(-1, image.shape[2])
unique_colors = np.unique(pixels, axis=0)
unique_colors = [tuple(c) for c in unique_colors if not np.all(c == 0)]

circles_color = defaultdict(int)
rectangles_color = defaultdict(int)

for color in unique_colors:
    mask = np.all(image == color, axis=-1)
    labeled = label(mask)

    for region in regionprops(labeled):
        if region.eccentricity < 0.01:
            circles_color[color] += 1
        else:
            rectangles_color[color] += 1

total_circles = sum(circles_color.values())
total_rectangles = sum(rectangles_color.values())
total_shapes = total_circles + total_rectangles

print(f'Total number of shapes: {total_shapes}')
print(f'Total number of circles: {total_circles}')
print(f'Total number of rectangles: {total_rectangles}\n')

print('Circles by color:')
for color, count in circles_color.items():
    print(f'  Color {color}: {count}')

print('\nRectangles by color:')
for color, count in rectangles_color.items():
    print(f'  Color {color}: {count}')