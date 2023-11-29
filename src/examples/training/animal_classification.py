from arch import Experiment
from loaders import BaseLoader, RotationLoader
from models import OneHot
from models.EfficientNetB0Model import EfficientNetB0Model
from preprocessing_steps import FilterColumn, FirstPercent, LastPercent

import columns
import labels

exp = Experiment()

exp.input = 'dataset/animals.xlsx'

exp.preprocessing_steps = [
    FilterColumn(columns.LABEL, [labels.COW, labels.SHEEP]),
    ]

exp.add_train_set([FilterColumn(columns.LABEL, [labels.COW]), FirstPercent(0.8)], RotationLoader(spread=10.0))
exp.add_train_set([FilterColumn(columns.LABEL, [labels.SHEEP]), FirstPercent(0.8)], RotationLoader(spread=10.0))

exp.add_test_set([FilterColumn(columns.LABEL, [labels.COW]), LastPercent(0.2)], RotationLoader(spread=10.0))
exp.add_test_set([FilterColumn(columns.LABEL, [labels.SHEEP]), LastPercent(0.2)], RotationLoader(spread=10.0))

exp.encoding = OneHot([labels.COW, labels.SHEEP])

exp.base_images_path = "dataset/"
exp.image_column = columns.FILE
exp.label_column = columns.LABEL
exp.model = EfficientNetB0Model()
exp.run()
