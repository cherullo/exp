import numpy as np
import pandas

from exp.models.OneHot import OneHot

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
