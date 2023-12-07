from exp.arch import Experiment
from exp.loaders import BrightLoader, SimpleLoader, RotationLoader
from exp.models import EfficientNetB0Model
from exp.preprocessing_steps import FilterColumn, FirstPercent, LastPercent

import columns
import labels

dimension = (128, 128)

exp = Experiment()

# Load the dataset
exp.input = 'dataset/animals.xlsx'

# Only keep lines containing cows and sheeps
exp.preprocessing_steps = [
    FilterColumn(columns.LABEL, labels.ALL),
    ]

# Add the first 80% of cow images to the training set, applying a different random rotation between -10 and 10 degrees to each image, every training epoch.
exp.add_train_set([FilterColumn(columns.LABEL, [labels.COW]), FirstPercent(0.8)], RotationLoader(resize=dimension, spread=10.0))
# Add the first 80% of sheep images to the training set, applying a different random rotation between -10 and 10 degrees to each image, every training epoch.
exp.add_train_set([FilterColumn(columns.LABEL, [labels.SHEEP]), FirstPercent(0.8)], RotationLoader(resize=dimension, spread=10.0))
# Add the first 80% of squirrel images to the training set, applying a different random rotation between -10 and 10 degrees to each image, every training epoch.
exp.add_train_set([FilterColumn(columns.LABEL, [labels.SQUIRREL]), FirstPercent(0.8)], RotationLoader(resize=dimension, spread=10.0))
# Add the first 80% of butterfly images to the training set, applying a different random rotation between -10 and 10 degrees to each image, every training epoch.
exp.add_train_set([FilterColumn(columns.LABEL, [labels.BUTTERFLY]), FirstPercent(0.2)], RotationLoader(resize=dimension, angle=-10.0), RotationLoader(resize=dimension, angle=+10.0), BrightLoader(resize=dimension, alpha=0.8))

# Add the last 20% of cow images to the validation set, without augmentation
exp.add_validation_set([FilterColumn(columns.LABEL, [labels.COW]), LastPercent(0.2)], SimpleLoader(resize=dimension))
# Add the last 20% of sheep images to the validation set, without augmentation
exp.add_validation_set([FilterColumn(columns.LABEL, [labels.SHEEP]), LastPercent(0.2)], SimpleLoader(resize=dimension))
# Add the last 20% of squirrel images to the validation set, without augmentation
exp.add_validation_set([FilterColumn(columns.LABEL, [labels.SQUIRREL]), LastPercent(0.2)], SimpleLoader(resize=dimension))
# Add the last 20% of butterfly images to the validation set, without augmentation
exp.add_validation_set([FilterColumn(columns.LABEL, [labels.BUTTERFLY]), LastPercent(0.2)], SimpleLoader(resize=dimension))

# Configure the base path from where images will be loaded
exp.base_images_path = "dataset/"
# Configure which column of the dataset contains the image file path
exp.image_column = columns.FILE
# Configure which column of the dataset contains the image label
exp.label_column = columns.LABEL

# Load EfficientNetB0 model
exp.model = EfficientNetB0Model()
# Train for 150 epochs
exp.epochs = 150
exp.run()
