# SFT Tool
# Hashing
# Justin Moser, s1103774

# Alle geïmporteerde libraries
from py_essentials import hashing as hs
import hashlib
import os
import platform
import json
from py_essentials import xcptns

# Genereert van elk bestand een hash
def fileChecksum(filename, algorithm='sha1', printing=False):
    if algorithm == "sha256":
        hasher = hashlib.sha256()
    elif algorithm == "sha512":
        hasher = hashlib.sha512()
    elif algorithm == "sha1":
        hasher = hashlib.sha1()
    else:
        raise xcptns.UnsupportedHashingalgorithm("fileChecksum()", algorithm, ["sha1", "sha265", "sha512"])
    try:
        try:
            with open(filename, 'rb') as afile:
                buf = afile.read(65536)
                while len(buf) > 0:
                    hasher.update(buf)
                    buf = afile.read(65536)
            checksum = hasher.hexdigest()
            if printing:
                print(filename + " - " + checksum)
            return checksum
        except PermissionError:
            return "ERROR"
    except Exception as e:
        raise xcptns.StrangeError("fileChecksum()", e)

# return True als het bestand bestaat, anders False
def isFile(object):
    try:
        os.listdir(object)
        return False
    except Exception:
        return True


# Maakt van de gehele directory, inclusief submappen en bestanden, een hash
def createHashtree(directory, algorithm='sha1'):
    if platform.system() == 'Windows':
        slash = '\\'
    directory = directory + slash
    checksum = ''
    jsonstring = '{'
    objects = os.listdir(directory) # De objecten zijn de mappen en onderliggende mappen en bestanden
    for i in range(0, len(objects)): # Deze loop wordt gedaan totdat alle objecten, dus alle mappen en bestanden voltooid zijn
        filename = directory + objects[i]
        if isFile(filename):
            checksum = fileChecksum(filename, algorithm)
            jsonstring = jsonstring + '"' + objects[i] + '":"' + str(checksum) + '",'
        else:
            if platform.system() == 'Windows':
                slash = '\\'
            jsonstring = jsonstring + '"' + objects[i] + '":' + createHashtree(directory + objects[i] + slash,
                                                                               algorithm) + ','
    if jsonstring[-1] == "{":
        jsonstring = jsonstring + "}"
    else:
        jsonstring = jsonstring[:-1] + "}"
    return jsonstring

# Schrijft alle bestanden en hashes naar een bestand 'hashes.txt'
def writetoFile():
    with open("hashes.txt", 'w') as f:
        json.dump(data, f)
        json.dump(data1, f)
        json.dump(data2, f)

# Voert het gehele programma uit
if __name__ == "__main__":
    directory = os.path.join("C:", os.sep, "Users", "Justin Moser", "Desktop", "test") # De gehele C: schijf wordt meegenomen
    data = createHashtree(directory, "sha1")
    data1 = createHashtree(directory, "sha256")
    data2 = createHashtree(directory, "sha512")
    data = json.loads(data)
    data1 = json.loads(data1)
    data2 = json.loads(data2)
    print("De SHA-1 hashwaardes zijn:")
    print(json.dumps(data, sort_keys=True, indent=4))
    print("De SHA-256 hashwaardes zijn:")
    print(json.dumps(data1, sort_keys=True, indent=4))
    print("De SHA-512 hashwaardes zijn:")
    print(json.dumps(data2, sort_keys=True, indent=4))
    writetoFile()
