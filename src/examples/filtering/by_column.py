import pandas
from arch import Hasher, Preprocessing
from preprocessing_steps import FilterColumn
import columns as cols

filter = Preprocessing()
filter.add_step(FilterColumn(cols.NATIONALITY, ["Andorra", "Albania"]))
print(filter)
print("Hash:", Hasher(filter))

df = pandas.read_excel("examples/filtering/sampledatawinterathletes.xlsx", engine = "openpyxl")
df = filter.process(df)
print(df)

