# uploading csv to dynamoDB
#original source code: https://thekevinwang.com/2021/04/11/csv-to-dynamodb/

import sys
import csv
import boto3

dynamodb = boto3.resource('dynamodb')

tableName = 'ouraData'
filename = 'oura-data.csv' 

def main():
    csvfile = open(filename)

    write_to_dynamo(csv.DictReader(csvfile))

    return print("Done")

def write_to_dynamo(rows):
    table = dynamodb.Table(tableName)
    with table.batch_writer() as batch:
        for row in rows:
            batch.put_item(
                Item={
                    'PersonID': row['PersonID'],
                    'date': row['date'],
                    'Total Sleep Duration': row['Total Sleep Duration'],
                    'Average Resting Heart Rate': row['Average Resting Heart Rate'],
                    'Lowest Resting Heart Rate': row['Lowest Resting Heart Rate'],
                    'Average HRV': row['Average HRV'],
                    'Temperature Deviation (C)': row['Temperature Deviation (C)'],
                    'Respiratory Rate': row['Respiratory Rate']
                }
            )

main()
