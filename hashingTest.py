import hashlib, os, sys, pickle
from py_essentials import xcptns

def getHashes():
    list = []
    for root, dirs, files in os.walk("C:\\Users\\Justin Moser\\Downloads", topdown=True):
        for name in files:
            filename = (os.path.join(root, name))
            printing = True
            blocksize = 65536
            hasher = hashlib.sha1()
            with open(filename, 'rb') as afile:
                buf = afile.read(65536)
                hasher.update(buf)
                checksum = hasher.hexdigest()
                print(checksum)
            with open("hashes.txt", 'w') as of: # Open 'hashes.txt' als output file
                of.write(checksum)

def main():
    getHashes()


if __name__ == '__main__':
    main()