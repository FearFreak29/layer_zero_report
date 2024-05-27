import pandas as pd
import json

# Load data from a CSV file with all LayerZero transactions
csv_file_path = 'layerzero.csv'   # Specify the path to your CSV file
data = pd.read_csv(csv_file_path)

# Convert SOURCE_TIMESTAMP_UTC to datetime for sorting
data['SOURCE_TIMESTAMP_UTC'] = pd.to_datetime(data['SOURCE_TIMESTAMP_UTC'])

# Read unique wallet addresses from a TXT file
txt_file_path = 'path_to_your_addresses_file.txt'  # Replace with your actual file path
with open(txt_file_path, 'r') as file:
    wallet_addresses = [line.strip() for line in file.readlines()]

# Filter data for transactions involving the specified wallets
filtered_data = data[data['SENDER_WALLET'].isin(wallet_addresses)]

# Sort data by wallet and timestamp
sorted_data = filtered_data.sort_values(by=['SENDER_WALLET', 'SOURCE_TIMESTAMP_UTC'])

# Create a dictionary to format as JSON
json_data = {}

for wallet in wallet_addresses:
    wallet_data = sorted_data[sorted_data['SENDER_WALLET'] == wallet]
    if not wallet_data.empty:
        # Create the chain sequence by concatenating source and destination chains
        chain_sequence = wallet_data.apply(lambda x: f"{x['SOURCE_CHAIN']},{x['DESTINATION_CHAIN']}", axis=1).tolist()
        json_data[",".join(chain_sequence)] = [wallet]

# Saving data to a JSON file
json_file_path = 'output_chains.json'  # Specify the desired path for the JSON file
with open(json_file_path, 'w') as file:
    json.dump(json_data, file, indent=2)

print("JSON file has been successfully saved.")