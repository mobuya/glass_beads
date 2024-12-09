import os
import cv2
import shutil
from id_parser import parse_pearl_id_and_view
from segmentation import process_images
from config_manager import config_context
from prediction import process_object_size_color
from openpyxl import Workbook
from openpyxl.styles import PatternFill


UPLOAD_FOLDER = 'combine_all/' 
OUTPUT_FOLDER = 'processed_pearl_output'
ALLOWED_FILE_TYPES = ('.jpg', '.jpeg', '.png')

XLSX_FILE = 'pearl_data_color.xlsx'

MERGE = True
TRANSPARENT = True

object_dictionary = {}

'''
Maybe size prediction is not always needed !!!!! i think it is, should ask Lukas about it
The folder maybe shouldnt be delete if it already exists: maybe append the date and time to the results folder

I can make a loop that looks for a valid scale, and when it finds a valid scale, it then starts predicting, for images where the scale is visible save that value as helper_scale_value 
so when it again gets to a scale thats not readable it takes that previous value

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

workbook = Workbook()
sheet = workbook.active
sheet.title = "Pearl Data"
sheet.append(['Pearl_ID', 'Length', 'Width', 'Color'])

for pearl_id, views in object_dictionary.items(): 
    processed_images = {}

    required_views = [object_dictionary[pearl_id][v] for v in views]
    main_path = required_views[0]  # the first picture determines the configuration !!! 

    try:
        with config_context(main_path) as config:
                # should add here the scale determination, should also ask lukas maybe what he thinks about my idea
                processed_images = process_images(required_views, config, MERGE, TRANSPARENT) # merge is per default false
                wA, wB, mean_color = process_object_size_color(required_views, config)

                for id, image in processed_images.items():
                    output_path = os.path.join(OUTPUT_FOLDER, f"{id}.png")
                    cv2.imwrite(output_path, image)
                    print('Saved: ', output_path)

                wA_str = f"{wA:.2f}".replace('.', ',')
                wB_str = f"{wB:.2f}".replace('.', ',')

                rgb_color = f"RGB: ({mean_color[0]}, {mean_color[1]}, {mean_color[2]})"
                row = [pearl_id, wA_str, wB_str, rgb_color]
                sheet.append(row)

                color_hex = f"{mean_color[0]:02X}{mean_color[1]:02X}{mean_color[2]:02X}"
                color_fill = PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")
                sheet[f"D{sheet.max_row}"].fill = color_fill

                print(f"Saved data for {pearl_id}")
    except ValueError as e:
        print(e)

workbook.save(XLSX_FILE)
print('Done!')