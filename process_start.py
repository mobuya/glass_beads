import os
import cv2
import shutil
from id_parser import parse_pearl_id_and_view
from segmentation import process_images
from config_manager import config_context
from prediction import process_object_size
import csv


UPLOAD_FOLDER = 'combine_all/' 
OUTPUT_FOLDER = 'processed_pearl_output'
ALLOWED_FILE_TYPES = ('.jpg', '.jpeg', '.png')
CSV_FILE = 'pearl_dimensions.csv'

MERGE = False

object_dictionary = {}

'''
Maybe size prediction is not always needed !!!!! i think it is, should ask Lukas about it
The folder maybe shouldnt be delete if it already exists: maybe append the date and time to the results folder


'''

for filename in os.listdir(UPLOAD_FOLDER):
    if filename.endswith(ALLOWED_FILE_TYPES):  
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        pearl_id, pearl_view = parse_pearl_id_and_view(filename)

        if pearl_id not in object_dictionary:
            object_dictionary[pearl_id] = {}

        object_dictionary[pearl_id][pearl_view] = file_path
    else:
        print('Format not supported! Allowed formats are: jpg, jpeg and png.')  # ofc better error hanfling, see flask



if not os.path.exists(OUTPUT_FOLDER): #  it deletes the folder if it already exists and creates a new one
        os.makedirs(OUTPUT_FOLDER)
else:
    try:
          shutil.rmtree(OUTPUT_FOLDER)
          os.makedirs(OUTPUT_FOLDER)
          print('Directiory for output already existed, created new one.')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


'''for pearl_id, views in object_dictionary.items():
     print('ID: ', pearl_id, ' views: ')
     for v in views:
          print('View', v,':', object_dictionary[pearl_id][v])'''

csv_header = ['pearl_id', 'length', 'width']
if not os.path.exists(CSV_FILE):
     with open(CSV_FILE, mode='w', newline='') as file:
          writer = csv.writer(file, delimiter = ';')
          writer.writerow(csv_header)


for pearl_id, views in object_dictionary.items(): 
    processed_images = {}

    required_views = [object_dictionary[pearl_id][v] for v in views]
    main_path = required_views[0]

    try:
        with config_context(main_path) as config:
                processed_images = process_images(required_views, config, MERGE) # merge is per default false
                wA, wB = process_object_size(required_views, config)
                for id, image in processed_images.items():
                    output_path = os.path.join(OUTPUT_FOLDER, f"{id}.png")
                    cv2.imwrite(output_path, image)
                    print('Saved: ', output_path)

                wA_str = f"{wA:.2f}".replace('.', ',')
                wB_str = f"{wB:.2f}".replace('.', ',')
                # add color determination: simple function
                with open(CSV_FILE, mode='a', newline='') as file:
                     writer = csv.writer(file, delimiter = ';')
                     writer.writerow([pearl_id, wA_str, wB_str])
                     print(f"Saved dimensions for {pearl_id}")
    except ValueError as e:
        print(e)


print('Done!')