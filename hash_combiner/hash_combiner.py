import glob
import time


def combiner():
    start_time = time.time()
    all_files = glob.glob('*.md5') # Ending with '.md5'

    # Opens the file "combines_hashes.txt".
    # If the file does not exist, creates a new file.

    counter = 0

    with open('virusshare_hashes.txt', 'w') as f_out:

        for file in all_files:
            counter += 1
            with open(file, 'r') as f_in:
                for line in f_in:

                    if not line.startswith('#'): # Ignores lines starting with "#"
                        f_out.write(line)

        # Writes some information to "info.txt"
        info = open('info.txt', 'w')
        info.write(f"Amount of hashfiles combined into virusshare_hashes.txt: {counter}")
        info.write(f"\n(VirusShare_00000.md5.txt - VirusShare_{counter-1:05}.md5.txt)")
        end_time = time.time()
        info.write("\nExecuted in: " + str(end_time - start_time) + " seconds.")
        info.close()


def main():
    combiner()


if __name__ == '__main__':
    main()

