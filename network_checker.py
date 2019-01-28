"""
Author: Mariska Temming, S1106242
Summary: This script checks the network of the system, so it checks if the system has a connection to the internet
"""

from urllib.request import urlopen


# Checks if there is a connection to the internet
def internet_on():
    try:
        urlopen('http://www.google.com', timeout=1)  # Test the connection to Google.com
        return True
    except Exception as e:
        print(e)
        return False
