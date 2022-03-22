import csv
import json

# ----------IMPORT AND VIEW CSV----------
with open('oura-data.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    for line in csv_reader:
        print(line)


