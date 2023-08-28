import os
import requests
import csv
import time
import random
import argparse
import logging

def download_data(csv_file, data_folder):
    # Create the data folder if it does not exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Set up logging
    logging.basicConfig(filename=os.path.join(data_folder, 'failed_downloads.log'), level=logging.ERROR,
                        format='%(asctime)s %(levelname)s %(message)s')

    # Read the CSV file and download the images
    with open(csv_file, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            species_folder = os.path.join(data_folder, row['Species'])
            if not os.path.exists(species_folder):
                os.makedirs(species_folder)

            image_path = os.path.join(species_folder, row['ID'] + '.jpg')
            if not os.path.exists(image_path):
                try:
                    response = requests.get(row['URL'])
                    with open(image_path, 'wb') as image_file:
                        image_file.write(response.content)
                    # Wait for a random time between 1 and 2 seconds
                    # Can be removed if the link can handle mutliple requests repeatidily
                    time.sleep(random.uniform(1, 2))
                except Exception as e:
                    # Log the error message
                    logging.error(f"Failed to download {image_path}: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, required=True, help='CSV file containing the data')
    parser.add_argument('--data_folder', type=str, default='data', help='Folder to store the downloaded data')
    args = parser.parse_args()

    download_data(args.csv_file, args.data_folder)
