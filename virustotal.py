# Mariska Temming, S1106242

import json
import requests
import os
import time


class Virustotal:
    def __init__(self, hash, key, output):
        self.hash = hash
        self.key = key
        self.output = output

    def get_hash(self):
        return self.hash

    def get_key(self):
        return self.key

    def get_output(self):
        return self.output


# checks if key is valid
def checkkey(key):
    try:
        if len(key) == 64:
            return key
        else:
            print("There is something wrong with your key. Not 64 Alpha Numeric characters.")
            exit()
    except Exception as e:
        print(e)


# checks if hashes appear valid
def check_hash(hash):
    try:
        if len(hash) == 32:     # MD5
            return hash
        elif len(hash) == 40:    # SHA-1
            return hash
        elif len(hash) == 64:   # SHA-256
            return hash
        else:
            print("The Hash input does not appear valid.")
            exit()
    except Exception as e:
        print(e)


def file_exists(filepath):
    try:
        if os.path.isfile(filepath):
            return filepath
        else:
            print("There is no file at:" + filepath)
            exit()
    except Exception as e:
        print(e)


def get_malware_name(key, hash):
    json_response = []

    params = {'apikey': key, 'resource': hash}
    url = requests.get('https://www.virustotal.com/vtapi/v2/file/report', params=params)
    try:
        json_response = url.json()
    except json.decoder.JSONDecodeError as e:
        print(e)
    print("json: " + str(json_response))

    if json_response != []:
        response = int(json_response.get('response_code'))

        if response == 0:
            print(hash + ' is not in Virus Total')
            result = None
        elif response == 1:
            positives = int(json_response.get('positives'))
            if positives == 0:
                print(hash + ' is not malicious')
                result = None
            else:
                print(hash + ' is malicious')
                result = json_response["scans"]["F-Secure"]["result"]
        else:
            print(hash + ' could not be searched. Please try again later.')
            result = None
    else:
        result = None

    return result


def main():
    input_file = 'malware_hashes.txt'
    file_exists(input_file)
    key = '672e7867c8c51efca05872894e865a92630883316d06d9d73b9284bc92977dd5'
    checkkey(key)

    with open(input_file) as malware_hashes:  # open text file with malware hashes and close automatically
        for line in malware_hashes.readlines():
            print("malware name: " + str(get_malware_name(key, line.rstrip())))
            check_hash(line.rstrip())

            # hier schrijven naar de database

            time.sleep(15)  # 4 requests to VirusTotal per minut, so there is a sleep needed


if __name__ == '__main__':
    main()
