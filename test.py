import cv2
from config.config_manager import config_context
import numpy as np
from matplotlib import pyplot as plt
from processing import find_artifact_contour
from processing import get_dominant_color
from utils import parse_bead_id_and_view

image_path = "combine_all/ENZFSCH_340_129_A.png"


def plot_img_with_colors(img, colors):
    n_colors = colors.shape[0]

    fig, ax = plt.subplots(1, n_colors + 1)
    [axi.set_axis_off() for axi in ax.ravel()]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ax[0].imshow(img)
    ax[0].set_title(f"Image with hole")
    for c_i, c in enumerate(colors):
        colored_box = np.full(img.shape, c)
        ax[c_i+1].imshow(colored_box)
        ax[c_i+1].set_title(f"Color #{c_i+1}")
    plt.show()

try:
    with config_context(image_path) as config:
        if config is None:
            print('its none')
            print(2+2)
        else:
            image = cv2.imread(image_path)
            sml_c, in_c = find_artifact_contour(image, 'B', config)
            dominant_colors = get_dominant_color(image, sml_c, in_c)
            print(f"Num of dom {len(dominant_colors)}")

            plot_img_with_colors(image, dominant_colors)

except ValueError as e:
        print(e) 
