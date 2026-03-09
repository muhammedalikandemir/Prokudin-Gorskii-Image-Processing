
# Tarihi Fotoğraf Renklendirme ve Hizalama

Bu proje, Prokudin-Gorskii formatındaki tek kare gri görüntülerden (üst üste duran B-G-R kanalları) renkli bir çıktı üretmek için hazırlanmış bir işleme akışıdır.

Temel olarak şu adımları uygular:
- Görüntüyü üç kanala ayırır
- Green ve Red kanallarını Blue kanalına göre hizalar
- Renkli görüntüyü birleştirir
- Kontrast/gamma/keskinlik iyileştirmesi yapar
- Hizalama sonrası kenar artefaktlarını kırpar

## Dizin Yapısı

- `code/main.py`: Uçtan uca çalışan CLI uygulaması
- `code/alignment.py`: Kanal hizalama fonksiyonları (`ssd` / `ncc`)
- `code/enhancement.py`: Görüntü iyileştirme ve kenar kırpma
- `code/utils.py`: Yükleme, kanal ayırma, metrik ve birleştirme yardımcıları
- `data/`: Girdi görüntüleri için ayrılmış klasör
- `results/`: Üretilen çıktılar

## Gereksinimler

Python 3.10+ önerilir.

Bağımlılıkları kurmak için:

```bash
cd code
pip install -r requirements.txt
```

## Kullanım

Tek dosya işlemek için:

```bash
python code/main.py --input "data/ornek.jpg"
```

Klasördeki tüm `.jpg` ve `.tif` dosyalarını işlemek için:

```bash
python code/main.py --input data
```

Farklı metrik ile çalıştırma:

```bash
python code/main.py --input "data/ornek.jpg" --metric ssd
```

Varsayılan çıktı klasörü `results/` dizinidir. İstenirse değiştirilebilir:

```bash
python code/main.py --input "data/ornek.jpg" --output "results"
```

## Çıktılar

Her girdi için üç dosya üretilir:
- `*_unaligned.jpg`: Hizalama öncesi birleştirilmiş görüntü
- `*_aligned.jpg`: Kanal hizalaması tamamlanmış görüntü
- `*_enhanced.jpg`: İyileştirme ve kırpma sonrası final görüntü



## Parametreler

`main.py` aşağıdaki argümanları destekler:
- `--input` (zorunlu): Dosya veya klasör yolu(olmayan bir dosya yolu verilirse kod çalışmayacaktır. Yolun Doğru olduğundan emin olun)
- `--output`: Çıktı klasörü (varsayılan: proje kökündeki `results/`)
- `--metric`: `ncc` veya `ssd` (varsayılan: `ncc`)
- `--pyramid`: Arayüzde mevcut, şu an aktif bir piramit implementasyonu kullanılmıyor

## Notlar

- Girdi görüntüsünün, yüksekliğinin 3 eşit parçaya bölünebildiği klasik Prokudin-Gorskii düzeninde olması beklenir.
- Hizalama `np.roll` tabanlı kaydırma ile yapılır ve kenar etkisini azaltmak için karşılaştırma sırasında iç bölge kullanılır.
