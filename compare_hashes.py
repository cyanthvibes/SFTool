"""

Author:  Justin Moser, S1103774
Summary: - compare_hashes
                Compares all the virusshare hashes with the system hashes
                Writes the corresponding hashes to a file named "virusshare_matches.txt"
                The "virusshare_matches" file will be opened in hashing.py

"""

# Omschrijving van de functie staat in de summary
def compare_hashes():
    for line in open('virusshare_hashes.txt'): # Leest elke regel van het bestand
        if line in open("system_hashes.txt"): # Als er een hash overeenkomt, doe dan het volgende:
            print(line.strip('\n'))
            with open("virusshare_matches.txt", "a") as e:
                e.write('{}\n'.format(line))
    return line

  
def TEST_compare_hashes():

    with open('system_hashes.txt', 'r') as system_hashes: # Opent 'virusshare_hashes.txt' en 'system_hashes.txt"
        for system_hash in system_hashes:
            hash_from_database = select_virusshare_hashes_by_system_hash(system_hash)
            print(hash_from_database)
            with open('virusshare_matches.txt', 'a') as e: # Open het 'virusshare_matches.txt'
                e.write('{}\n'.format(hash_from_database)) # Schrijf de overeenkomende hash naar het bestand

                
def main():
    compare_hashes()

if __name__ == '__main__':
    main()
