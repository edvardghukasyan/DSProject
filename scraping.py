import requests
from io import StringIO
import pandas as pd

#scraping url to get data
def scrape_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text))
            return data
        else:
            print(f"Failed to retrieve data, status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
