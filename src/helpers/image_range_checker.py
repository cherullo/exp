import os
import arch
from loaders import BaseLoader
import numpy as np
import matplotlib.pyplot as plt
from arch.config import get_images_path

class PathIterator():
    def __init__(self, path):
        self.n = -1
        self.path = path
        self.basenames = os.listdir( path )
    
    def __iter__(self):
        self.n = -1
        return self
    
    def __next__(self):
        self.n = self.n + 1
        
        if (self.n >= len(self.basenames)):
            raise StopIteration
        
        current_base = self.basenames[self.n]
        current_full = os.path.join(self.path, current_base)
        
        if os.path.isdir(current_full): 
            return self.__next__()
                    
        return ( current_base, current_full )


iter = PathIterator( get_images_path() )

ranges=[]
bs = BaseLoader()

for i, (base, file) in enumerate(iter):
    img = bs.Load(file)
    ranges.append(np.amax(img) - np.amin(img))

    if i % 100 == 0:
        print(i)

plt.hist(ranges, bins=40)

plt.show()