import numpy as np
import skimage.io as io
from skimage.util import img_as_float32
from skimage.transform import rescale, resize, downscale_local_mean
import matplotlib.pyplot as plt
import cv2


from base.Base import Base
from helpers import Hasher


class BaseLoader(Base):
    def __init__(self, rows=None, columns=None):
        if rows is None:
            rows = 292

        if columns is None:
            columns = 348

        self.rows = rows
        self.columns = columns

    #def Load(self, file: str) -> np.ndarray:
    #    img = img_as_float32(io.imread(file, as_gray=True))
    #    img = resize(img, (self.rows, self.columns), anti_aliasing=True)
    ##    ##img[0:148,:]=0
    ##    #hh, ww = img.shape[:2]
    ##    #print(hh,' ',ww)
    ##    #hh2 = int(hh // 2)
    ##    #ww2 = int(ww // 2)

    ##    ## define circles
    ##    #radius = hh2
    ##    #yc = hh2
    ##    #xc = ww2

    ##    ## draw filled circle in white on black background as mask
    ##    #mask = np.zeros_like(img) 
    ##    #mask = cv2.circle(mask, (xc,yc), int(radius/1.2), (1,1,1), -1)
    ##    ## apply mask to image
    ##    #img = img* mask
    #    return img.reshape([self.rows, self.columns, 1])

    def Load(self, file: str) -> np.ndarray:
        color_map = plt.get_cmap('jet')
        colored_image = color_map(io.imread(file, as_gray=True))
        img=img_as_float32(colored_image[:,:,:3])
        #plt.imshow(colored_image[:,:,:3])
        #img = img_as_float32(cm(io.imread(file, as_gray=True)))
        img = resize(img, (self.rows, self.columns), anti_aliasing=True)
        #img[0:148,:]=0
        # Get the color map by name:
        #cm = plt.get_cmap('hot')

        #hh, ww = img.shape[:2]
        ##print(hh,' ',ww)
        #hh2 = int(hh // 2)
        #ww2 = int(ww // 2)

        ## define circles
        #radius = hh2
        #yc = hh2
        #xc = ww2

        ## draw filled circle in white on black background as mask
       # mask = np.zeros_like(img) 
       # mask = cv2.circle(mask, (xc,yc), int(radius/1.2), (1,1,1), -1)
        # apply mask to image
        #img = img* mask
        # Apply the colormap like a function to any array:
        #colored_image = cm(img)

        # Obtain a 4-channel image (R,G,B,A) in float [0, 1]
        # But we want to convert to RGB in uint8 and save it:
        #img=colored_image[:, :, 0] * 255#Image.fromarray((colored_image[:, :, 0] * 255).astype(np.uint8))#.save('test.png')
        #plt.imshow(xhot)
        return img.reshape([self.rows, self.columns, 3])

    def ToString(self) -> str:
        return f'BaseLoader({self.rows}x{self.columns})'

    def Description(self) -> str:
        return "Loads the image from disk as grayscale in the range [0,1] and resizes it to {self.rows} rows by {self.columns} columns."

    def AddHash(self, h:Hasher):
        h.ordered(self.__class__.__name__)
