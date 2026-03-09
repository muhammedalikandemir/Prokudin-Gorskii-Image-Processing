import numpy as np

def apply_alignment(channel, dx, dy):
    # channel: 2D (grayscale) olmalı
    return np.roll(channel, shift=(dy, dx), axis=(0, 1))

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

def align_channels(reference, target, search_range=15, metric='ncc', edge_crop=0.1):
    
    
    # Kenar kırpma
    h, w = reference.shape
    crop_h = int(h * edge_crop)
    crop_w = int(w * edge_crop)
    
    ref_crop = reference[crop_h:-crop_h, crop_w:-crop_w]
    
    best_score = float('-inf') if metric == 'ncc' else float('inf')
    best_dx, best_dy = 0, 0
    
    # Tüm kaydırmaları dene
    for dy in range(-search_range, search_range + 1):
        for dx in range(-search_range, search_range + 1):
            # Target'ı kaydır
            shifted = np.roll(target, shift=(dy, dx), axis=(0, 1))
            
            # Aynı bölgeyi kırp
            shifted_crop = shifted[crop_h:-crop_h, crop_w:-crop_w]
            
            # Metrik hesapla
            if metric == 'ncc':
                score = ncc_metric(ref_crop, shifted_crop)
                if score > best_score:
                    best_score = score
                    best_dx, best_dy = dx, dy
            else:  # ssd
                score = ssd_metric(ref_crop, shifted_crop)
                if score < best_score:
                    best_score = score
                    best_dx, best_dy = dx, dy
    
    return best_dx, best_dy, best_score