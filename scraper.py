import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Browser Setup
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 1: Updated URL (Latest IMDb Release Calendar)
url = "https://www.imdb.com/calendar/?region=IN&type=movie"
driver.get(url)
time.sleep(8) # Page load aaga wait pannunga

movies_data = []

# Step 2: Current IMDb Selector (ipc-metadata-list-summary-item)
items = driver.find_elements(By.CLASS_NAME, "ipc-metadata-list-summary-item")

print(f"Total {len(items)} movies found. Scraping...")

for item in items:
    try:
        # Title find panradhu
        title = item.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t").text
        # Storyline or Description text-a full-ah eduthukrom
        story = item.text.replace(title, "").strip() 
        
        if title and story:
            movies_data.append({"Movie Name": title, "Storyline": story})
    except:
        continue

# Step 3: Save to CSV (Idhu empty-ah iruka koodadhu)
df = pd.DataFrame(movies_data)
if not df.empty:
    df.to_csv("movies_2024.csv", index=False)
    print(f"Success! {len(df)} movies saved in movies_2024.csv")
else:
    print("Scraping Failed! Please check internet or IMDb URL.")

driver.quit()