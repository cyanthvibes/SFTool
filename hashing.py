# SFT Tool
# Hashing
# Justin Moser, s1103774

# pip install pypiwin32
import hashlib, os, sys, win32api

def getHashes():
    drives = win32api.GetLogicalDriveStrings() # Berekend het aantal schijven
    drives = drives = drives.split('\000')[:-1]

    for drive in drives: # Voor elke schijf in het systeem wordt de loop uitgevoerd
        for root, dirs, files in os.walk(drive, topdown=True): # Scant de root en alle onderliggende mappen en bestanden op de drive(s)
            files = [fi for fi in files if not fi.endswith(('.sys', '.dll'))] # Zorgt ervoor dat alle system en dll files worden overgeslagen
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

def main():
    getHashes()

if __name__ == '__main__':
    main()