import os
import sys
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
sys.path.append('..')
from tensorflow import keras 

from tensorflow.keras.applications.imagenet_utils import decode_predictions

#from efficientnet.keras import EfficientNetB0
#from efficientnet.keras import center_crop_and_resize, preprocess_input

## if you use tensorflow.keras: 
from efficientnet.tfkeras import EfficientNetB0
from efficientnet.tfkeras import center_crop_and_resize, preprocess_input

# test image
image = imread('C:/Users/gusma/Downloads/paper.jpg')
plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.show()

# loading pretrained model. weights must receive path to trained model or imagenet
model = EfficientNetB0(weights='C:/Users/gusma/Documents/projects/fetal_echo_classifier/RPS_model_20ep.h5')

# preprocess input
image_size = model.input_shape[1]
x = center_crop_and_resize(image, image_size=image_size)
x = preprocess_input(x)
x = np.expand_dims(x, 0)


# make prediction and decode
y = model.predict(x)
print(y)
#for imaginet decoding
#print(decode_predictions(y))