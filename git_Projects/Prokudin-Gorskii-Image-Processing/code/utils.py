import numpy as np 
import cv2

def load_image(filepath):
    img = cv2.imread(filepath)
    if img is None:
        raise ValueError(f"Görüntü yüklenemdi: {filepath}")
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    return img_gray

def split_image(image):
    img = image
    if img is None:
        raise ValueError(f"Görüntü yüklenemedi: {image}")

    height = img.shape[0]
    third = height // 3

    b_part = img[0:third, :]          
    g_part = img[third:2*third, :]      
    r_part = img[2*third:3*third, :]  

    return b_part, g_part, r_part


def ssd_metric(img1, img2):
    if img1.shape != img2.shape:
        raise ValueError("Goruntuler ayni boyutta olmali")
    
    diff = img1.astype(np.float32) - img2.astype(np.float32)
    ssd = np.sum(diff ** 2)
    return ssd



def ncc_metric(img1, img2):
    if img1.shape != img2.shape:
        raise ValueError("Goruntuler ayni boyutta olmali")
    
    img1_norm = img1 - np.mean(img1)
    img2_norm = img2 - np.mean(img2)
    
    numerator = np.sum(img1_norm * img2_norm)
    denominator = np.sqrt(np.sum(img1_norm ** 2) * np.sum(img2_norm ** 2))
    
    if denominator == 0:
        return 0
    
    ncc = numerator / denominator
    
    return ncc


def create_color_image(b, g, r):
    color_img = cv2.merge([r, g, b])
    
    
    #color_img = cv2.normalize(color_img, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX)

    return color_img
