from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
surah_data = []

for surah_num in range(1, 115):
    try:
        # URL untuk Surah berdasarkan nomor
        surah_url = f"https://quran.kemenag.go.id/quran/per-ayat/surah/{surah_num}?from=1&to=300"
        driver.get(surah_url)
        time.sleep(5)

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        surah_elements = driver.find_elements(By.CLASS_NAME, 'card-surah')

        for ayat_num, element in enumerate(surah_elements, start=1):
            try:
                surah_text = element.find_element(By.CLASS_NAME, 'arabic').text.strip()
                terjemahan_text = element.find_element(By.CLASS_NAME, 'surah-translate').text.strip()
                
                terjemahan_indonesia = element.find_elements(By.CLASS_NAME, 'surah-translate')[1].text.strip()

                if surah_text and terjemahan_text and terjemahan_indonesia:

                    surah_data.append([surah_num, ayat_num, surah_text, terjemahan_text, terjemahan_indonesia])

            except Exception as e:
                print(f"Error pada Surah {surah_num} Ayat {ayat_num}: {e}")

    except Exception as e:
        print(f"Gagal ambil data untuk Surah {surah_num}: {e}")

# Simpan ke CSV
with open('Dataset/quran_kemenag.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['SurahNo', 'AyahNor', 'ArabicText', 'LatinText', 'IndonesianText'])
    
    for row in surah_data:
        writer.writerow(row)

driver.quit()

print("Data sudah berhasil disimpan di 'quran_kemenag.csv'.")