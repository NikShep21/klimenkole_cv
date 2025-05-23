import socket 
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops

host = "84.237.21.36"
port = 5152

def recvall(sock, n):
    data = bytearray()
    while len(data)<n:
        packet = sock.recv(n-len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    beat = b"nope"
    plt.ion()
    plt.figure()

    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)
        
        im = np.frombuffer(bts[2:], dtype="uint8").reshape(bts[0], bts[1])
        
        labeled = label(im > 200, connectivity=1)
        regions = regionprops(labeled)
        if len(regions) < 2:
            continue

        y1, x1 = regions[0].centroid
        y2, x2 = regions[1].centroid
        result = round(((y1 - y2)**2 + (x1 - x2)**2)**0.5, 1)
        sock.send(str(result).encode())
        print(sock.recv(10))
    
        plt.clf()
        plt.imshow(im, cmap='gray')
        plt.scatter([x1, x2], [y1, y2], color='red')
        plt.title(f"Distance: {result}")
        plt.pause(0.1)

        sock.send(b"beat")
        beat = sock.recv(10)
