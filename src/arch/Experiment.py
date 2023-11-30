import time
from contextlib import redirect_stdout

import pandas
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Tuple
from sklearn.metrics import classification_report, confusion_matrix

from arch import Hasher
from helpers import main_helper
from loaders import BaseLoader
from arch import Step
from models.OneHot import OneHot

from .SampleExtractor import SampleExtractor
from .ReportPath import ReportPath
from .DatasetGenerator import DatasetGenerator
from arch import config
import arch.dataset_columns as dataset_columns

def _process_steps(df: pandas.DataFrame, steps:List[Step]) -> pandas.DataFrame:
    for step in steps:
        df = step.process(df)

    return df

def _generate_histogram(df: pandas.DataFrame, group_col:str): #, sum_col:str):
    hist = df.groupby(group_col).count() # [sum_col].agg('sum')
    hist.sort_index(axis=0, inplace=True)

    return hist

def _generate_dataset_histogram(df: pandas.DataFrame):
    columns = df[dataset_columns.INPUT_LOADER].unique() 
    columns = np.unique([str(input) for input in columns])
    indexes = df[dataset_columns.OUTPUT].unique()

    ret = pandas.DataFrame(columns=columns, index=indexes)
    ret.sort_index(axis=0, inplace=True)
    ret.sort_index(axis=1, inplace=True)

    counts = df.groupby([ dataset_columns.OUTPUT, dataset_columns.INPUT_LOADER ]).count()

    for index, row in counts.iterrows():
        ret.loc[ [index[0]], [str(index[1])] ] = row[dataset_columns.INPUT]

    return ret

class Experiment():

    def __init__(self, name:str = None):
        self.name = name or main_helper.get_main_basename_extless();
        
        self.base_images_path = None
        self.base_report_path = 'reports/'
        self.report_path = None
        self.str_hash = None
        self.str_final_hash = None

        self.input = None
        self.image_column = None
        self.label_column = None
        self.preprocessing_steps: List[Step] = []
        self.validation_sets: List(List[Step], Tuple[BaseLoader]) = []
        self.validation_set = None
        self.validation_set_generator = None

        self.train_sets: List(List[Step], Tuple[BaseLoader]) = []
        self.train_set = None
        self.train_set_generator = None

        self.model = None
        self.encoding = None

    def add_train_set( self, steps:List[Step], *loaders: BaseLoader ):
        self.train_sets.append( (steps, loaders) )

    def add_validation_set( self, steps:List[Step], *loaders: BaseLoader ):
        self.validation_sets.append(  (steps, loaders) )

    def _print_dry_warning(self):
        print('-------------------------')
        print('--- THIS IS A DRY RUN ---')
        print('--- THIS IS A DRY RUN ---')
        print('--- THIS IS A DRY RUN ---')
        print('-------------------------')
        time.sleep(3)


    def run(self, dry = False):
        if (dry == True):
            self._print_dry_warning()
        self.str_hash = str( self.hash() )
        self.base_images_path = self.base_images_path or config.get_images_path()
        self.report_path = ReportPath(self.base_report_path, f'{self.name}-{self.str_hash}')

        print (f'Starting experiment {self.name}-{self.str_hash}')
        print (f'Image path: {self.base_images_path}')

        # Load source XLS file
        df: pandas.DataFrame = pandas.read_excel(self.input,engine = 'openpyxl')

        # Apply preprocessing steps
        df = _process_steps(df, self.preprocessing_steps)

        # Save preprocesssed XLS
        df.to_excel(self.report_path.get('preprocessed.xlsx'))

        # Generate preprocessed histogram
        # hist = _generate_histogram(df, self.label_column)

        # hist.plot(kind='bar')

        # for index, row in enumerate(hist.iterrows()):
        #     label, row = row
        #     plt.text(index, row[self.image_column], str(label), ha='center')

        # plt.savefig(self.report_path.get('preprocessed_histogram.png'), dpi=200)

        # Generate validation set
        if (len(self.validation_sets) > 0):
            print ("Creating validation set")
            self.validation_set = self._extract_sets(df.copy(deep=True), self.validation_sets)

            # Remove duplicates from validation set
            self.validation_set.drop_duplicates(subset=dataset_columns.INPUT, inplace=True)

            self.validation_set.to_excel(self.report_path.get('validation_set.xlsx'))
            self._plot_dataset(self.validation_set, self.report_path.get('validation_set_histogram.png'))

        # Generate training set
        if (len(self.train_sets) > 0):
            self.train_set = self._extract_sets(df.copy(deep=True), self.train_sets)

            if len(self.train_set) == 0:
                print ('No images selected for training set. This is a dry run.')
                dry = True
            else:
                # Remove files in validation_set from train_set
                if (self.validation_set is not None):
                    validation_images = self.validation_set[dataset_columns.INPUT]
                    
                    print ("intersection")
                    [print(f'{row["input"]}') for _, row in self.train_set[ self.train_set[dataset_columns.INPUT].isin(validation_images) ].iterrows()]
                    
                    self.train_set = self.train_set[ ~self.train_set[dataset_columns.INPUT].isin(validation_images) ]

                    if len(self.train_set) == 0:
                        print ('All images in training set were also on the validation set and were removed. This is a dry run.')
                        dry=True

            # Save training set
            self.train_set.to_excel(self.report_path.get('training_set.xlsx'))
            self._plot_dataset(self.train_set, self.report_path.get('training_set_histogram.png'))

        # Select default enconding
        if (self.train_set is None):
            print ('No training set defined. This is a dry run.')
            dry = True
        else:
            if self.encoding is None:
                unique_outputs = self.train_set[dataset_columns.OUTPUT].unique()

                if len(unique_outputs) == 0:
                    print ('No unique output values on training set. This is a dry run.')
                    dry=True
                else:
                    self.encoding = OneHot(np.sort(unique_outputs))

        # Create DatasetGenerators
        if self.train_set_generator is None:
            self.train_set_generator = DatasetGenerator()
        self.train_set_generator.dataset = self.train_set
        self.train_set_generator.encoding = self.encoding
        
        if self.validation_set_generator is None:
            self.validation_set_generator = DatasetGenerator()
        self.validation_set_generator.dataset = self.validation_set
        self.validation_set_generator.encoding = self.encoding

        self.str_final_hash = self.hash()

        custom_callbacks = [
            #tf.keras.callbacks.EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=15),
            tf.keras.callbacks.ModelCheckpoint(self.report_path.get('checkpoint.h5'), monitor='val_loss', save_best_only=True, mode='min'),
            tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=7, min_lr=1e-9),
            tf.keras.callbacks.CSVLogger(self.report_path.get('training.csv'))
            ]

        if self.model is not None:
            if self.encoding is not None:
                self.model.compile(len(self.encoding.labels))
            else:
                self.model.compile()

        self._export_summary()

        if dry is True:
            return

        if self.model is None:
            print('No model set. Quitting.')
            return
        
        startTime = time.time()
                
        history = self.model.get().fit(
            self.train_set_generator,
            #class_weight=self.encoding.weights,
            epochs=80,
            validation_data = self.validation_set_generator,
            callbacks = custom_callbacks,
            steps_per_epoch=None, #len(self.train_set_generator),
            validation_steps=None, #len(self.validation_set_generator),
            #shuffle=True
        )

        end = time.time()
        print("Training time (secs): {}".format(end-startTime))

        plt.clf()
        plt.plot(history.history['loss'],color='b',label='Training Loss')
        plt.plot(history.history['val_loss'],color='r', label='Validation Loss')
        plt.plot(history.history['acc'],color='g', label='Accuracy')
        plt.ylabel("loss")
        plt.ylim([0, 3])
        plt.xlabel("epoch")
        plt.title("Training")
        plt.legend()
        plt.savefig(self.report_path.get('history.png'), dpi=200)

        self.model.get().save(self.report_path.get('final.h5'))

        training_set_report = self._generate_confusion(self.train_set, self.model, self.encoding, self.report_path.get("training_set_final_confusion.png"))
        test_set_report = self._generate_confusion(self.validation_set, self.model, self.encoding, self.report_path.get("test_set_final_confusion.png"))
        self._complement_summary('Final', training_set_report, test_set_report)

        self.model.model = tf.keras.models.load_model(self.report_path.get('checkpoint.h5'))

        training_set_report = self._generate_confusion(self.train_set, self.model, self.encoding, self.report_path.get("training_set_best_confusion.png"))
        test_set_report = self._generate_confusion(self.validation_set, self.model, self.encoding, self.report_path.get("test_set_best_confusion.png"))
        self._complement_summary('Best', training_set_report, test_set_report)

    def hash(self):
        hasher = Hasher()
        hasher.ordered(self.name, self.input)
        hasher.ordered(*self.preprocessing_steps)

        hasher.ordered('train')
        hasher.unordered( *[ Hasher().ordered(*x).ordered(*l) for x, l in self.train_sets ] )

        hasher.ordered('test')
        hasher.unordered( *[ Hasher().ordered(*x).ordered(*l) for x, l in self.validation_sets ] )

        hasher.ordered(self.encoding, self.model, self.train_set_generator, self.validation_set_generator)
                   
        return hasher

    def _extract_sets(self, df:pandas.DataFrame, sets):
        if (len(sets) == 0):
            return pandas.DataFrame(columns=dataset_columns.all)

        datasets = []
        extractor = SampleExtractor(self.base_images_path, self.label_column, self.image_column)
        for steps, loaders in sets:
            samples = extractor.extract( _process_steps(df, steps) )

            for loader in loaders:
                samples_for_loader = samples.copy(deep=True)

                samples_for_loader.loc[:, dataset_columns.INPUT_LOADER] = loader

                datasets.append (samples_for_loader)

        ret = pandas.concat(datasets, ignore_index=True)

        return ret

    def _run_redirecting_stdout(self, file, func):
        with open(file, 'w') as f:
          with redirect_stdout(f):
              func()

    def _export_summary(self):
        file = self.report_path.get('modelsummary.txt')

        self._run_redirecting_stdout(file, self._print_full_summary)

    def _complement_summary(self, model, training_set_report, validation_set_report):
        file = self.report_path.get('modelsummary.txt')
        with open(file, 'a') as f:
            f.write (f'\n-- {model} model training set report:\n')
            f.write (training_set_report)
            f.write (f'\n-- {model} model validation set report:\n')
            f.write (validation_set_report)
                
    def _print_steps(self, steps: List[Step], loaders:Tuple[BaseLoader]):
        col1 = [str(x) for x in steps]
        col1_width = np.max([len(x) for x in col1]) + 3
        
        for col1, col2 in zip(col1, [x.description() for x in steps]):
            print (' ', col1.ljust(col1_width), col2)

        for loader in loaders:
            print ('   ', str(loader).ljust(col1_width - 2), loader.description())

        print ('')


    def _generate_confusion(self, dataset, model, encoding, filename):
        y = dataset['output'].tolist()

        generator = DatasetGenerator(dataset, encoding, batch_size=4, shuffle=False)

        ypred = model.get().predict_generator(generator)
        ypred = [encoding.decode(x) for x in ypred]

        cm = confusion_matrix(y, ypred, labels=encoding.labels)
        cm = pandas.DataFrame(cm, index=encoding.labels, columns=encoding.labels)

        plt.clf()
        plt.figure(figsize = (10,10))

        sns.heatmap(cm, annot=True, annot_kws={"size": 12}, fmt="d") # font size
        plt.savefig(filename, dpi=200)

        return classification_report(y, ypred)


    def _print_full_summary(self):

        title = f'--- Experiment {self.name} ({self.str_hash}) ---'
        print (title)
        print ('-' * len(title))
        print ('')
        print (f'Input: {self.input}')
        print (f'Images Path: {self.base_images_path}')
        print ('')
        print ('-- Preprocessing Steps:')
        self._print_steps(self.preprocessing_steps, ())

        print ('\n-- Training Set Steps:\n')
        for (steps, loader) in self.train_sets:
            self._print_steps(steps, loader)

        print ('\n-- Validation Set Steps:\n')
        for (steps, loader) in self.validation_sets:
            self._print_steps(steps, loader)

        if (self.model is not None):
            print (f'\n-- Model: {self.model}')
            print ('-- Model Summary:')
            self.model.get().summary()

        encoding_str = str(self.encoding) if self.encoding is not None else 'None'
        print (f'\n-- Encoding: {encoding_str}')
        print (f'-- Final Hash: {self.str_final_hash}')

    def _plot_dataset(self, df: pandas.DataFrame, filename:str):
        if (df.empty == True):
            return

        plt.clf()
        hist = _generate_dataset_histogram(df)
        hist.plot.bar(stacked=True)

        plt.legend(loc='upper left', bbox_to_anchor=(0.1, -0.2), borderaxespad=0, mode='expand')
        plt.tight_layout()

        ct = 0
        for idx, row in hist.iterrows(): 
            value = row.sum()
            plt.text(ct, value, str(value), ha='center')
            ct += 1

        plt.savefig(filename, dpi=200)
