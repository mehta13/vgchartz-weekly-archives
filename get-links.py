import openpyxl
import csv

# Load the Excel file
workbook = openpyxl.load_workbook('C:/Users/anchi/OneDrive/Documents/data2.xlsm')

# Select the specific sheet you want to work with
sheet = workbook['Sheet1']  # Replace 'Sheet1' with the actual sheet name

# Define the range to read (B1 to H1551)
start_row = 1
end_row = 1551
start_col = 2  # Column B
end_col = 8    # Column H

# Create a list to store the transformed data
transformed_data = []

# Iterate over the specified range and perform data manipulation
for row in sheet.iter_rows(min_row=start_row, max_row=end_row, min_col=start_col, max_col=end_col):
    for cell in row:
        if cell.hyperlink:
            link = cell.hyperlink.target

            # Extract region from the link
            region = link.split('/')[-2]

            # Extract date from the link
            date = link.split('/')[-3]

            # Append the transformed data to the list
            transformed_data.append([link, region, date])

# Define the output CSV file path
output_file = 'transformed_data.csv'

# Write the transformed data to the CSV file
with open(output_file, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Links", "Region", "Date"])
    writer.writerows(transformed_data)

print(f"Transformed data exported to '{output_file}' successfully.")
