# Created by:
# Justin Moser

from py_essentials import hashing as hs
from pprint import pprint
import os

def hashingSHA1():
    path = os.path.join("C:") # Pad is de C: schijf
    hashtree = hs.createHashtree(path, 'sha1') # Van de directoy in 'path' wordt van alle onderliggende bestanden een sha1 hash berekend
    return hashtree

def hashingSHA256():
    path = os.path.join("C:")  # Pad is de C: schijf
    hashtree = hs.createHashtree(path, 'sha256') # Van de directoy in 'path' wordt van alle onderliggende bestanden een sha256 hash berekend
    return hashtree

def hashingSHA512():
    path = os.path.join("C:")  # Pad is de C: schijf
    hashtree = hs.createHashtree(path, 'sha512') # Van de directoy in 'path' wordt van alle onderliggende bestanden een sha512 hash berekend
    return hashtree

# De main klasse, pprint zorgt voor een 'Pretty-Print'
def main():
    print("De SHA1 hashwaardes zijn:")
    pprint(hashingSHA1())
    print("De SHA256 hashwaardes zijn:")
    pprint(hashingSHA256())
    print("De SHA512 hashwaardes zijn:")
    pprint(hashingSHA512())

# Voert de main functie uit
if __name__ == '__main__':
    main()
