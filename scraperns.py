import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- Replace these if needed ---
from_date = "01-06-2024"
to_date = "21-06-2024"
# Tokens you extracted from DevTools — may need to be dynamic if they expire
scid = "exqbc96408fxeyxpewiqyroduwgu2db31ss3walh"
tok = "cfbbe8bd52f0c755ca2540e9c8072f4cde64b325"
captcha_val = "3"

# Set up params
params = {
    "from_date": from_date,
    "to_date": to_date,
    "scid": scid,
    "tok_2609d153df4434d2b47decb8b70f37c414ef760a": tok,
    "siwp_captcha_value": captcha_val,
    "es_ajax_request": "1",
    "submit": "Search",
    "action": "get_judgements_judgement_date",
    "language": "en"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Referer": "https://www.sci.gov.in/judgements-judgement-date/"
}

# Make the request
url = "https://www.sci.gov.in/wp-admin/admin-ajax.php"
response = requests.get(url, params=params, headers=headers)

if response.status_code != 200:
    print(f"❌ Request failed with status code {response.status_code}")
    exit()

# Parse the embedded HTML
json_data = response.json()
html_content = json_data.get("resultsHtml", "")
soup = BeautifulSoup(html_content, "html.parser")

# Extract judgment rows
table = soup.find("table")
if not table:
    print("⚠️ Table not found in resultsHtml.")
    exit()

rows = table.find_all("tr")
data = []

for row in rows:
    cols = row.find_all("td")
    if len(cols) >= 2:
        title = cols[0].get_text(strip=True)
        # Get all judgment links
        links = cols[1].find_all("a")
        for link in links:
            href = link.get("href")
            text = link.get_text(strip=True)
            if href:
                data.append({
                    "Case Title": title,
                    "Label": text,
                    "Download Link": href
                })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("sci_judgments_final.csv", index=False)
print("✅ Scraped and saved sci_judgments_final.csv")
print(df.head())
