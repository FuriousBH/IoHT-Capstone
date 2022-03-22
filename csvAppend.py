#-------- append PersonID to oura data csv --------

import csv
import pandas as pd

df = pd.read_csv("oura-data.csv")
df.insert(loc=0, column="PersonID", value = "00001")
df.to_csv("oura-data.csv", index = False)