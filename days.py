import pandas as pd
import json

# Load data from a CSV file with all LayerZero transactions
csv_file_path = 'layerzero.csv'  # Specify the path to your CSV file
data = pd.read_csv(csv_file_path)

# Formatting and filtering data
data['SOURCE_TIMESTAMP_UTC'] = pd.to_datetime(data['SOURCE_TIMESTAMP_UTC']).dt.strftime('(%Y-%m-%d)')
addresses = data['SENDER_WALLET'].unique()

# Reading cluster addresses from our report
txt_file_path = 'path_to_your_addresses_file.txt'  # Specify the path to your TXT file
with open(txt_file_path, 'r') as file:
    all_addresses = [line.strip() for line in file.readlines()]

# Creating a dictionary for JSON
json_data = {}

for address in all_addresses:
    # Getting all corresponding dates for this address
    if address in addresses:
        dates = data[data['SENDER_WALLET'] == address]['SOURCE_TIMESTAMP_UTC'].tolist()
        dates.sort()
        key = str(dates)
        if key in json_data:
            json_data[key].append(address)
        else:
            json_data[key] = [address]

# Saving data to a JSON file
json_file_path = 'output.json'  # Specify the desired path for the JSON file
with open(json_file_path, 'w') as file:
    json.dump(json_data, file, indent=2)

print("JSON file has been successfully saved.")