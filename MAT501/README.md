# MAT501 - Doktora yeterlik çalışma paketi

Bu klasör, birlikte hazırlanmış matematik PDF'lerini, üretim kodlarını ve yeni genel tekrar setini bir araya getirir. Son düzenleme: **17 Kasım 2026**.

## PDF rehberi

| Bölüm | İçerik | Dosya |
|---|---|---|
| Chapter 1 | Birinci mertebe ODE; özet ve çözümler, 18 sayfa | [Anlatım](output/pdf/MAT501_Chapter1_Ozet_ve_Cozumler.pdf) |
| Chapter 2 | Yüksek mertebe lineer ODE, 16 sayfa | [Anlatım](output/pdf/MAT501_Chapter2_Anlatim_ve_Cozumler.pdf) |
| Chapter 2 | 14 soru, 8 sayfa | [Alıştırmalar](output/pdf/MAT501_Chapter2_Karisik_Alistirmalar.pdf) |
| Chapter 2 | 14 sorunun kısa çözümleri, 8 sayfa | [Cevap anahtarı](output/pdf/MAT501_Chapter2_Alistirmalar_Cevap_Anahtari.pdf) |
| Chapter 4 | Seri çözümleri ve Frobenius, 13 sayfa | [Anlatım](output/pdf/MAT501_Chapter4_Anlatim_ve_Cozumler.pdf) |
| Chapter 4 | 12 soru, 7 sayfa | [Alıştırmalar](output/pdf/MAT501_Chapter4_Karisik_Alistirmalar.pdf) |
| Chapter 4 | 12 sorunun kısa çözümleri, 9 sayfa | [Cevap anahtarı](output/pdf/MAT501_Chapter4_Alistirmalar_Cevap_Anahtari.pdf) |
| Chapter 1 + 2 + 4 | **Yeni: Genel Tekrar 01**, 12 soru, 7 sayfa | [Yeni alıştırmalar](output/pdf/MAT501_Karisik_Genel_Tekrar_01.pdf) |

## Çalışma durumu

- Chapter 1, 2 ve 4'ün konu anlatım turları tamamlandı; bu, tüm alıştırmaların bağımsız çözülmüş olduğu anlamına gelmez.
- Chapter 5-6-7, matrisler, özdeğerler ve diferansiyel denklem sistemleri olarak hızlandırılmış çalışılacak.
- Chapter 3 (Laplace), kullanıcının tercihiyle en sona bırakıldı.
- Yeni Genel Tekrar 01 yalnızca çalışılan Chapter 1, 2 ve 4 kapsamındadır. Soru PDF'si cevap içermez. Doğrulama kodu çözüm verileri içerir.

## Soru düzeyi ve kaynak sınırı

Yeni soru hazırlamada referans gerçek vize sorularıdır. Bu çalışma klasöründe MAT501 vize örneği bulunmadığından Genel Tekrar 01'in vizeye göre zorluğu doğrulanamamıştır. Set, yüklenen Chapter 1, 2 ve 4 notları ve çalışılan örneklerle sınırlı tutulmuştur. Geçmiş final/yeterlik sorusu olduğu veya bunların düzeyini temsil ettiği iddia edilmez.

Özgün ders notları, kitaplar, öğrenci fotoğrafları ve başka derslerin dosyaları bu pakete eklenmedi. PDF'lerdeki örnekler bu hazırlık çalışmasında kullanılan örneklerdir.

## Üretim ve doğrulama kodu

Python 3.11+ ve bir sanal ortam önerilir. Gerekli paketleri yükleyip bu klasörün içinden aşağıdaki komutları çalıştırın:

```powershell
python -m pip install -r requirements.txt
python scripts/build_mat501_ch1.py
python scripts/build_mat501_ch2.py
python scripts/build_mat501_ch4.py
python scripts/build_mat501_answer_keys.py
python scripts/build_mat501_general_review.py
python scripts/validate_mat501_ch2.py
python scripts/validate_mat501_ch4.py
python scripts/validate_mat501_general_review.py
```

Üretim kodları `output/pdf/` altına yazar. Ara formül görselleri ve kontrol raporları `tmp/` altında tutulur ve Git'e eklenmez. Ortamdan bağımsız üretim için kodlarda Matplotlib ile gelen DejaVu fontları kullanılır; arşivlenmiş eski PDF'ler ilk üretimdeki fontlarını korur. Bu nedenle yeniden üretim birebir aynı PDF baytlarını vermeyebilir.

`manifest.json`, teslim edilen PDF'lerin SHA-256 ve Git blob kimliklerini içerir. Yeni setin denklem, başlangıç koşulu ve istisna kontrolleri `scripts/validate_mat501_general_review.py` içindedir.
