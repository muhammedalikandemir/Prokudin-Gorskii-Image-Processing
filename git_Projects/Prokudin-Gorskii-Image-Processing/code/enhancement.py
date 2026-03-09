import numpy as np 
import cv2


def gamma_correction(image, gamma=1.2):
    invGamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** invGamma * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)



def sharpen_image(image, amount=0.5, kernel_size=(5,5), sigma=1.0):
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharp = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
    return sharp



def auto_contrast(image, percentile=2):
    result = np.zeros_like(image)

    for c in range(3):
        channel = image[:,:,c]
        low = np.percentile(channel, percentile)
        high = np.percentile(channel, 100 - percentile)

        channel = np.clip((channel - low) * 255.0 / (high - low), 0, 255)
        result[:,:,c] = channel

    return result.astype(np.uint8)


def enhance_image(image):

    # 1. Otomatik kontrast
    img = auto_contrast(image, percentile=2)

    # 2. Gamma düzeltme
    img = gamma_correction(img, gamma=1.2)

    # 3. Keskinleştirme
    img = sharpen_image(img, amount=0.5)

    return img


def crop_edges(image, crop_percent=0.075):
    """
    Görüntünün kenarlarından otomatik olarak belirtilen yüzde oranında kırpar.
    Hizalama sonrası renkli bantları gidermek için kullanılır.
    """
    h, w = image.shape[:2]
    crop_h = int(h * crop_percent)
    crop_w = int(w * crop_percent)
    
    # Görüntüyü kırp
    cropped_image = image[crop_h:-crop_h, crop_w:-crop_w]
    return cropped_image