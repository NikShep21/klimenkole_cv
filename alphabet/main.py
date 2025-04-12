
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import binary_dilation
from pathlib import Path

out_path = Path(Path(__file__).parent / "out")
out_path.mkdir(exist_ok=True)

def count_holes(region):
    shape = region.image.shape
    new_image = np.zeros((shape[0]+2, shape[1]+2))
    new_image[1:-1, 1:-1] = region.image
    new_image = np.logical_not(new_image)
    labeled = label(new_image)
    return np.max(labeled)-1

def count_vlines(region):
    return np.all(region.image, axis=0).sum()

def count_lgr_vlines(region):
    x = region.image.sum(axis=0)
    return np.sum(x[:len(x)//2]) > np.sum(x[len(x)//2:])

def regionize(region):
    if np.all(region.image):
        return "-"
    else:
        holes = count_holes(region)
        
        if holes == 2:
            _,cx  = region.centroid_local
            cx /= region.image.shape[1]
            if cx < 0.44:
                return "B"
            return "8"
        elif holes == 1:
            labeled = label(~region.image)
            num_objects = np.max(labeled)
        
            if num_objects == 4:
                return "A"
        
            if num_objects == 3:
                if region.eccentricity < 0.65:
                    return "D"
                else:
                    return "P"
            return "0"
        else:
            if count_vlines(region) >= 3:
                return "1"
            else:
                if region.eccentricity < 0.43:
                    return "*"
                inv_image = ~region.image
                inv_image = binary_dilation(inv_image,np.ones((3,3)))
                labeled = label(inv_image, connectivity = 1)
                match np.max(labeled):
                    case 2: return "/"
                    case 4: return "X"
                    case _: return "W"
    return "#"

image = plt.imread(Path(__file__).parent / "symbols.png")[:, :, :-1]
gray = image.mean(axis=2)
binary = gray > 0
labeled = label(binary)
regions = regionprops(labeled)

result = {}
plt.figure()
for i, region in enumerate(regions):
    print(f"{i+1}/{len(regions)}")
    symbol = regionize(region)
    if symbol not in result:
        result[symbol] = 0
    result[symbol] +=1
   
print(result)