"""

Author:  Justin Moser, S1103774

Summary: - get_pathname_and_hashes function
                Making MD5 hashes of all the files on a system
                Storing file paths and MD5 hashes in a CSV-file
                Storing MD5 hashes in a TXT-file
         - convert_md5_to_sha1 function
                Opening the 'virusshare.txt'-file which contains the infected MD5-hashes
                Finding the same hashes in the 'path_and_hash.csv'-file
                Obtaining the path of these infected files
                Making a SHA1-hash of the files and storing them in 'malware_hashes.txt'

"""

import hashlib, os, sys, csv
import win32api # pip install pypiwin32

drives = win32api.GetLogicalDriveStrings()  # Berekend het aantal schijven
drives = drives = drives.split('\000')[:-1]

# Omschrijving van de functie staat in de summary
def get_pathname_and_hashes(): #
    for drive in drives: # Voor elke schijf in het systeem wordt de loop uitgevoerd

        for root, dirs, files in os.walk(drive, topdown=True): # Scant de root en alle onderliggende mappen en bestanden op de drive(s)
            try:
                for name in files: # Voor elk bestand wordt de loop uitgevoerd
                    filename = (os.path.join(root, name))
                    if os.path.getsize(filename) <= 1000000: # Voer de loop uit als de bestanden kleiner of gelijk zijn aan 10MB (voor demo)
                        blocksize = 65536
                        path_dict = dict([(filename, hashlib.md5(open(filename, 'rb').read()).hexdigest())]) # De padnaam en de MD5 hash worden opgeslagen in een dictionary
                        print(path_dict) # Zodat er kan worden gezien of het werkt

                        with open('path_and_hash.csv', 'a') as f: # Er wordt een CSV-bestand geopend
                            writer = csv.writer(f)
                            for key, value in path_dict.items(): # De items (keys en values) worden naar dit bestand toe geschreven
                                writer.writerow([key, value])

                        with open('system_hashes.txt', 'a') as e: # Er wordt een TXT-bestand geopend
                            for value in path_dict.values(): # Elke value (de hashes) in hash_dict worden naar dit bestand toegeschreven
                                e.write('{}\n'.format(value))
            except (IOError, PermissionError, MemoryError, FileNotFoundError) as x: # Als deze errors voorkomen, dan worden deze bestanden overgeslagen zonder dat het programma stopt
                print(x)

    return path_dict

# Omschrijving van de functie staat in de summary
def convert_md5_to_sha1():
    with open('path_and_hash.csv', 'r') as e: # Het bestand met de padnamen en MD5 hashes wordt geopend
        path_dict = dict(filter(None, csv.reader(e))) # Het CSV-bestand wordt omgezet in een dictionary

    md5_hash_list = [] # Een lijst waar de MD5 hashes in komen te staan
    lines = [line.rstrip('\n') for line in open('virusshare_hashes.txt')] # Het bestand met daarin de MD5 matches van Virusshare wordt hier geopend
    for line in lines: # Voor elke regel in het bestand wordt de loop uitgevoerd
        md5_hash_list.append(line) # Elke hash wordt in de lijst opgeslagen

    for key, value in path_dict.items(): # Er wordt door alle items in de dictionary gelooped

        if value in md5_hash_list: # Als de value (hash) voorkomt in 'virusshare_hashes.txt', doe het volgende:
            padnaam = key # De variabele padnaam is nu de key van de dictionary
            filename = os.path.join(padnaam)
            checksum = hashlib.sha1(filename.encode('utf-8')).hexdigest() # Er wordt een SHA1-hash berekend van het bestand in het opgegeven pad
            print(checksum)

            with open('malware_hashes.txt', 'a') as f:  # Er wordt een TXT-bestand geopend
                f.write('{}\n'.format(checksum)) # De SHA1-hashes van geïnfecteerde bestanden wordt hier naartoe geschreven

    return checksum

def main():
    get_pathname_and_hashes()
    convert_md5_to_sha1()

if __name__ == '__main__':
    main()
