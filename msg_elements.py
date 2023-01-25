from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from getpass import getpass

class Textual_msg:
    def __init__(self,text_of_msg, like_of_msg):
        self.text_of_msg = text_of_msg
        self.life_of_msg = like_of_msg

class Name_tag_msg:
    def __init__(self, name):
        self.name = name

class Media_msg:
    def __init__(self, like_of_msg):
        self.like_of_msg =like_of_msg

class Like_of_msg:
    def __init__(self, element):
        self.element = element