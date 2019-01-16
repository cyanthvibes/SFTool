import subprocess
import time

def start_memory_dump():
    p = subprocess.Popen(['MagnetRAMCapture.exe'])
    p.wait()


def main():
    start_memory_dump()

if __name__ == '__main__':
    main()