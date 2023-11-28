import pandas
from arch import Hasher, Preprocessing
from preprocessing_steps import ChangeColumn, FilterColumn
import columns as cols

filter = Preprocessing()
filter.add_step(FilterColumn(cols.NATIONALITY, ["Andorra", "Albania"]))
filter.add_step(ChangeColumn(cols.SPORT, "Alpine Skiing", "Skiing"))
filter.add_step(ChangeColumn(cols.SPORT, "Cross-Country Skiing", "Skiing"))
print(filter)
print("Hash:", Hasher(filter))

df = pandas.read_excel("sampledatawinterathletes.xlsx", engine = "openpyxl")
print(filter.process(df))