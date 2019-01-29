"""
Author:  Justin Moser, S1103774
Summary: - compare_hashes
                Compares all the virusshare hashes with the system hashes
                Writes the corresponding hashes to a file named "virusshare_matches.txt"
                The "virusshare_matches" file will be opened in hashing.py
"""

from database_helper import select_virusshare_hashes_by_system_hash


# Description of the function is in the summary
def compare_hashes():
    malware_found = False
    with open('system_hashes.txt', 'r') as hashes: # Opens 'system_hashes.txt'
        for system_hash in hashes: # Selects all hashes from the file
            system_hash = system_hash.strip()
            # Searches for corresponding hashes in the database
            hash_from_database = select_virusshare_hashes_by_system_hash(system_hash)
            if hash_from_database != '':
                print("Virusshare match: " + str(hash_from_database))
                with open('virusshare_matches.txt', 'a') as e: # Opens the 'virusshare_matches.txt'
                    malware_found = True
                    e.write('{}\n'.format(hash_from_database)) # Writes the corresponding hash to the file
    return malware_found
