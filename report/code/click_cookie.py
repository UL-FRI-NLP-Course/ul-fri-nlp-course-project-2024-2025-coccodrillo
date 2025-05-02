import cv2
import numpy as np
import pyautogui

# Funzione per il multi-scale template matching
def multi_scale_template_matching(large_img, template, scales, method=cv2.TM_SQDIFF_NORMED):
    best_val = float('inf')
    best_rect = None

    for scale in scales:
        resized = cv2.resize(large_img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        if resized.shape[0] < template.shape[0] or resized.shape[1] < template.shape[1]:
            continue

        res = cv2.matchTemplate(resized, template, method)
        min_val, _, min_loc, _ = cv2.minMaxLoc(res)

        if min_val < best_val:
            best_val = min_val
            h, w = template.shape[:2]
            best_rect = (
                int(min_loc[0] / scale), int(min_loc[1] / scale)
            )

    return best_rect  # top-left corner del match

# Funzione per ottenere i pixel non bianchi
def get_pixels(large_img_path, template_path):
    # Carica le immagini
    large_img = cv2.imread(large_img_path)
    template = cv2.imread(template_path)

    if large_img is None or template is None:
        print("Errore nel caricamento delle immagini!")
        return []

    # Scelte di scala per il template matching
    scales = np.linspace(0.5, 1.5, 40)
    
    # Trova il miglior match
    top_left = multi_scale_template_matching(large_img, template, scales)
    if top_left is None:
        print("Nessun match trovato!")
        return []

    x_start, y_start = top_left
    h, w = template.shape[:2]
    
    # Lista per i pixel non bianchi
    non_white_pixels = []

    # Scorri attraverso i pixel del template nel match
    for y in range(h):
        for x in range(w):
            pixel = large_img[y_start + y, x_start + x]
            if not (pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240):  # non bianco
                non_white_pixels.append((y_start + y, x_start + x))

    return non_white_pixels







