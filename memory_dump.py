import subprocess
import time

def start_memory_dump():
    subprocess.call(['C:\\Users\\Schellingerhoudt\\PycharmProjects\\ISCRIPT\\start_memory_dump.bat'])
    time.sleep(12)

def main():
    start_memory_dump()

if __name__ == '__main__':
    main()