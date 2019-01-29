"""
Author:  Justin Moser, S1103774
Summary: - get_pathname_and_hashes function
                Getting user input from 'start_menu.py'
                Making MD5 hashes of all the files on a system under 'x' size
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
         - hash_single_file function
                Getting user input from 'start_menu.py'
                Making the MD5 hash of the user-selected file
                Storing the file path and MD5 hash in a CSV-file
                Storing MD5 hash in a TXT-file
         - hash_single_folder function
                Getting user input from 'start_menu.py'
                Making MD5 hashes of all the files in a user-selected folder
                Storing file paths and MD5 hashes in a CSV-file
                Storing MD5 hashes in a TXT-file
         - hash_folder_limited_size function
                Getting user input from 'start_menu.py'
                Making MD5 hashes of all the files in a user-selected folder under 'x' size
                Storing file paths and MD5 hashes in a CSV-file
                Storing MD5 hashes in a TXT-file

Update: Daan Schellingerhoudt, S1108356
    - Added hash_single_file, hash_single_folder, hash_folder_limited_size
"""

import hashlib, os, csv, datetime
import win32api # pip install pypiwin32

drives = win32api.GetLogicalDriveStrings() # Checks how many drives are in the system
drives = drives = drives.split('\000')[:-1]

# Description of the function is in the summary
def get_pathname_and_hashes(file_size):

    file_size = file_size * 1048576 # Conversion from 1 byte to 1MB

    for drive in drives: # This will be executed for every drive in the system

        # Scans the root and all the files on the drive(s)
        for root, dirs, files in os.walk(drive, topdown=True):
            try:
                for name in files: # This will be executed for every file on the system
                    time = datetime.datetime.now() # Time and date will be logged to the console
                    filename = (os.path.join(root, name))
                    # If the file is smaller or as big as the user input
                    if os.path.getsize(filename) <= file_size:
                        # Name of the path and MD5 hash will be saved in a dictionary
                        path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(), filename)])
                        print(str(time) + " " + str(path_dict))

                        with open('path_and_hash.csv', 'a') as f:
                            writer = csv.writer(f)
                            # The items of path_dict (keys en values) will be saved in a text-file
                            for key, value in path_dict.items():
                                writer.writerow([key, value])

                        with open('system_hashes.txt', 'a') as e:
                            # Every key (the hashes) in path_dict will be saved in a text-file
                            for key in path_dict.keys():
                                e.write('{}\n'.format(key))

            # If these errors occur while scanning a file, this file will be skipped
            except (IOError, PermissionError, MemoryError, FileNotFoundError, UnicodeEncodeError) as x:
                print(x)

# Description of the function is in the summary
def hash_single_file(single_file):

    filename = single_file

    try:
        time = datetime.datetime.now() # Time and date will be logged to the console
        # Name of the path and MD5 hash will be saved in a dictionary
        path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(), filename)])
        print(str(time) + " " + str(path_dict))

        with open('path_and_hash.csv', 'a') as f:
            writer = csv.writer(f)
            # The items of path_dict (key en value) will be saved in a text-file
            for key, value in path_dict.items():
                writer.writerow([key, value])

        with open('system_hashes.txt', 'a') as e:
            # The key (the hash) in path_dict will be saved in a text-file
            for key in path_dict.keys():
                e.write('{}\n'.format(key))

    # If these errors occur while scanning the file, this file will be skipped 
    except (IOError, PermissionError, MemoryError, FileNotFoundError, UnicodeEncodeError) as x:
        print(x)

# Description of the function is in the summary
def hash_single_folder(single_folder):

    for root, dirs, files in os.walk(single_folder, topdown=True):
        try:
            for name in files:  # This will be executed for every file on the system
                time = datetime.datetime.now() # Time and date will be logged to the console
                filename = (os.path.join(root, name))
                # Name of the path and MD5 hash will be saved in a dictionary
                path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(), filename)])
                print(str(time) + " " + str(path_dict))

                with open('path_and_hash.csv', 'a') as f:
                    writer = csv.writer(f)
                    # The items of path_dict (keys en values) will be saved in a text-file
                    for key, value in path_dict.items():
                        writer.writerow([key, value])

                with open('system_hashes.txt', 'a') as e:
                    # Every key (the hashes) in path_dict will be saved in a text-file
                    for key in path_dict.keys():
                        e.write('{}\n'.format(key))

        # If these errors occur while scanning a file, this file will be skipped
        except (IOError, PermissionError, MemoryError, FileNotFoundError, UnicodeEncodeError) as x:
            print(x)

# Description of the function is in the summary
def hash_folder_limited_size(file_size, single_folder):

    file_size = file_size * 1048576 # Conversion from 1 byte to 1MB

    # Scans the root and all the files on the drive(s)
    for root, dirs, files in os.walk(single_folder, topdown=True):
        try:
            for name in files: # This will be executed for every file on the system
                time = datetime.datetime.now() # Time and date will be logged to the console
                filename = (os.path.join(root, name))
                if os.path.getsize(filename) <= file_size:
                    # Name of the path and MD5 hash will be saved in a dictionary
                    path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(), filename)])
                    print(str(time) + " " + str(path_dict))

                    with open('path_and_hash.csv', 'a') as f:
                        writer = csv.writer(f)
                        # The items of path_dict (keys en values) will be saved in a text-file
                        for key, value in path_dict.items():
                            writer.writerow([key, value])

                    with open('system_hashes.txt', 'a') as e:
                        # Every key (the hashes) in path_dict will be saved in a text-file
                        for key in path_dict.keys():
                            e.write('{}\n'.format(key))

        # If these errors occur while scanning a file, this file will be skipped
        except (IOError, PermissionError, MemoryError, FileNotFoundError, UnicodeEncodeError) as x:
            print(x)

# Description of the function is in the summary
def hashing_without_limitations():

    for drive in drives: # This will be executed for every drive in the system

        # Scans the root and all the files on the drive(s)
        for root, dirs, files in os.walk(drive, topdown=True):
            try:
                for name in files: # This will be executed for every file on the system
                    time = datetime.datetime.now() # Time and date will be logged to the console
                    filename = (os.path.join(root, name))
                    # Name of the path and MD5 hash will be saved in a dictionary
                    path_dict = dict([(hashlib.md5(open(filename, 'rb').read()).hexdigest(), filename)])
                    print(str(time) + " " + str(path_dict))

                    with open('path_and_hash.csv', 'a') as f:
                        writer = csv.writer(f)
                        # The items of path_dict (keys en values) will be saved in a text-file
                        for key, value in path_dict.items():
                            writer.writerow([key, value])

                    with open('system_hashes.txt', 'a') as e:
                        for key in path_dict.keys(): # Every key (the hashes) in path_dict will be saved in a text-file
                            e.write('{}\n'.format(key))

            # If these errors occur while scanning a file, this file will be skipped
            except (IOError, PermissionError, MemoryError, FileNotFoundError, UnicodeEncodeError) as x:
                print(x)

# Description of the function is in the summary
def convert_md5_to_sha1():
    with open('path_and_hash.csv', 'r') as e: # The file with pathnames and hashes will be opened
        path_dict = dict(filter(None, csv.reader(e))) # The CSV-file will be transformed in a dictionary

    lines = [line.rstrip('\n') for line in open('virusshare_matches.txt')] # Virusshare matches are turned into a list

    for key, value in path_dict.items(): # For all the items in the dictonary (hashes and pathnames)
        hash = key
        padnaam = value
        filename = os.path.join(padnaam)
        if hash in lines: # If a key in the dictionary is the same as a line in Virusshare matches, do this:
            # A SHA1-hash will be generated of de given pathname
            checksum = hashlib.sha1(open(filename, 'rb').read()).hexdigest()
            with open('malware_hashes.txt', 'a') as f:  #
                # The SHA1-hashes of the infected files will be saved in a text-file
                f.write('{}\n'.format(checksum))
            print(checksum)

            with open('malware_sha_path.csv', 'a') as f:
                writer = csv.writer(f)
                # The SHA1 hash and pathname of the malware are saved in a CSV-file
                writer.writerow([checksum, padnaam])

    return checksum
