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

# toggle switch

MERGE = True  
TRANSPARENT = True
ORIGINAL_SCALE_SIZE_mm = 50   # this is a fixed value, need to make this adaptable to user input 

# *************** 

start_time = datetime.now()

UPLOAD_FOLDER = 'upload_images/' 
OUTPUT_FOLDER_NAME = 'processed_pearl_output'
output_counter = 1

ALLOWED_FILE_TYPES = ('.jpg', '.jpeg', '.png')
XLSX_FILE = 'pearl_data_color.xlsx'

object_dictionary = {}


for filename in os.listdir(UPLOAD_FOLDER):
    if filename.endswith(ALLOWED_FILE_TYPES):  
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        pearl_id, pearl_view = parse_pearl_id_and_view(filename)

        if pearl_id not in object_dictionary:
            object_dictionary[pearl_id] = {}

        object_dictionary[pearl_id][pearl_view] = file_path
    else:
        print('Format not supported! Allowed formats are: jpg, jpeg and png.') 


output_path = OUTPUT_FOLDER_NAME
while os.path.exists(output_path):
        print(f"Folder {output_path} already exists!")
        output_path = OUTPUT_FOLDER_NAME + f"_{output_counter}"
        output_counter += 1
os.makedirs(output_path)


workbook = Workbook()
sheet = workbook.active

sheet.title = "Pearl Data"
sheet.append(['PEARL_ID', 'LENGTH (mm)', 'WIDTH (mm)', '#1 COLOR','#1 RGB', '#2 COLOR','#2 RGB', '#3 COLOR','#3 RGB'])


for pearl_id, views in object_dictionary.items(): 
    processed_images = {}

    rgb_values = ["(X, X, X)", "(X, X, X)", "(X, X, X)"]  
    white_fill = PatternFill(start_color='FFFFFFFF', end_color='FFFFFFFF', fill_type="solid")
    cell_fills = [white_fill, white_fill, white_fill]

    required_views = [object_dictionary[pearl_id][v] for v in views]
    main_path = required_views[0] 

    try:
        with config_context(main_path) as config:
                processed_images, obj_len, obj_width, colors = crop_artifact_and_measure(required_views, config, MERGE, TRANSPARENT, ORIGINAL_SCALE_SIZE_mm)
                rgb_values = []
                cell_fills = []
                for id, image in processed_images.items():
                    output_image_path = os.path.join(output_path, f"{id}.png")
                    cv2.imwrite(output_image_path, image)
                    print('Saved: ', output_image_path)

                wA_str = f"{obj_len:.2f}".replace('.', ',')
                wB_str = f"{obj_width:.2f}".replace('.', ',')

                if colors is not None:
                    rgb_values, cell_fills = convert_for_xlsx(colors)

                row = [pearl_id, wA_str, wB_str, ' ', rgb_values[0], ' ', rgb_values[1], ' ', rgb_values[2]]
                sheet.append(row)
                row_index = sheet.max_row
                
                sheet[f"D{row_index}"].fill = cell_fills[0]
                sheet[f"F{row_index}"].fill = cell_fills[1]
                sheet[f"H{row_index}"].fill = cell_fills[2]

                print(f"Saved data for {pearl_id}")
    except ValueError as e:
        print(e)

# join paths 
#workbook.save(XLSX_FILE)
workbook.save(os.path.join(output_path, XLSX_FILE))
end_time = datetime.now()

print('Done!')
print('Duration: {}'.format(end_time - start_time))