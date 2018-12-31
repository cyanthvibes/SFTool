"""

Author: Justin Moser, S1103774
Summary: Making hashes of all the files on a system

"""

import hashlib
import os
import sys
import win32api # pip install pypiwin32
import ctypes

drives = win32api.GetLogicalDriveStrings()  # Berekend het aantal schijven
drives = drives = drives.split('\000')[:-1]

def calculate_hashes():
    for drive in drives: # Voor elke schijf in het systeem wordt de loop uitgevoerd

        for root, dirs, files in os.walk(drive, topdown=True): # Scant de root en alle onderliggende mappen en bestanden op de drive(s)
            files = [fi for fi in files if not fi.endswith(('.sys', '.dll'))]

            for name in files:
                filename = (os.path.join(root, name))
                blocksize = 65536
                hasher = hashlib.sha1() # Berekend een SHA1 hashwaarde

                with open(filename, 'rb') as afile:
                    buf = afile.read(65536)
                    hasher.update(buf)
                    checksum = hasher.hexdigest()
                    print(checksum)

                with open("hashes.txt", "a") as of: # Opent 'hashes.txt' als output file
                    of.write(checksum + "\n") # Print alle hashes naar 'hashes.txt', elke waarde op één lijn

def is_admin(): # Checkt of de gebruiker Admin-rechten heeft
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if is_admin():
        calculate_hashes()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

if __name__ == '__main__':
    main()
