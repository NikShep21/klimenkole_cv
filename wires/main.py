import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_opening, binary_dilation, binary_erosion)

data = np.load("wires6npy.txt")

labeled = label(data)
struct_elem = np.ones((3, 1))
    
for i in range(1, np.max(labeled)+1):
    wires = (labeled==i)
    erosionWires = binary_erosion(wires, struct_elem)
    newWires = label(erosionWires)
    if np.max(newWires) == np.max(wires):
        print(f'у провода {i} нет разрывов')
    elif np.max(newWires) < np.max(wires):
        print('провода не существует')
    else:
        print( f"у провода {i} {np.max(newWires)-np.max(wires)} разрывов")