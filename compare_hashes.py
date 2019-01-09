
Author:  Justin Moser, S1103774
Summary: - compare_hashes
                Compares all the virusshare hashes with the system hashes
                Writes the corresponding hashes to a file named "virusshare_matches.txt"
                The "virusshare_matches" file will be opened in hashing.py

"""

# Omschrijving van de functie staat in de summary
def compare_hashes():
    for line in open("system_hashes.txt"):
        if line in open("virusshare_hashes.txt"):
            print(line)
            with open("virusshare_matches.txt", "a") as e:
                e.write('{}\n'.format(line))

def main():
    compare_hashes()

if __name__ == '__main__':
    main()
