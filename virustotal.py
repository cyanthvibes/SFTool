"""
Author: Mariska Temming, S1106242
Summary: - The class Virustotal contains virustotal information: hash (the malware hash),
            key (the public key of virustotal), input (a input file with the malware hashes)
         - Checks the key, hash and file if they are valid
         -
"""

import json
import requests     # pip install requests
import os
import time
import datetime
import csv

from malware import Malware
from database_helper import insert_data_malware_detection
from ranking_malware import ranking_malware_by_positives


class Virustotal:
    def __init__(self, hash, key, input):
        self.hash = hash
        self.key = key
        self.input = input

    def get_hash(self):
        return self.hash

    def get_key(self):
        return self.key

    def get_input(self):
        return self.input


# Checks if key is valid
def is_valid_key(key):
    if len(key) == 64:
        return True
    else:
        print("This key is not valid.")
        return False


# Checks if hashes appear valid
def is_valid_hash(hash):
    if len(hash) == 32:     # MD5
        return True
    elif len(hash) == 40:    # SHA-1
        return True
    elif len(hash) == 64:   # SHA-256
        return True
    else:
        print("The Hash: " + hash + " input does not appear to be valid.")
        return False


# Checks if file exists
def file_exists(filepath):
    try:
        if os.path.isfile(filepath):
            return filepath
        else:
            print("There is no file at:" + filepath)
            exit()
    except Exception as e:
        print(e)


# gets the malware name
def get_malware_name(key, hash):
    json_response = []

    params = {'apikey': key, 'resource': hash}
    url = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)   # Send request to VirusTotal
    try:
        json_response = url.json()
    except json.decoder.JSONDecodeError as e:
        print(e)
    print("json: " + str(json_response))   # Print the result of the request to VirusTotal in json format in the console

    if json_response != []:
        response = int(json_response.get('response_code'))  # Gets the response code

        if response == 0:
            print(hash + ' is not in Virus Total')
            result = None
        elif response == 1:
            positives = int(json_response.get('positives'))    # Gets the positives: amount of virusscanners who
            # detects the malware (hash)
            if positives == 0:
                print(hash + ' is not malicious')
                result = None
            else:
                print(hash + ' is malicious')
                result = json_response["scans"]["F-Secure"]["result"]   # Get the malware name from the virusscanner:
                # F-Secure

                total = json_response["total"]
                ranking_malware_by_positives(str(positives), str(total), str(result))
        else:
            print(hash + ' could not be searched. Please try again later.')
            result = None
    else:
        result = None

    return result


# Write malware detection data to the database
def register_malware_to_database():
    input_file = 'malware_hashes.txt'
    file_exists(input_file)
    key = '672e7867c8c51efca05872894e865a92630883316d06d9d73b9284bc92977dd5'

    if is_valid_key(key):
        with open(input_file) as malware_hashes:  # Opens a text file with the malware hashes and closes automatically
            for line in malware_hashes.readlines():
                hash = line.rstrip()
                if is_valid_hash(hash):
                    time_detection = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    malware_name = str(get_malware_name(key, hash))
                    print("Malware name: " + malware_name)
                    path = ''
                    with open('malware_sha_path.csv', 'r') as e:  # Opens file with path and sha1 hashes of the malware
                        malware_dict = dict(filter(None, csv.reader(e)))  # Convert CSV-file to a dictionary
                        path = malware_dict.get(hash)  # If the hash exists then get the path of that hash

                    malware = Malware(malware_name, hash, path, time_detection)
                    insert_data_malware_detection(malware)  # Write the malware detection data to the database

                time.sleep(15)  # There is a sleep needed because of the 4 requests per minut to VirusTotal


def main():
    register_malware_to_database()


if __name__ == '__main__':
    main()
