import os
import cv2
import shutil
import numpy as np
from datetime import datetime
from id_parser import parse_pearl_id_and_view
from config_manager import config_context
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from color_converter import convert_for_xlsx
from crop_and_measure import crop_artifact_and_measure


start_time = datetime.now()

UPLOAD_FOLDER = 'combine_all/' 
OUTPUT_FOLDER = 'processed_pearl_output'
ALLOWED_FILE_TYPES = ('.jpg', '.jpeg', '.png')

XLSX_FILE = 'pearl_data_color.xlsx'

MERGE = True  
TRANSPARENT = True

object_dictionary = {}

'''
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
        print('Format not supported! Allowed formats are: jpg, jpeg and png.') 



if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
else:
    try:
          shutil.rmtree(OUTPUT_FOLDER)
          os.makedirs(OUTPUT_FOLDER)
          print('Directiory for output already existed, created new one.')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))



workbook = Workbook()
sheet = workbook.active

sheet.title = "Pearl Data"
sheet.append(['PEARL_ID', 'LENGTH (mm)', 'WIDTH (mm)', '#1 COLOR','#1 RGB', '#2 COLOR','#2 RGB', '#3 COLOR','#3 RGB'])


for pearl_id, views in object_dictionary.items(): 
    processed_images = {}

    required_views = [object_dictionary[pearl_id][v] for v in views]
    main_path = required_views[0] 

    try:
        with config_context(main_path) as config:
                processed_images, obj_len, obj_width, colors = crop_artifact_and_measure(required_views, config, MERGE, TRANSPARENT)
                rgb_values = []
                cell_fills = []
                for id, image in processed_images.items():
                    output_path = os.path.join(OUTPUT_FOLDER, f"{id}.png")
                    cv2.imwrite(output_path, image)
                    print('Saved: ', output_path)

                wA_str = f"{obj_len:.2f}".replace('.', ',')
                wB_str = f"{obj_width:.2f}".replace('.', ',')

                if colors is not None:
                    rgb_values, cell_fills = convert_for_xlsx(colors)
                else:
                    rgb_values = ["(X, X, X)", "(X, X, X)", "(X, X, X)"]  # Use a plain list
                    white_fill = PatternFill(start_color='FFFFFFFF', end_color='FFFFFFFF', fill_type="solid")
                    cell_fills = [white_fill, white_fill, white_fill]  # Use a plain list


                row = [pearl_id, wA_str, wB_str, ' ', rgb_values[0], ' ', rgb_values[1], ' ', rgb_values[2]]
                sheet.append(row)
                row_index = sheet.max_row
                
                sheet[f"D{row_index}"].fill = cell_fills[0]
                sheet[f"F{row_index}"].fill = cell_fills[1]
                sheet[f"H{row_index}"].fill = cell_fills[2]

                print(f"Saved data for {pearl_id}")
    except ValueError as e:
        print(e)

workbook.save(XLSX_FILE)
end_time = datetime.now()

print('Done!')
print('Duration: {}'.format(end_time - start_time))