import pandas
from exp.arch import Preprocessing
from exp.preprocessing_steps import ReplaceValueInColumn, FilterColumn
import columns as cols

filter = Preprocessing()

# Keep only the rows where Nationality equals Andorra or Albania
filter.add_step(FilterColumn(cols.NATIONALITY, ["Andorra", "Albania"]))

# Replace "Alpine Skiing" with "Skiing" in the Sport column
filter.add_step(ReplaceValueInColumn(cols.SPORT, "Alpine Skiing", "Skiing"))
# Replace "Alpine Skiing" with "Cross-Country Skiing" in the Sport column
filter.add_step(ReplaceValueInColumn(cols.SPORT, "Cross-Country Skiing", "Skiing"))

# Manually load the dataset
df = pandas.read_excel("sampledatawinterathletes.xlsx", engine = "openpyxl")

# Print the preprocessing steps
print(filter)
# Filter the dataset and print the results
print(filter.process(df))

# Expected output:
#
#  FilterColumn("Nationality", ["Andorra", "Albania"])   Keeps all rows where the column "Nationality" has any of the following values: "Andorra", "Albania"
#  ChangeColumn[Alpine Skiing -> Skiing]                 In row "Sport", change "Alpine Skiing" to "Skiing"
#  ChangeColumn[Cross-Country Skiing -> Skiing]          In row "Sport", change "Cross-Country Skiing" to "Skiing"
#
#                   Name      Sport Nationality  Age  Wt kg     Ht
# 0           TOLA Erjon     Skiing     Albania   23   74.0  181.0
# 2  ESTEVE RIGAIL Kevin     Skiing     Andorra   20   80.0  180.0
# 3     GUTIERREZ Mireia     Skiing     Andorra   21   60.0  162.0
# 4         JUAREZ Sofie     Skiing     Andorra   18   70.0  172.0
# 5  MARIN TARROCH Lluis  Snowboard     Andorra   21   80.0  186.0
# 6      SOULIE Francois     Skiing     Andorra   31   68.0  180.0