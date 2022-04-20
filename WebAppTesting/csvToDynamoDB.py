# uploading csv to dynamoDB
#original source code: https://thekevinwang.com/2021/04/11/csv-to-dynamodb/

import sys
import csv
import boto3

dynamodb = boto3.resource('dynamodb')

tableName = 'oura-api'
filename = 'finalResults.csv' 


csvfile = open(filename)
def write_to_dynamo(rows):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(
                Item={
                    'bpm': row['bpm'],
                    'source': row['source'],
                    'timestamp': row['timestamp'],
                    'personid': row['personid']
                }
            )

csvfile = open(filename)
write_to_dynamo(csv.DictReader(csvfile))
print ('done')



#------------Working Code, testing without defs
# def main():
#     csvfile = open('finalResults.csv')
#                 #original = filename
#     write_to_dynamo(csv.DictReader(csvfile))

#     return print("Done")

# def write_to_dynamo(rows):
#     table = dynamodb.Table(tableName)
#     with table.batch_writer() as batch:
#         for row in rows:
#             batch.put_item(
#                 Item={
#                     'bpm': row['bpm'],
#                     'source': row['source'],
#                     'timestamp': row['timestamp'],
#                     'personid': row['personid']
#                 }
#             )

# main()
#-----------end working code--------------------

#------------Format for old batch csv data upload----------------------------------------------
#                     'PersonID': row['PersonID'],
#                     'date': row['date'],
#                     'Total Sleep Duration': row['Total Sleep Duration'],
#                     'Average Resting Heart Rate': row['Average Resting Heart Rate'],
#                     'Lowest Resting Heart Rate': row['Lowest Resting Heart Rate'],
#                     'Average HRV': row['Average HRV'],
#                     'Temperature Deviation (C)': row['Temperature Deviation (C)'],
#                     'Respiratory Rate': row['Respiratory Rate']