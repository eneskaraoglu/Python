import pandas as pd

class SorumluGelistiriciChecker:
    def __init__(self, file_path):
        # CSV dosyasını yükle ve DataFrame olarak sakla.
        self.df = pd.read_csv(file_path, sep=",", encoding="utf-8")
    
    def check_missing(self):
        """
        'Sorumlu Geliştirici' sütunundaki eksik değerlerin sayısını hesaplar ve yüzde olarak çıktı verir.
        """
        total_count = self.df["Sorumlu Geliştirici"].shape[0]
        missing_count = self.df["Sorumlu Geliştirici"].isnull().sum()
        missing_percentage = (missing_count / total_count) * 100
        print(f"'Sorumlu Geliştirici' sütununda {missing_count} eksik değer bulunuyor (%{missing_percentage:.2f}).")
        return missing_count

    def missing_indices(self):
        """
        Eksik değere sahip satırların indekslerini liste olarak döner.
        """
        missing_idx = self.df[self.df["Sorumlu Geliştirici"].isnull()].index.tolist()
        print("Eksik değer bulunan satır indeksleri:", missing_idx)
        return missing_idx

# Sınıfı kullanmak için örnek kullanım
if __name__ == "__main__":
    # Dosya yolunu kendi dosya konumunuza göre ayarlayın.
    file_path = r'C:\Users\enesk\Downloads\jira.csv'
    checker = SorumluGelistiriciChecker(file_path)
    
    # Eksik değer sayısını kontrol et
    checker.check_missing()
    
    # Eksik değer bulunan satır indekslerini getir
    checker.missing_indices()
