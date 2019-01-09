def compare_hashes():
    # with open('virusshare_hashes.txt', 'r') as f1, open('system_hashes.txt', 'r') as f2: # Opent 'virusshare_hashes.txt' en 'system_hashes.txt"
    #     for line in f2:
    #         if line in f1:
    #             with open('virusshare_matches.txt', 'a') as e: # Open het 'virusshare_matches.txt'
    #                 e.write('{}\n'.format(line)) # Schrijf de overeenkomende hash naar het bestand
    # return line

    file1 = set(line.strip() for line in open('virusshare_hashes.txt'))
    file2 = set(line.strip() for line in open('system_hashes.txt'))


    for line in file1 & file2:

        if line:
            matches = open('virusshare_matches.txt', 'a')
            matches.write('{}\n'.format(line))
            matches.close()

def main():
    compare_hashes()

if __name__ == '__main__':
    main()
