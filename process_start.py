import os
import cv2
import numpy as np
import shutil
from id_parser import parse_pearl_id_and_view
from segmentation import process_images
from config_manager import config_context

MERGE = False

# uploaded images
UPLOAD_FOLDER = 'upload_images/' 
object_dictionary = {}

'''
Maybe size prediction is not always needed
The folder maybe shouldnt be delete if it already exists: maybe append the date and time to the results folder


'''

allowed_file_types = ('.jpg', '.jpeg', '.png')

for filename in os.listdir(UPLOAD_FOLDER):
    if filename.endswith(allowed_file_types):  
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        pearl_id, pearl_view = parse_pearl_id_and_view(filename)

        if pearl_id not in object_dictionary:
            object_dictionary[pearl_id] = {}

        object_dictionary[pearl_id][pearl_view] = file_path
    else:
        print('Format not supported! Allowed formats are: jpg, jpeg and png.')  # ofc better error hanfling, see flask


output_folder = 'processed_pearl_output'

if not os.path.exists(output_folder): #  it deletes the folder if it already exists and creates a new one
        os.makedirs(output_folder)
else:
    try:
          shutil.rmtree(output_folder)
          os.makedirs(output_folder)
          print('Directiory for output already existed, created new one.')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


'''for pearl_id, views in object_dictionary.items():
     print('ID: ', pearl_id, ' views: ')
     for v in views:
          print('View', v,':', object_dictionary[pearl_id][v])'''



for pearl_id, views in object_dictionary.items(): 
    processed_images = {}

    required_views = [object_dictionary[pearl_id][v] for v in views]
    main_path = required_views[0]

    try:
        with config_context(main_path) as config:
                processed_images = process_images(required_views, config, MERGE) # merge is per default false

                for id, image in processed_images.items():
                    output_path = os.path.join(output_folder, f"{id}.png")
                    cv2.imwrite(output_path, image)
                    print('Saved: ', output_path)
    except ValueError as e:
        print(e)


print('Done!')