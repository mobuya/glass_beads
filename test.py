import cv2
import numpy as np
from matplotlib import pyplot as plt
from find_object import find_artifact_contour_and_color
from config_manager import config_context
from color_extraction import get_dominant_color


#path = "ENZFSCH_333_009_A.png"
#path = "ENZFSCH_333_027_A.png"
#path = "ENZFSCH_340_007_B1.png"
#path = "ENZFSCH_333_001_B2.png"
#path = "ENZFSCH_333_010_A.png"

path = "combine_all/ENZFSCH_333_010_B2.png"
img = cv2.imread(path)



def plot_img_with_colors(img, colors):
    n_colors = colors.shape[0]
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)

    fig, ax = plt.subplots(1, n_colors + 1)
    [axi.set_axis_off() for axi in ax.ravel()]

    ax[0].imshow(img)
    ax[0].set_title(f"Image")
    for c_i, c in enumerate(colors):
        print(f"The color is: {c}") # 135 108  63
        colored_box = np.full(img.shape, c)
        ax[c_i+1].imshow(colored_box)
        ax[c_i+1].set_title(f"Color #{c_i+1}")
    plt.show()


try:
    with config_context(path) as config:
        out_cnt, _, main_clr = find_artifact_contour_and_color(path, 'X', config)
        dom_cols = get_dominant_color(img, out_cnt)
        #plot_img_with_colors(img, np.array(dom_cols))
        plot_img_with_colors(img, np.array([main_clr]))
except ValueError as e:
        print(e) 
