import pandas
from arch import Preprocessing
from preprocessing_steps import FilterColumn
import columns as cols

filter = Preprocessing()

# Keep only the rows where Nationality equals Andorra or Albania
filter.add_step(FilterColumn(cols.NATIONALITY, ["Andorra", "Albania"]))

# Manually load the dataset
df = pandas.read_excel("sampledatawinterathletes.xlsx", engine = "openpyxl")

# Print the preprocessing steps
print(filter)
# Filter the dataset and print the results
print(filter.process(df))

# Expected output:

# FilterColumn("Nationality", ["Andorra", "Albania"])   Keeps all rows where the column "Nationality" has any of the following values: "Andorra", "Albania"
#
#                   Name                 Sport Nationality  Age  Wt kg     Ht
# 0           TOLA Erjon         Alpine Skiing     Albania   23   74.0  181.0
# 2  ESTEVE RIGAIL Kevin         Alpine Skiing     Andorra   20   80.0  180.0
# 3     GUTIERREZ Mireia         Alpine Skiing     Andorra   21   60.0  162.0
# 4         JUAREZ Sofie         Alpine Skiing     Andorra   18   70.0  172.0
# 5  MARIN TARROCH Lluis             Snowboard     Andorra   21   80.0  186.0
# 6      SOULIE Francois  Cross-Country Skiing     Andorra   31   68.0  180.0