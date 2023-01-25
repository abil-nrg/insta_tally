#!/usr/bin/env python3
from bs4 import BeautifulSoup as BS
import requests
import time
from getpass import getpass
import os


def main():
    instagram = requests.get("https://www.instagram.com/direct/t/340282366841710300949128280204986662479")
    print(instagram.json)
    return

if __name__ == "__main__":
    main()