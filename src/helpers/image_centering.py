import numpy as np

def center(img, final_center, final_radius):
    m = np.amin(img)
    M = np.amax(img)

    image_radius = (M - m) * 0.5
    image_center = (M + m) * 0.5

    img = img - image_center
    img = img * (final_radius / image_radius) + final_center
    return img