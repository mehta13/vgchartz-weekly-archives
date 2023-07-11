import pandas as pd
from bs4 import BeautifulSoup
import requests

# Read the transformed data file
df_links = pd.read_csv('C:/Users/anchi/OneDrive/Documents/GitHub/vgchartzScrape/transformed_data.csv')

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
    game_sales_table = soup.find_all('table')[10]
    rows = game_sales_table.find_all('tr')

    game_sales_data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        game_info = cols[0].text.strip()
        game_info_parts = game_info.split('(')
        game_name = game_info_parts[0].strip()
        game_platform = game_info_parts[1].replace(")", "").strip() if len(game_info_parts) > 1 else None
        weekly_sales = cols[1].text.strip()
        total_sales = cols[2].text.strip()
        game_sales_data.append([game_name, game_platform, weekly_sales, total_sales])

    df_games = pd.concat([df_games, pd.DataFrame(game_sales_data, columns=['Game Name', 'Platform', 'Weekly Sales', 'Total Sales'])], ignore_index=True)

    print(f'Parsed game sales data from {url}')

    # Parse hardware by platform table
    hardware_table = soup.find_all('table')[13]
    rows = hardware_table.find_all('tr')

    hardware_data = []
    for row in rows[1:-1]:
        cols = row.find_all('td')
        platform = cols[0].text.strip()
        weekly_change = cols[1].text.strip()
        total = cols[2].text.strip()
        hardware_data.append([platform, weekly_change, total])

    df_hardware = pd.concat([df_hardware, pd.DataFrame(hardware_data, columns=['Platform', 'Weekly Change', 'Total'])], ignore_index=True)

    print(f'Parsed hardware data from {url}')

    # Parse software by platform table
    software_table = soup.find_all('table')[15]
    rows = software_table.find_all('tr')

    software_data = []
    for row in rows[1:-1]:
        cols = row.find_all('td')
        platform = cols[0].text.strip()
        weekly_change = cols[1].text.strip()
        total = cols[2].text.strip()
        software_data.append([platform, weekly_change, total])

    df_software = pd.concat([df_software, pd.DataFrame(software_data, columns=['Platform', 'Weekly Change', 'Total'])], ignore_index=True)

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
