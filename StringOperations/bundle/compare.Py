def dosya_icerigini_oku(dosya_yolu, karakter_seti='cp1254'):
    with open(dosya_yolu, 'r', encoding=karakter_seti) as dosya:
        return dosya.readlines()

def karşılaştır_ve_farkı_kaydet(dosya1_yolu, dosya2_yolu, fark_dosya_yolu):
    dosya1_icerik = dosya_icerigini_oku(dosya1_yolu)
    dosya2_icerik = dosya_icerigini_oku(dosya2_yolu)

    fark_listesi = []

    for deger2 in dosya2_icerik:
        if not any(deger2.strip() in deger1 for deger1 in dosya1_icerik):
            fark_listesi.append(deger2.strip())

    if fark_listesi:
        with open(fark_dosya_yolu, 'w') as fark_dosya:
            fark_dosya.write('\n'.join(fark_listesi))
        print("Farklar başarıyla kaydedildi.")
    else:
        print("Fark bulunamadı.")

# Örnek kullanım
dosya1_yolu = "MessagesBundle_en.properties"
dosya2_yolu = "output_stringsTR.txt"
fark_dosya_yolu = "farklar.txt"

karşılaştır_ve_farkı_kaydet(dosya1_yolu, dosya2_yolu, fark_dosya_yolu)
