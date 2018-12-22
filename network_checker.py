from urllib.request import urlopen


# internet_on(): Mariska Temming s1106242
# check if there is an internet connection
def internet_on():
    try:
        urlopen('http://216.58.192.142', timeout=1)  # test network connection Google.com
        return True
    except Exception as e:
        print(e)
        return False


def main():
    print(internet_on())


if __name__ == '__main__':
    main()
