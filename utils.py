import pandas as pd
from bs4 import BeautifulSoup
import re

def get_sales_data(soup):
    sales_data = []
    sales_table = soup.find_all('table')[10]
    rows = sales_table.find_all('tr')
    for row in rows[1:]:
        cols = row.find_all('td')
        game_info = cols[0].text.strip()
        game_info_parts = game_info.split('(')
        game_name = game_info_parts[0].strip()
        game_platform = game_info_parts[1].replace(")", "").strip() if len(game_info_parts) > 1 else None
        weekly_sales = cols[1].text.strip()
        total_sales = cols[2].text.strip()
        sales_data.append([game_name, game_platform, weekly_sales, total_sales])
    return pd.DataFrame(sales_data, columns=['Game Name', 'Platform', 'Weekly Sales', 'Total Sales'])

def get_platform_data(soup, table_index):
    platform_data = []
    platform_table = soup.find_all('table')[table_index]
    rows = platform_table.find_all('tr')
    for row in rows[1:-1]:
        cols = row.find_all('td')
        platform = cols[0].text.strip()
        weekly_change = cols[1].text.strip()
        total = cols[2].text.strip()
        platform_data.append([platform, weekly_change, total])
    return pd.DataFrame(platform_data, columns=['Platform', 'Weekly Change', 'Total'])
