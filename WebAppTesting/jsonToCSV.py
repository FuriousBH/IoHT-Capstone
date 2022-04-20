import json
import csv
import pandas as pd

import warnings
warnings.filterwarnings("ignore")
  
#Start of Brock's code to add key value pairs to oura data
with open("result.json") as json_file:
    json_decoded = json.load(json_file)

for s in json_decoded['data']:
    s['personid'] = '00001'

with open("updatedResults.json", 'w') as json_file:
    json.dump(json_decoded, json_file)
#-------End of Brock's Code-------------------------

#Start of Riley's code to convert json file to csv
df = pd.read_json('updatedResults.json')

print('The shape of the dataset is:', df.shape)

# %%
print(df)

# %%

import pandas as pd

pdObj = pd.read_json('updatedResults.json', orient='data')
csvData = pdObj.to_csv('updatedResults.csv')
print(csvData)

# %%
Cov = pd.read_csv("updatedResults.csv", 
                  sep=',', 
                  names=['dum1','bpm','source','timestamp','personid','dum2'],
                  quotechar="'")

Cov.head()

# %%
m = Cov.iloc[1: ,1:5]


# %%
m.head()

# %%
m['bpm'] = m['bpm'].str.extract('(\d+)').astype(int)
m['timestamp'] = m['timestamp'].str.replace("'timestamp':", "").astype(str)
m['timestamp'] = m['timestamp'].str.replace("'", "").astype(str)
# m['uuid'] = m['uuid'].str.extract('(\d+)').astype(int)
m['personid'] = m['personid'].str.extract('(\d+)').astype(int)
m['source'] = m['source'].str.replace("'source':", "")
m['source'] = m['source'].str.replace("'", "")

m.head()

# %%
convData3 = m.to_csv('finalResults.csv')
#-----------End of Riley's Code-----------------------