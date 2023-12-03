from arch import Experiment
from loaders import BaseLoader, RotationLoader
from models import OneHot
from models.EfficientNetB0Model import EfficientNetB0Model
from preprocessing_steps import FilterColumn, FirstPercent, LastPercent

import columns
import labels

dimension = (128, 128)

exp = Experiment()

# Load the dataset
exp.input = 'dataset/animals.xlsx'

# Only keep lines containing cows and sheeps
exp.preprocessing_steps = [
    FilterColumn(columns.LABEL, [labels.COW, labels.SHEEP]),
    ]

# Add the first 80% of cow images to the training set, applying a different random rotation between -10 and 10 degrees to each image, every training epoch.
exp.add_train_set([FilterColumn(columns.LABEL, [labels.COW]), FirstPercent(0.8)], RotationLoader(resize=dimension, spread=10.0))
# Add the first 80% of sheep images to the training set, applying a different random rotation between -10 and 10 degrees to each image, every training epoch.
exp.add_train_set([FilterColumn(columns.LABEL, [labels.SHEEP]), FirstPercent(0.8)], RotationLoader(resize=dimension, spread=10.0))

# Add the last 20% of cow images to the validation set, without augmentation
exp.add_validation_set([FilterColumn(columns.LABEL, [labels.COW]), LastPercent(0.2)], BaseLoader(resize=dimension))
# Add the last 20% of sheep images to the validation set, without augmentation
exp.add_validation_set([FilterColumn(columns.LABEL, [labels.SHEEP]), LastPercent(0.2)], BaseLoader(resize=dimension))

# Use OneHot encoding for the labels ([1, 0] and [0, 1])
exp.encoding = OneHot([labels.COW, labels.SHEEP])

# Configure the base path from where images will be loaded
exp.base_images_path = "dataset/"
# Configure which column of the dataset contains the image file path
exp.image_column = columns.FILE
# Configure which column of the dataset contains the image label
exp.label_column = columns.LABEL

# Load EfficientNetB0 model
exp.model = EfficientNetB0Model()
# Train for 20 epochs
exp.epochs = 20
#
exp.run()
