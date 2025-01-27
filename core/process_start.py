import os
import cv2
from datetime import datetime

from utils import parse_bead_id_and_view, convert_for_xlsx
from config import config_context
from core import process_bead_data

from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter


import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='processing.log', encoding='utf-8', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s") # check the level

'''
These are all the web user inputs!
'''
MERGE = False  
TRANSPARENT = True
ORIGINAL_SCALE_SIZE_mm = 50 
GET_ALL_VIEW_COLOR = False


start_time = datetime.now() 

UPLOAD_FOLDER = 'upload_images/'
OUTPUT_FOLDER_NAME = 'processed_bead_output'
output_counter = 1 

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
'''
for filename in os.listdir(UPLOAD_FOLDER):
    if filename.endswith(ALLOWED_FILE_TYPES):  
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        pearl_id, pearl_view = parse_bead_id_and_view(filename)

        if pearl_id not in object_dictionary:
            object_dictionary[pearl_id] = {}

        object_dictionary[pearl_id][pearl_view] = file_path
    else:
        logger.info(f"Format is not supported for {filename}, the allowed types are: {ALLOWED_FILE_TYPES}")


output_path = OUTPUT_FOLDER_NAME
while os.path.exists(output_path):
        logger.info(f"A folder with the name {output_path} already exists, created new one appending {output_counter} to folder name.")
        output_path = OUTPUT_FOLDER_NAME + f"_{output_counter}"
        output_counter += 1
os.makedirs(output_path) 


workbook = Workbook()
sheet = workbook.active

sheet.title = "Pearl Data"

# sheet.append(['PEARL_ID', 'LENGTH (mm)', 'WIDTH (mm)', '#1 COLOR','#1 RGB', '#2 COLOR','#2 RGB', '#3 COLOR','#3 RGB'])

sheet.append(['PEARL_ID', 'LENGTH (mm)', 'WIDTH (mm)', '#1 COLOR','#1 RGB', '#2 COLOR','#2 RGB', '#3 COLOR','#3 RGB'])

for pearl_id, views in object_dictionary.items():  
    processed_images = {}

    required_views = [object_dictionary[pearl_id][v] for v in views]
    main_path = required_views[0] 

    try:
        with config_context(main_path) as config:
                if config is None:
                    logger.warning(f"For the bead: {pearl_id} the processing had to be skipped because the config manager yield None.")
                    continue
                
                logger.info(f"Processing bead: {pearl_id}")
                processed_images, obj_len, obj_width, colors = process_bead_data(required_views, config, MERGE, TRANSPARENT, ORIGINAL_SCALE_SIZE_mm)
    
                if len(processed_images.keys()) == 0:
                     logger.info(f"For bead {pearl_id} no processed images saved (!!!)")
                else:
                    for id, image in processed_images.items(): 
                        output_image_path = os.path.join(output_path, f"{id}.png")
                        cv2.imwrite(output_image_path, image)
                        print('Saved: ', output_image_path)
                
                # this all is the data for the XLSx file 
                wA_str = f"{obj_len:.2f}".replace('.', ',')
                wB_str = f"{obj_width:.2f}".replace('.', ',')

                rgb_values, cell_fills = convert_for_xlsx(colors)

                row = [pearl_id, wA_str, wB_str, ' ', rgb_values[0],' ',rgb_values[1],' ', rgb_values[2]]
                sheet.append(row)

                row_index = sheet.max_row
                
                sheet[f"D{row_index}"].fill = cell_fills[0]
                sheet[f"F{row_index}"].fill = cell_fills[1]
                sheet[f"H{row_index}"].fill = cell_fills[2]

                logger.info(f"Finished processing bead: {pearl_id}.")
    except Exception as e:
        logger.error(f"Error while processing: {pearl_id}: {e}")
 
workbook.save(os.path.join(output_path, XLSX_FILE))

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))