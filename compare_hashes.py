"""

Author:  Justin Moser, S1103774
Summary: - compare_hashes
                Compares all the virusshare hashes with the system hashes
                Writes the corresponding hashes to a file named "virusshare_matches.txt"
                The "virusshare_matches" file will be opened in hashing.py

"""

# Omschrijving van de functie staat in de summary
def compare_hashes():
    with open('virusshare_hashes.txt', 'r') as f1, open('system_hashes.txt', 'r') as f2: # Opent 'virusshare_hashes.txt' en 'system_hashes.txt"
        for line in f2:
            if line in f1:
                with open('virusshare_matches.txt', 'a') as e: # Open het 'virusshare_matches.txt'
                    e.write('{}\n'.format(line)) # Schrijf de overeenkomende hash naar het bestand
    return line

def main():
    compare_hashes()

if __name__ == '__main__':
    main()
