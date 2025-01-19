import os
import cv2
import numpy as np
from datetime import datetime
from id_parser import parse_bead_id_and_view
from config_manager import config_context
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter

from color_converter import convert_for_xlsx
from crop_and_measure import process_bead_data



'''
This is the MAIN file, this is where everything starts and everything gets done!

----> OpenCV version: 4.9.0 (!!!)
'''

# toggle switch
'''
These are all the web user inputs!
'''
MERGE = False  
TRANSPARENT = True
ORIGINAL_SCALE_SIZE_mm = 50 

GET_ALL_VIEW_COLOR = True
# *************** 

start_time = datetime.now() # i use this jus to measure time

UPLOAD_FOLDER = 'combine_all/' 
#UPLOAD_FOLDER = 'pearls_to_segment/' 
OUTPUT_FOLDER_NAME = 'processed_pearl_output'
output_counter = 1  # this just helps in cae the output folder was not renamed, to just create a new one, to avoid overwriting the existing one

ALLOWED_FILE_TYPES = ('.jpg', '.jpeg', '.png')
XLSX_FILE = 'pearl_data_color.xlsx'

object_dictionary = {}  

'''
To clarify: my objects are saved in a dictionary, for example the bead ENZFSCH_333_001 has views A1, A2, B1 and B2 so then its saved as:

object_dictionary = {
    "ENZFSCH_333_001": {
        "A1": "UPLOAD_FOLDER/ENZFSCH_333_001_A1.png",
        "A2": "UPLOAD_FOLDER/ENZFSCH_333_001_A2.png",
        "B1": "UPLOAD_FOLDER/ENZFSCH_333_001_B1.png",
        "B2": "UPLOAD_FOLDER/ENZFSCH_333_001_B2.png"
    }, etc.. 

The following code reads the values from the UPLOAD_FOLDER and creates this dictionary; it is not saved in a separate function for now, it starts automatically with running this file.  
    
    
    down here
'''
for filename in os.listdir(UPLOAD_FOLDER):
    if filename.endswith(ALLOWED_FILE_TYPES):  
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        pearl_id, pearl_view = parse_bead_id_and_view(filename)

        if pearl_id not in object_dictionary:
            object_dictionary[pearl_id] = {}

        object_dictionary[pearl_id][pearl_view] = file_path
    else:
        print('Format not supported! Allowed formats are: jpg, jpeg and png.') # TODO: Logging


output_path = OUTPUT_FOLDER_NAME
while os.path.exists(output_path):
        print(f"Folder {output_path} already exists!") # TODO: Logging
        output_path = OUTPUT_FOLDER_NAME + f"_{output_counter}"
        output_counter += 1
os.makedirs(output_path) # this creates the output dictionary 


workbook = Workbook()
sheet = workbook.active

sheet.title = "Pearl Data"

# sheet.append(['PEARL_ID', 'LENGTH (mm)', 'WIDTH (mm)', '#1 COLOR','#1 RGB', '#2 COLOR','#2 RGB', '#3 COLOR','#3 RGB'])

'''
DISCLAIMER: The color function for now only looks at view A, i need to change this, it will be later done, i will send you all that when im done, but i dont think it will impact your code much. 
But just info to be sure :)
'''

if GET_ALL_VIEW_COLOR:
     sheet.append(['PEARL_ID', 'LENGTH (mm)', 'WIDTH (mm)', 'VIEW', '# # #', 'RBG'])
     print('hmm')
else:
     sheet.append(['PEARL_ID', 'LENGTH (mm)', 'WIDTH (mm)', '#1 COLOR','#1 RGB', '#2 COLOR','#2 RGB', '#3 COLOR','#3 RGB'])

for pearl_id, views in object_dictionary.items():  # this loops through the dictionary, it goes PER bead_id
    processed_images = {}
    # this is just a placeholder, default value in case the colors couldn't be determined for some reason 
    rgb_values = ["(X, X, X)", "(X, X, X)", "(X, X, X)"]  
    white_fill = PatternFill(start_color='FFFFFFFF', end_color='FFFFFFFF', fill_type="solid")
    cell_fills = [white_fill, white_fill, white_fill]

    required_views = [object_dictionary[pearl_id][v] for v in views] # this just saves all the paths for each view of the bead
    main_path = required_views[0]  # the first image of the bead is used to determine the configuration

    try:
        with config_context(main_path) as config:
                processed_images, obj_len, obj_width, colors = process_bead_data(required_views, config, MERGE, TRANSPARENT, ORIGINAL_SCALE_SIZE_mm) # this does alllll the work, you can look into the file if you want more info
                #rgb_values = []
                #cell_fills = []
                '''
                Basically it returns the merged image or single images of each view of the bead, and the beads dimensions
                Later the processed_images gets looped, it is also a dictionary containing the ID of the output image and the result image.
                Those then get saved in the output path.
                '''
                for id, image in processed_images.items(): 
                    output_image_path = os.path.join(output_path, f"{id}.png")
                    cv2.imwrite(output_image_path, image)
                    print('Saved: ', output_image_path)
                
                # this all is the data for the XLSx file 
                wA_str = f"{obj_len:.2f}".replace('.', ',')
                wB_str = f"{obj_width:.2f}".replace('.', ',')

                row = [pearl_id, wA_str, wB_str]
                sheet.append(row)

                current_col = 4 
                if GET_ALL_VIEW_COLOR:
                    for view, all_colors in colors.items():
                            #rgb_values, cell_fills = convert_for_xlsx([all_colors[0]])
                            #rgb_values, cell_fills = convert_for_xlsx(all_colors)
                            rgb_values, cell_fills = convert_for_xlsx([all_colors[1]])
                            row_index = sheet.max_row

                            for i, (label, fill, rgb) in enumerate(zip([f"{view} COL1:", f"{view} COL2:", f"{view} COL3:"],
                                                                    cell_fills,
                                                                    rgb_values)):
                                sheet[f"{get_column_letter(current_col)}{row_index}"] = label
                                current_col += 1
                                sheet[f"{get_column_letter(current_col)}{row_index}"].fill = fill
                                current_col += 1
                                sheet[f"{get_column_letter(current_col)}{row_index}"] = rgb
                                current_col += 1           
                else:
                    main_color = list(colors.values())[0]
                    rgb_values, cell_fills = convert_for_xlsx(main_color)
                
                    row_index = sheet.max_row
                    
                    sheet[f"D{row_index}"].fill = cell_fills[0]
                    sheet[f"E{row_index}"] = rgb_values[0]

                    sheet[f"F{row_index}"].fill = cell_fills[1]
                    sheet[f"G{row_index}"] = rgb_values[1]

                    sheet[f"H{row_index}"].fill = cell_fills[2]
                    sheet[f"I{row_index}"] = rgb_values[2]

                print(f"Saved data for {pearl_id}")
    except ValueError as e:
        print(e)

# join paths 
workbook.save(XLSX_FILE)
workbook.save(os.path.join(output_path, XLSX_FILE))

end_time = datetime.now()

print('Done!')
print('Duration: {}'.format(end_time - start_time))