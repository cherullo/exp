import pandas
from arch import Hasher, Preprocessing
from preprocessing_steps import KeepCount

filter = Preprocessing()
filter.add_step(KeepCount(5))
print(filter)
print("Hash:", Hasher(filter))

df = pandas.read_excel("sampledatawinterathletes.xlsx", engine = "openpyxl")
print(filter.process(df))