"""

Author:  Justin Moser, S1103774
Summary: Making MD5 hashes of all the files on a system
         Storing file paths and hashes in a CSV-file
         Storing hashes in a TXT-file

"""

import hashlib
import os
import sys
import win32api # pip install pypiwin32
import ctypes
import csv

drives = win32api.GetLogicalDriveStrings()  # Berekend het aantal schijven
drives = drives = drives.split('\000')[:-1]

def get_pathname_and_hashes(): #
    for drive in drives: # Voor elke schijf in het systeem wordt de loop uitgevoerd

        for root, dirs, files in os.walk(drive, topdown=True): # Scant de root en alle onderliggende mappen en bestanden op de drive(s)
            try:
                for name in files: # Voor elk bestand wordt de loop uitgevoerd
                    filename = (os.path.join(root, name))
                    blocksize = 65536
                    hash_dict = dict([(filename, hashlib.md5(open(filename, 'rb').read()).hexdigest())]) # De padnaam en de MD5 hash worden opgeslagen in een dictionary
                    print(hash_dict) # Zodat er kan worden gezien of het werkt

                    with open('Test.csv', 'a') as f: # Er wordt een CSV-bestand geopend
                        writer = csv.writer(f)
                        for key, value in hash_dict.items(): # De items (keys en values) worden naar dit bestand toe geschreven
                            writer.writerow([key, value])

                    with open('Hashes.txt', 'a') as e: # Er wordt een TXT-bestand geopend
                        for value in hash_dict.values(): # Elke value (de hashes) in hash_dict worden naar dit bestand toegeschreven
                            e.write('{}\n'.format(value))
            except (IOError, PermissionError, FileNotFoundError) as x: # Als deze errors voorkomen, dan worden deze bestanden overgeslagen zonder dat het programma stopt
                print(x)

    return hash_dict
  
def main():
    get_pathname_and_hashes()

if __name__ == '__main__':
    main()
