import numpy as np
import matplotlib.pyplot as plt

external = np.array([
    [[0,0],[0,1]],
    [[0,0],[1,0]],
    [[0,1],[0,0]],
    [[1,0],[0,0]]

]) 

internal = np.logical_not(external)
cross = np.array([
    [[0,1],[1,0]],
    [[1,0],[0,1]]
])

def match(sub,masks):
    for mask in masks:
        if np.all(mask == (sub!=0)):
            return True
    return False
def count_objects(image):
    E = 0
    I = 0
    for y in range(0,image.shape[0]-1):
        for x in range(0,image.shape[1]-1):
            sub = image[y:y+2, x:x+2]
            if match(sub, internal):
                I += 1
            elif match(sub,external):
                E += 1
            elif match(sub,cross):
                E += 2
    return (E-I)/4


image = np.load("example2.npy")
if len(image.shape) == 3:
    
    result = np.sum([count_objects(image[:, :, i]) for i in range(image.shape[2])])
else:
    result = count_objects(image)

plt.imshow(image)
plt.show()
print(result)