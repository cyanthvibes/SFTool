"""

Author:  Justin Moser, S1103774
Summary: - compare_hashes
                Compares all the virusshare hashes with the system hashes
                Writes the corresponding hashes to a file named "virusshare_matches.txt"
                The "virusshare_matches" file will be opened in hashing.py

"""

from difflib import Differ

def compare_hashes():
    with open('virusshare_hashes.txt') as f1, open('system_hashes.txt') as f2: # Opent 'virusshare_hashes.txt' en 'system_hashes.txt"
        for l1, l2 in zip(f1, f2):
            if l1 == l2: # Als de regels overeenkomen, doen dat het volgende:
                with open("virusshare_matches.txt", 'a') as e: # Open het 'virusshare_matches.txt'
                    e.write(l1)
            print(l1)

def main():
    compare_hashes()

if __name__ == '__main__':
    main()
