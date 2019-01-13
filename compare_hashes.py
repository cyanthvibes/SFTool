"""
Author:  Justin Moser, S1103774
Summary: - compare_hashes
                Compares all the virusshare hashes with the system hashes
                Writes the corresponding hashes to a file named "virusshare_matches.txt"
                The "virusshare_matches" file will be opened in hashing.py
"""

from SFTool.database_helper import select_virusshare_hashes_by_system_hash

# Omschrijving van de functie staat in de summary
def compare_hashes():
    with open('system_hashes.txt', 'r') as hashes: # Opent 'system_hashes.txt'
        for system_hash in hashes:
            system_hash = system_hash.strip()
            hash_from_database = select_virusshare_hashes_by_system_hash(system_hash)
            print("Virusshare match: " + str(hash_from_database))
            with open('virusshare_matches.txt', 'a') as e: # Open het 'virusshare_matches.txt'
                e.write('{}\n'.format(hash_from_database)) # Schrijf de overeenkomende hash naar het bestand

def main():
    compare_hashes()

if __name__ == '__main__':
    main()
