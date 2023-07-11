# vgchartz-weekly-archives
This project consists of a set of Python scripts to scrape weekly video game sales data from VGChartz.

Files
main.py: The main script that orchestrates the scraping process.
utils.py: Contains utility functions for parsing the HTML content and extracting sales data.
Usage
Run the main.py script with Python 3. This script reads URLs from transformed_data.csv, fetches the webpages, and extracts sales data.

The script will create three CSV files: games.csv, hardware.csv, and software.csv. These files contain sales data for games, hardware, and software respectively.

Data
The scripts extract the following data:

Game sales data: game name, platform, weekly sales, total sales
Hardware data: platform, weekly change, total
Software data: platform, weekly change, total
