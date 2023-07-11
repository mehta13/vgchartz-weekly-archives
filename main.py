import pandas as pd
from bs4 import BeautifulSoup
import requests
from utils import get_sales_data, get_platform_data

# Read the transformed data file
df_links = pd.read_csv('transformed_data.csv')

# Initialize empty dataframes
df_games = pd.DataFrame()
df_hardware = pd.DataFrame()
df_software = pd.DataFrame()

for index, row in df_links.iterrows():
    url = row[0]  # First column is the URL

    # Skip if URL is invalid
    if pd.isnull(url) or 'http' not in url:
        continue

    # Fetch the webpage content
    response = requests.get(url)

    # Skip if fetch failed
    if response.status_code != 200:
        print(f'Failed to get data from {url}, status code: {response.status_code}')
        continue

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # Parse main game sales table
    df_games = pd.concat([df_games, get_sales_data(soup)], ignore_index=True)
    print(f'Parsed game sales data from {url}')

    # Parse hardware by platform table
    df_hardware = pd.concat([df_hardware, get_platform_data(soup, 1)], ignore_index=True)
    print(f'Parsed hardware data from {url}')

    # Parse software by platform table
    df_software = pd.concat([df_software, get_platform_data(soup, 2)], ignore_index=True)
    print(f'Parsed software data from {url}')

    # Save data to CSV files every 10 pages
    if index % 10 == 0:
        df_games.to_csv('games.csv', index=False)
        df_hardware.to_csv('hardware.csv', index=False)
        df_software.to_csv('software.csv', index=False)

# Save the dataframes to CSV files
df_games.to_csv('games.csv', index=False)
df_hardware.to_csv('hardware.csv', index=False)
df_software.to_csv('software.csv', index=False)

print('Scraping completed and data saved to CSV files')
