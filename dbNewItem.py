#-------- adds new table item directly to dynamo --------
import boto3
import json
from datetime import datetime
# client for dynamodb
dynamodb_client = boto3.client('dynamodb')

# setting the table
ouraTestTable = 'ouraTest'

#converting date time to string
DATE = datetime.now()
date = str(DATE)

# table item
# item = {
#     'PersonID':{'S':'00005'},
#     'Date':{'S':date},
#     'AvgHRV':{'N':'30'},
#     'AvgRestingHeart':{'N':'60'}
# }

item = {
    "2022-03-12": {
        "date": "2022-03-12",
        "Total Sleep Duration": "25770",
        "Average Resting Heart Rate": "63.49",
        "Lowest Resting Heart Rate": "58.0",
        "Average HRV": "29",
        "Temperature Deviation (\u00b0C)": "-0.21",
        "Respiratory Rate": "13.75"
    }
}


# put item into dynamo
resp = dynamodb_client.put_item(TableName = ouraTestTable, Item = item)

