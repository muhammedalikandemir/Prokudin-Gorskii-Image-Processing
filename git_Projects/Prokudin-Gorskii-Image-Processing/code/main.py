import argparse
import os
import time
from pathlib import Path
import sys
import cv2

from alignment import align_channels, apply_alignment
from enhancement import crop_edges, enhance_image
from utils import create_color_image, load_image, split_image, ncc_metric, ssd_metric


def process_image(input_path, output_dir, metric='ncc', use_pyramid=False):
    _ = use_pyramid  # mevcut arayuzle uyumluluk

    print(f"\n{'=' * 60}")
    print(f"Isleniyor: {input_path}")
    print(f"{'=' * 60}")

    start_time = time.time()

    img = load_image(input_path)
    b, g, r = split_image(img)
    print(f"✓ Goruntu bolundu: {b.shape}")

    print(f"✓ Hizalama basliyor ({metric} metrigi)...")
    dx_g, dy_g, score_g = align_channels(b, g, metric=metric)
    dx_r, dy_r, score_r = align_channels(b, r, metric=metric)

    print(f"  Green: dx={dx_g}, dy={dy_g}, score={score_g:.4f}")
    print(f"  Red: dx={dx_r}, dy={dy_r}, score={score_r:.4f}")

    g_aligned = apply_alignment(g, dx_g, dy_g)
    r_aligned = apply_alignment(r, dx_r, dy_r)

    img_unaligned = create_color_image(b, g, r)
    img_aligned = create_color_image(b, g_aligned, r_aligned)

    print("✓ Goruntu iyilestirme...")
    img_enhanced = enhance_image(img_aligned)
    img_final = crop_edges(img_enhanced)

    base_name = Path(input_path).stem

    cv2.imwrite(
        f"{output_dir}/{base_name}_unaligned.jpg",
        cv2.cvtColor(img_unaligned, cv2.COLOR_RGB2BGR),
    )
    cv2.imwrite(
        f"{output_dir}/{base_name}_aligned.jpg",
        cv2.cvtColor(img_aligned, cv2.COLOR_RGB2BGR),
    )
    cv2.imwrite(
        f"{output_dir}/{base_name}_enhanced.jpg",
        cv2.cvtColor(img_final, cv2.COLOR_RGB2BGR),
    )

    elapsed_time = time.time() - start_time
    print(f"✓ Tamamlandi! Sure: {elapsed_time:.2f} saniye")

    return {
        'image': base_name,
        'g_shift': (dx_g, dy_g),
        'r_shift': (dx_r, dy_r),
        'time': elapsed_time,
    }


def main():
    parser = argparse.ArgumentParser(description='Prokudin-Gorskii Goruntu Isleme')
    parser.add_argument('--input', required=True, help='Girdi goruntusu veya klasoru')
    project_root = Path(__file__).resolve().parent.parent
    default_output = project_root / "results"
    parser.add_argument('--output', default=str(default_output), help='Cikti klasoru')
    parser.add_argument('--metric', default='ncc', choices=['ssd', 'ncc'])
    parser.add_argument('--pyramid', action='store_true', help='Piramit hizalama kullan')

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"HATA: Girdi yolu bulunamadi -> {input_path}")
        sys.exit(1)
    
    if not (input_path.is_file() or input_path.is_dir()):
        print(f"HATA: Girdi bir dosya veya klasor olmali -> {input_path}")
        sys.exit(1)    
        
    if input_path.is_file():
        files = [input_path]
    else:
        files = list(input_path.glob('*.jpg')) + list(input_path.glob('*.tif'))
        
    

    results = []
    for file in files:
        result = process_image(str(file), args.output, args.metric, args.pyramid)
        results.append(result)

    print(f"\n{'=' * 60}")
    print("OZET SONUCLAR")
    print(f"{'=' * 60}")
    print(f"{'Goruntu':<20} {'G Shift':<15} {'R Shift':<15} {'Sure (s)':<10}")
    print(f"{'-' * 60}")

    for r in results:
        print(f"{r['image']:<20} {str(r['g_shift']):<15} {str(r['r_shift']):<15} {r['time']:<10.2f}")


if __name__ == '__main__':
    main()
