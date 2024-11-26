import csv
import numpy as np
from id_parser import parse_pearl_id_and_view
import os

csv_file_path = 'original_measuring_100.csv'

# Read the CSV file
with open(csv_file_path, mode='r', newline='') as file:
    reader = csv.reader(file, delimiter=';')
    
    # Extract the header
    header = next(reader)
    
    # Extract the rows
    rows = []
    for row in reader:
        rows.append(row)

# Display rows
print("the size: ", len(rows))
values_in_csv = []

for row in rows:
    values_in_csv.append(row[0])


UPLOAD_FOLDER = 'size_test/' 

object_dictionary = {}

for filename in os.listdir(UPLOAD_FOLDER):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    pearl_id, pearl_view = parse_pearl_id_and_view(filename)


    if pearl_id not in object_dictionary:
        object_dictionary[pearl_id] = {}

    object_dictionary[pearl_id][pearl_view] = file_path


print(len(object_dictionary.keys()))





