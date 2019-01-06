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
         - hashing_demo function
                Creating the hashes of a given directory
                This script will be used in the demo instead of 'get_pathname_and_hashes' because the lack of time

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
                    if os.path.getsize(filename) <= 10: # Voer de loop uit als de bestanden kleiner of gelijk zijn aan 10MB (voor demo)
                        blocksize = 65536
                        path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(), filename)]) # De padnaam en de MD5 hash worden opgeslagen in een dictionary
                        print(path_dict) # Zodat er kan worden gezien of het werkt

                        with open('path_and_hash.csv', 'a') as f: # Er wordt een CSV-bestand geopend
                            writer = csv.writer(f)
                            for key, value in path_dict.items(): # De items (keys en values) worden naar dit bestand toe geschreven
                                writer.writerow([key, value])

                        with open('system_hashes.txt', 'a') as e: # Er wordt een TXT-bestand geopend
                            for value in path_dict.values(): # Elke value (de hashes) in hash_dict worden naar dit bestand toegeschreven
                                e.write('{}\n'.format(key))
            except (IOError, PermissionError, MemoryError, FileNotFoundError) as x: # Als deze errors voorkomen, dan worden deze bestanden overgeslagen zonder dat het programma stopt
                print(x)

    return path_dict


# Omschrijving staat in de summary
def hashing_demo():
    for root, dirs, files in os.walk("C:\\Users\\Justin Moser\\Desktop\\git", topdown=True): # Vul het directory path in (dit is een voorbeeld)
        try:
            for name in files:  # Voor elk bestand wordt de loop uitgevoerd
                filename = (os.path.join(root, name))
                blocksize = 65536
                path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(),filename)])  # De padnaam en de MD5 hash worden opgeslagen in een dictionary
                print(path_dict)  # Zodat er kan worden gezien of het werkt

                with open('path_and_hash.csv', 'a') as f:  # Er wordt een CSV-bestand geopend
                    writer = csv.writer(f)
                    for key, value in path_dict.items():  # De items (keys en values) worden naar dit bestand toe geschreven
                        writer.writerow([key, value])

                with open('system_hashes.txt', 'a') as e:  # Er wordt een TXT-bestand geopend voor value in path_dict.values():
                    e.write('{}\n'.format(key)) #  Elke key (de hashes) in hash_dict worden naar dit bestand toegeschreven
        except (IOError, PermissionError, MemoryError, FileNotFoundError) as x:  # Als deze errors voorkomen, dan worden deze bestanden overgeslagen zonder dat het programma stopt
            print(x)

    return path_dict

# Omschrijving van de functie staat in de summary
def convert_md5_to_sha1():
    with open('path_and_hash.csv', 'r') as e: # Het bestand met de padnamen en MD5 hashes wordt geopend
        path_dict = dict(filter(None, csv.reader(e))) # Het CSV-bestand wordt omgezet in een dictionary

    lines = [line.rstrip('\n') for line in open('virusshare_matches.txt')]  # Het bestand met daarin de MD5 matches van Virusshare wordt hier geopend

    for key, value in path_dict.items(): # De loop gaat over alle items in de dictionary
        hash = key
        padnaam = value
        filename = os.path.join(padnaam)
        if hash in lines: # Als de hash voorkomt in de dictionary, doe het volgende:
            checksum = hashlib.sha1(filename.encode('utf-8').hexdigest())  # Er wordt een SHA1-hash berekend van het bestand in het opgegeven pad
            with open('malware_hashes.txt', 'a') as f:  # Er wordt een TXT-bestand geopend
                f.write('{}\n'.format(checksum)) # De SHA1-hashes van geïnfecteerde bestanden wordt hier naartoe geschreven
            print(checksum)

            with open('malware_sha_path.csv', 'a') as f:  # Er wordt een CSV-bestand geopend
                writer = csv.writer(f)
                writer.writerow([checksum, padnaam])    # De sha1 waarde en de padnaam van de malware worden weggeschreven


def main():
    get_pathname_and_hashes()
    convert_md5_to_sha1()

if __name__ == '__main__':
    main()
