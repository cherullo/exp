import numpy as np
import tensorflow_datasets as tfds
import tensorflow as tf
from tensorflow import keras 
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications.imagenet_utils import decode_predictions

#from efficientnet.keras import EfficientNetB0
#from efficientnet.keras import center_crop_and_resize, preprocess_input

## if you use tensorflow.keras: 
from efficientnet.tfkeras import EfficientNetB0
from efficientnet.tfkeras import center_crop_and_resize, preprocess_input

#Load dataset from tensorflow
dataset = tfds.load('rock_paper_scissors')

#This dataset can be broken in train and test groups
train, test = dataset['train'], dataset['test']

#Convert MapDataset to Numpy Array
train_numpy = np.vstack(tfds.as_numpy(train))
test_numpy = np.vstack(tfds.as_numpy(test))
print(train_numpy.shape)
X_train = np.array(list(map(lambda x: x[0]['image'], train_numpy)))
y_train = np.array(list(map(lambda x: x[0]['label'], train_numpy)))
print(X_train.shape)
X_test = np.array(list(map(lambda x: x[0]['image'], test_numpy)))
y_test = np.array(list(map(lambda x: x[0]['label'], test_numpy)))

#Preprocessing image
X_train=X_train.astype('float32')
X_train=X_train/255.0
y_train=y_train.astype('float32')
#print(X_train, y_train)

# one hot encode target values
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

print(X_train.shape)
# Calling EfficientNet model. For training must use weights=None, default input shape is (224,224,3)
model = EfficientNetB0(weights=None,input_shape=(300,300,3),classes=3)

model.compile(loss='categorical_crossentropy', optimizer='adam', 
    metrics=['acc'])
model.summary()
history = model.fit(X_train, y_train, batch_size=10,epochs=20, verbose=0)

# save model
model.save('RPS_model_20ep.h5')

#evaluate
test_acc = model.evaluate(X_test,  y_test, verbose=0)
print('\nTest accuracy:', test_acc)

