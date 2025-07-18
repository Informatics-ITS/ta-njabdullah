from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from selenium.common.exceptions import TimeoutException, WebDriverException

# Daftar link
endpoints = ["guidance", "haram-and-forbidden", "zakat", "zina", "qiyamah", "shaitan", "prophet-ibrahim", "prophet-musa", "jinn",
             "jahannam", "jannah", "jesus-isa", "hypocrites", "rizq", "tawakkul"]

base_url = "https://myislam.org/quran-verses/"
results = []

for endpoint in endpoints:
    print(f"\nProcessing endpoint: {endpoint}")
    
    options = Options()
    options.headless = False
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
        driver.delete_all_cookies()
    except WebDriverException as e:
        print(f"Error initializing WebDriver: {e}")
        continue
    
    url = base_url + endpoint + "/"
    try:
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 3))
        
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dua-container"))
        )
        print("Content loaded")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.find_all("div", class_="dua-container")
        print(f"Found {len(containers)} dua-containers")

        for container in containers:
            title_div = container.find("div", class_="chapter-title")
            if title_div and title_div.find("a"):
                link = title_div.find("a")
                text = link.get_text(strip=True)
                if "Surah" in text and "Ayat" in text:
                    parts = text.split("Ayat")
                    surah = parts[0].replace("Surah", "").strip()
                    ayah = parts[1].strip()
                    results.append({
                        "List": endpoint,
                        "SurahNo": surah,
                        "AyahNo": ayah
                    })

    except TimeoutException:
        print(f"Timeout while loading {url}. Skipping...")
    except Exception as e:
        print(f"Error processing {url}: {e}")
    
    try:
        driver.quit()
    except Exception:
        pass
    
    time.sleep(random.uniform(3, 7))

df = pd.DataFrame(results)
df.to_csv("Dataset/quran_groundtruth.csv", index=False)
print("\nScraping completed. Saved as quran_groundtruth.csv")