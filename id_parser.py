

def parse_pearl_id_and_view(filename):
    filename = filename.split('.')[0] 
    parts = filename.split('_')

    pearl_id = '_'.join(parts[:-1])
    pearl_view = parts[-1]

    return pearl_id, pearl_view

def parse_pearl_id_from_path(filepath):
    filename = filepath.split('/')[-1]
    filename = filename.split('.')[0] 

    return filename

