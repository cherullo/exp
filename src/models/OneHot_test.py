import pandas as pd
import numpy as np
import pandas
import arch.DatasetGenerator as DG
from models.OneHot import OneHot

LABEL1 = 'label_1'
LABEL2 = 'label_2'
LABEL3 = 'label_3'
LABEL4 = 'label_4'
LABELS = [LABEL1, LABEL2, LABEL3, LABEL4]
onehot = OneHot(LABELS)


def test_encoding_works():
    assert np.array_equal(onehot.encode(LABEL1), [1.0, 0.0, 0.0, 0.0])

def test_encoding_series():
    df = pandas.DataFrame(data=[LABEL1, LABEL2], columns=['col'])

    encoded = onehot.encode(df['col'])

    assert np.array_equal(encoded[0], [1.0, 0.0, 0.0, 0.0])
    assert np.array_equal(encoded[1], [0.0, 1.0, 0.0, 0.0])

def test_decoding_works():
    assert onehot.decode([1.0, 0.0, 0.0, 0.0]) == LABEL1

#def test_integrated():
#
#    df = pd.read_excel("reports\efficient_baseline-db583958\dataset.xlsx")
#
#    Dataset=DG(df,batch_size=100)
#    y=Dataset[10]
#    print('Encoding sucessfull: ',y)