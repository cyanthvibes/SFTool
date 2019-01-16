"""

Author:  Justin Moser, S1103774

Summary: - get_pathname_and_hashes function
                Getting user input from 'start_menu.py'
                Making MD5 hashes of all the files on a system
                Storing file paths and MD5 hashes in a CSV-file
                Storing MD5 hashes in a TXT-file
         - hashing_without_limitations function
                If user input from 'startmenu.py' is empty, this function will be started
                Making MD5 hashes of all the files on a system
                Storing file paths and MD5 hashes in a CSV-file
                Storing MD5 hashes in a TXT-file
         - convert_md5_to_sha1 function
                Opening the 'virusshare_matches.txt'-file which contains the infected MD5-hashes
                Finding the same hashes in the 'path_and_hash.csv'-file
                Obtaining the path of these infected files
                Making a SHA1-hash of the files and storing them in 'malware_hashes.txt'

"""

import hashlib, os, sys, csv
import win32api # pip install pypiwin32

drives = win32api.GetLogicalDriveStrings()  # Berekend het aantal schijven
drives = drives = drives.split('\000')[:-1]

# Omschrijving van de functie staat in de summary
def get_pathname_and_hashes(file_size):

    file_size = file_size * 1048576 # Conversie van 1 byte naar 1MB

    for drive in drives: # Voor elke schijf in het systeem wordt de loop uitgevoerd

        for root, dirs, files in os.walk(drive, topdown=True): # Scant de root en alle onderliggende mappen en bestanden op de drive(s)
            try:
                for name in files: # Voor elk bestand wordt de loop uitgevoerd
                    filename = (os.path.join(root, name))
                    if os.path.getsize(filename) <= file_size:
                        blocksize = 65536
                        path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(), filename)]) # De padnaam en de MD5 hash worden opgeslagen in een dictionary
                        print(path_dict)

                        with open('path_and_hash.csv', 'a') as f:
                            writer = csv.writer(f)
                            for key, value in path_dict.items(): # De items (keys en values) worden naar dit bestand toe geschreven
                                writer.writerow([key, value])

                        with open('system_hashes.txt', 'a') as e:
                            for key in path_dict.keys(): # Elke key (de hashes) in hash_dict worden naar dit bestand toegeschreven
                                e.write('{}\n'.format(key))

            except (IOError, PermissionError, MemoryError, FileNotFoundError, UnicodeEncodeError) as x: # Als deze errors voorkomen, dan worden deze bestanden overgeslagen zonder dat het programma stopt
                print(x)

    return file_size

# Omschrijving van de functie staat in de summary
def hashing_without_limitations():
    for drive in drives: # Voor elke schijf in het systeem wordt de loop uitgevoerd

        for root, dirs, files in os.walk(drive, topdown=True): # Scant de root en alle onderliggende mappen en bestanden op de drive(s)
            try:
                for name in files: # Voor elk bestand wordt de loop uitgevoerd
                    filename = (os.path.join(root, name))
                    blocksize = 65536
                    path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(), filename)]) # De padnaam en de MD5 hash worden opgeslagen in een dictionary
                    print(path_dict)

                    with open('path_and_hash.csv', 'a') as f:
                        writer = csv.writer(f)
                        for key, value in path_dict.items(): # De items (keys en values) worden naar dit bestand toe geschreven
                            writer.writerow([key, value])

                    with open('system_hashes.txt', 'a') as e:
                        for key in path_dict.keys(): # Elke key (de hashes) in hash_dict worden naar dit bestand toegeschreven
                            e.write('{}\n'.format(key))

            except (IOError, PermissionError, MemoryError, FileNotFoundError, UnicodeEncodeError) as x: # Als deze errors voorkomen, dan worden deze bestanden overgeslagen zonder dat het programma stopt
                print(x)

# Omschrijving van de functie staat in de summary
def convert_md5_to_sha1():
    with open('path_and_hash.csv', 'r') as e: # Het bestand met de padnamen en MD5 hashes wordt geopend
        path_dict = dict(filter(None, csv.reader(e))) # Het CSV-bestand wordt omgezet in een dictionary

    lines = [line.rstrip('\n') for line in open('virusshare_matches.txt')] # Virusshare matches worden omgezet in list

    for key, value in path_dict.items(): # De loop gaat over alle items in de dictionary
        hash = key
        padnaam = value
        filename = os.path.join(padnaam)
        if hash in lines: # Als de hash voorkomt in de dictionary, doe het volgende:
            checksum = hashlib.sha1(open(filename, 'rb').read()).hexdigest() # Er wordt een SHA1-hash berekend van het bestand in het opgegeven pad
            with open('malware_hashes.txt', 'a') as f:  #
                f.write('{}\n'.format(checksum)) # De SHA1-hashes van geïnfecteerde bestanden worden naar het bestand toe geschreven
            print(checksum)

            with open('malware_sha_path.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([checksum, padnaam]) # De SHA1 waarde en de padnaam van de malware worden weggeschreven naar het bestand

    return checksum

def main():
    get_pathname_and_hashes()
    convert_md5_to_sha1()


if __name__ == '__main__':
    main()