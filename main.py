#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
from getpass import getpass
import os

USERNAME = "username"
PASSWORD = "password"

class WebDriver_User:

    def __init__(self, username = None, password = None, groupchat_id = None):
        self.username = username
        self.password = password
        self.groupchat_id = groupchat_id
        print("Setting Up Driver ...")
        self.driver = webdriver.Firefox()
        if (username == None or password == None or groupchat_id == None):
            print("Sorry eihter the password, username or groupchar_id are missing.\nTry Again")
    
    def fill_input_element(self, input_element, input_text):
        """
            Fills an input_element with text and presses return
            Input: input_element - a webdriver element, input text - str with the text you want to write
            Output: void        
        """
        input_element.clear()
        input_element.send_keys(input_text)
    
    def does_element_exist_xpath(self, element_xpath):
        try:
            self.driver.find_element(By.XPATH, element_xpath)
        except NoSuchElementException:
            return False
        return True

    def does_element_exist_class(self, element, class_name):
        try:
            element.find_element(By.CLASS_NAME, class_name)
        except NoSuchElementException:
            return False
        return True

    def does_element_exist_tag(self, element, tag):
        try:
            element.find_element(By.TAG_NAME, tag)
        except NoSuchElementException:
            return False
        return True

    def process_text_media_message(self, element, xpath_counter):
        """
        Returns a list of [text_msg, [likes]]
        """
        #figure out if text or media, see if an img or video exists with in the class
        #this works since the picture inside likes is stored inside a span
        base_xpath = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div["
        cut_out_pfp_xpath = "]/div[2]"
        text_xpath_adder = "]/div[2]/div/div/div[1]/div/div/div/div/div/div"
        emoji_xpath_adder = "]/div[2]/div/div/div/div/div/div/div/p/span"
        final_list = [] # [TEXT/MEDIA, [People Who Liked It]]
        base_xpath = base_xpath + str(xpath_counter)
        element = self.driver.find_element(By.XPATH, base_xpath + cut_out_pfp_xpath)
        if (self.does_element_exist_tag(element, "img") or self.does_element_exist_tag(element, "video") or self.does_element_exist_tag(element, "svg")):
            #it is media
            final_list.append("==media==")
        else:
            #it is text
            text_xpath = base_xpath + text_xpath_adder
            if(self.does_element_exist_xpath(text_xpath)):
                if(self.does_element_exist_xpath(base_xpath + emoji_xpath_adder)): #if its an emoji
                    text_xpath = base_xpath + emoji_xpath_adder
                if(self.does_element_exist_class(element, "Linkify")): #if its a link
                    link_xpath = "]/div[2]/div/div/div/div/div/div/div/div/span/a"
                    text_xpath = base_xpath + link_xpath
                text_content = self.driver.find_element(By.XPATH, text_xpath).get_attribute('textContent')
            final_list.append(text_content)
        
        #Get the LIKE!!!

        return final_list

    def __sign_in(self):
        """
        Input: None
        Output: web_data st[], has all the data in a big list
        """
        print("Signing in ... ")
        starting_url = "https://www.instagram.com/accounts/login/"
        inbox_url = "https://www.instagram.com/direct/inbox/"
        #sign in and go into inbox
        self.driver.get(starting_url)
        time.sleep(3)
        username_element = self.driver.find_element(By.NAME, USERNAME)
        password_element = self.driver.find_element(By.NAME, PASSWORD)
        self.fill_input_element(username_element, self.username)
        self.fill_input_element(password_element, self.password)
        password_element.send_keys(Keys.RETURN)
        time.sleep(4)
        self.driver.get(inbox_url)

    def __open_groupchat(self):
        inbox_url = "https://www.instagram.com/direct/t/"
        groupchat_url = inbox_url + self.groupchat_id

        self.driver.get(groupchat_url)
        time.sleep(3)
        notif_button_xpath = "/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"
        self.driver.find_element(By.XPATH, notif_button_xpath).click()

    def read_messages(self):
        msg_base_xpath = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div["
        name_tag_xpath = "/div/div"
        possible_date_tag_xpath = "/div[2]/div"
        text_media_class = "_acd3"
        all_text = []
        ctr = 1
        cur_xpath = msg_base_xpath + str(ctr) + ']'
        while(self.does_element_exist_xpath(cur_xpath)):
            cur_element = self.driver.find_element(By.XPATH, cur_xpath)
            cur_nametage_xpath = cur_xpath + name_tag_xpath
            cur_text = ''
            cur_personal_xpath = cur_xpath = "/div"
            if(self.does_element_exist_class(cur_element, text_media_class)):
                #media or text
                cur_text = self.process_text_media_message(cur_element, ctr)
            elif(self.does_element_exist_xpath(cur_nametage_xpath)):
                #is a name tage
                if(self.does_element_exist_xpath(cur_xpath + possible_date_tag_xpath)):
                    cur_nametage_xpath = cur_xpath + possible_date_tag_xpath
                cur_text = self.driver.find_element(By.XPATH, cur_nametage_xpath).get_attribute('textContent')
                cur_text = "__name__ : " + cur_text
            elif(not self.does_element_exist_xpath(cur_personal_xpath)):
                cur_text = "__name__ : Me"
            else:
                cur_text = "==Misc=="
            ctr += 1
            cur_xpath = msg_base_xpath + str(ctr) + ']'
            all_text.append(cur_text)
            print("Read ", str(ctr), " messages")
        return all_text
    
    def load_new_msgs(self, action, sleep_amt_milisec):
        time.sleep(sleep_amt_milisec * 0.01)
        action.key_down(Keys.CONTROL).key_down(Keys.UP).key_up(Keys.UP).key_up(Keys.CONTROL).perform()
    
    def start_the_scroll(self,action, starting_div):
        """
        Clicks on the svg element in the groupchat body so that we can start scrolling
        """
        msg_base_xpath = "/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div["
        svg_xpath = "/div[2]/div/div/div/button[1]"
        little_button_xpath = msg_base_xpath + str(starting_div) + ']' + svg_xpath
        if(self.does_element_exist_xpath(little_button_xpath)):
            button = self.driver.find_element(By.XPATH, msg_base_xpath + str(starting_div) + ']')
            action.move_to_element(button).perform()
            scroll_button = self.driver.find_element(By.XPATH, little_button_xpath)
            print("CLICKED")
            scroll_button.click()
            scroll_button.click()
        else:
            self.start_the_scroll(action, starting_div - 1)


    def collect_data(self):
        """

        """
        print("Data Collection Start ...")
        self.__sign_in()
        time.sleep(4)
        print("Opening Up Groupchat ...")
        self.__open_groupchat()
        
        print("Scrolling thru Chat ...")
        action = ActionChains(self.driver)
        self.start_the_scroll(action, 38)
        print("SCROLLING")
        sleep_milisec = 20
        amt_to_scroll = 500
        for i in range(0, amt_to_scroll):
            self.load_new_msgs(action, sleep_milisec)
            print("Scrolled ", str(i), " times")

        print("Reading Messages ...")
        msg_list = self.read_messages()

        self.driver.close()
        return msg_list

def main():
    print("STARTING")
    password = getpass()
    username = "ab__il"
    groupchat_id = "340282366841710300949128280204986662479" #Chill Night
    #groupchat_id = "340282366841710300949128151897195936895" #Ngan
    #groupchat_id = "340282366841710300949128533472207363990" #PONGERS

    screen = WebDriver_User(username, password, groupchat_id)
    chat_name = "pong_chat_log"
    chat_name = "chill_night_log"
    file_make_command = "touch " + chat_name 
    os.system(file_make_command)
    raw_data = screen.collect_data()
    with open(chat_name, "w") as myfile:
        myfile.write(chat_name + "LOG\n")


    with open(chat_name, "a") as myfile:
        for msg in raw_data:
            print(msg)
            myfile.write(str(msg) + "\n")
        
    return


if __name__ == "__main__":
    main()
