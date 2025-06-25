from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
time.sleep(2)  # just before filling dates

# Launch Chrome (headless optional)
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # comment this out to watch it
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the date filter page
driver.get("https://sci.gov.in/judgements-judgement-date/")
time.sleep(5)

with open("sci_debug.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

# Allow time for JS
# Corrected lowercase IDs
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "judgement_date1")))

start, end = "01-06-2024", "21-06-2024"
driver.execute_script(f"document.getElementById('judgement_date1').value = '{start}';")
driver.execute_script(f"document.getElementById('judgement_date2').value = '{end}';")

# If CAPTCHA exists, you may need to pause and solve manually:
input("👀 Solve CAPTCHA in browser, then press Enter here...")

# Submit the form
driver.find_element(By.XPATH, "//button[text()='Submit']").click()

# Wait for results
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#example tbody tr")))

rows = driver.find_elements(By.CSS_SELECTOR, "table#example tbody tr")
data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, "td")
    title = cols[0].text
    date = cols[1].text
    link = cols[2].find_element(By.TAG_NAME, "a").get_attribute('href')
    data.append({"Case Title": title, "Date": date, "Download Link": link})

df = pd.DataFrame(data)
df.to_csv("sci_judgments_selenium.csv", index=False)
print(df)

driver.quit()
