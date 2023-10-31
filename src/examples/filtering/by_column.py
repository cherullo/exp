import pandas
from arch import Hasher, Preprocessing
from preprocessing_steps import FilterColumn
import columns as cols

df = pandas.read_excel("src/examples/filtering/sampledatawinterathletes.xlsx", engine = "openpyxl")

filter = Preprocessing()
filter.add_step(FilterColumn(cols.NATIONALITY, ["Andorra"]))
df = filter.process(df)

print("Hash:", Hasher(filter))
print(filter)

print(df)

