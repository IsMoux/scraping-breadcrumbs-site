import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Config Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# ouvrire URL
url = 'https://www.edeka24.de/Lebensmittel/Suess-Salzig/Schokoriegel/'
driver.get(url)

#extraire breadcrumb 
breadcrumb_element = driver.find_element(By.CSS_SELECTOR, 'div.breadcrumb ul')
breadcrumb_items = breadcrumb_element.find_elements(By.CSS_SELECTOR, 'li > a')
breadcrumb_list = [item.text for item in breadcrumb_items]    
print(breadcrumb_list)

with open('breadcrumbs.csv', 'w') as file:
    for breadcrumb in breadcrumb_list:
            file.write(f"{breadcrumb}\n")


def clicker_button():
       
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element((By.ID, 'usercentrics-root'))
        )
        
        # attendre  button present au DOM
        voireplus_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'loader-btn'))
        )
        
        # Scroller vers le button
        driver.execute_script("arguments[0].scrollIntoView(true);", voireplus_button)
        
        # attendre jusqu'a le button soit  clickable
        voireplus_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'loader-btn'))
        )
        
        # Clicker avec JavaScript 
        driver.execute_script("arguments[0].click();", voireplus_button)


# Clicker le button
clicker_button()
time.sleep(3)  

# Extraire  information de produits
produits = driver.find_elements(By.CLASS_NAME, 'product-item')

produit_data = []
for product in produits:
    try:
        title_element = product.find_element(By.XPATH, ".//div[@class='product-details']/a[@class='title']/h2")
        title = title_element.text

        produit_data.append({
            'title': title,
        })
    except Exception as e:
        print(f"An error occurred while processing a product: {e}")

# sauvegarde de donnée en format csv
csv_file_path = 'products.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in produit_data:
        writer.writerow(item)

print(f"Data saved to {csv_file_path}")

# fermer le browser
driver.quit()
