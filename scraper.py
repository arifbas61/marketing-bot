import os
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def pazarlama_verisi_topla():
    # Hedef pazarlama/rakip analiz url'si (Örnektir, hedef sitenize göre güncelleyebilirsiniz)
    url = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"[{datetime.now()}] Veri toplama işlemi başladı...")
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Hata: Siteye erişilemedi. Durum Kodu: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="product_pod")
    
    veri_listesi = []
    tarih_damgasi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for product in products:
        urun_adi = product.h3.a["title"]
        fiyat = product.find("p", class_="price_color").text.strip()
        stok_durumu = product.find("p", class_="instock availability").text.strip()

        veri_listesi.append({
            "Tarih": tarih_damgasi,
            "Ürün Adı": urun_adi,
            "Fiyat": fiyat,
            "Stok Durumu": stok_durumu
        })

    # Verileri CSV dosyasına yazma/ekleme (Append modu)
    dosya_adi = "pazarlama_verileri.csv"
    dosya_mevcut_mu = os.path.isfile(dosya_adi)

    with open(dosya_adi, mode="a", newline="", encoding="utf-8") as file:
        alanlar = ["Tarih", "Ürün Adı", "Fiyat", "Stok Durumu"]
        writer = csv.DictWriter(file, fieldnames=alanlar)
        
        if not dosya_mevcut_mu:
            writer.writeheader()  # Dosya ilk kez oluşuyorsa başlıkları ekle
            
        writer.writerows(veri_listesi)

    print(f"Başarılı: {len(veri_listesi)} adet ürün verisi '{dosya_adi}' dosyasına kaydedildi.")

if __name__ == "__main__":
    pazarlama_verisi_topla()
