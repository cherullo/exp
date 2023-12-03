import pandas
from arch import Preprocessing
from preprocessing_steps import FirstCount

filter = Preprocessing()

# Keep the first 5 rows of the dataset 
filter.add_step(FirstCount(5))

# Manually load the dataset
df = pandas.read_excel("sampledatawinterathletes.xlsx", engine = "openpyxl")

# Print the preprocessing steps
print(filter)
# Filter the dataset and print the results
print(filter.process(df))

# Expected output
#
#  FirstCount(5)   Keeps the first 5 rows.

#                    Name                 Sport Nationality  Age  Wt kg     Ht
# 0            TOLA Erjon         Alpine Skiing     Albania   23   74.0  181.0
# 1  KHELIFI Mehdhi-Selim  Cross-Country Skiing     Algeria   17   65.0  170.0
# 2   ESTEVE RIGAIL Kevin         Alpine Skiing     Andorra   20   80.0  180.0
# 3      GUTIERREZ Mireia         Alpine Skiing     Andorra   21   60.0  162.0
# 4          JUAREZ Sofie         Alpine Skiing     Andorra   18   70.0  172.0