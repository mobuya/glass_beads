

def parse_bead_id_and_view(filename):
    '''
    Extracts the bead ID and view type from the given filename.

    Assumes the filename follows the pattern: "beadID_view.extension"  
        example: "ENZFSCH_333_001_A.png" →  bead_id: "ENZFSCH_333_001", bead_view: "A"

    Parameters
    ----------
    filename : str
        The filename of the image (not the full path).

    Returns
    -------
    bead_id : str
        The unique identifier of the pearl (everything before the last underscore).

    bead_view : str
        The view type of the pearl extracted after the last underscore (e.g., 'A', 'B', 'A1', 'B2', ...).
    '''
    filename = filename.split('.')[0] 
    parts = filename.split('_')

    bead_id = '_'.join(parts[:-1])
    bead_view = parts[-1]

    return  bead_id, bead_view

def parse_filename_from_path(filepath):
    '''
    Extracts the filename without the extension from a full file path.

    Example: "/path/to/image/ENZFSCH_333_001_A.png" → "ENZFSCH_333_001_A"

    Parameters
    ----------
    filepath : str
        The FULL file path to the image.

    Returns
    -------
    filename : str
        The filename WITHOUT its extension.
    '''
    filename = filepath.split('/')[-1]
    filename = filename.split('.')[0] 

    return filename

