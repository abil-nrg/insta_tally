#!/usr/bin/env python3
import fileinput
import sys
import re

def read_word_list():
    file = open(str(sys.argv[2]), "r")
    file_word_list = file.readlines()
    word_list = []
    for word in file_word_list:
        word_list.append(word.strip('\n'))
    file.close()
    return word_list

def read_chat_log(words_of_interest):
    file = open(str(sys.argv[1]), "r")
    file_word_list = file.readlines()
    chat_log = []

    msg_regex = (r"^\['(.*)']$")
    nametag_regex= (r"^__name__ : ([^\d:\d]*)$")

    msg_regex_obj = re.compile(msg_regex)
    nametag_regex_obj = re.compile(nametag_regex)
    prev_name = ""
    for word in file_word_list:
        word = word.strip('\n')
        # __name__
        # ['']
        msg = re.match(msg_regex, word, re.IGNORECASE)
        name_tag = re.match(nametag_regex, word, re.IGNORECASE)
        if(msg != None):
            #msg   
            msg_text = msg.group(1)
            msg_list = [prev_name, msg_text]
            chat_log.append(msg_list)
        elif(name_tag != None):
            if(name_tag.group(1) != 'November' and name_tag != 'Yesterday'):
                name_tag_text = name_tag.group(1)
                prev_name = name_tag_text
            elif(name_tag.group(1) == ''):
                prev_name = "Me"
    return chat_log

def main():
    word_list= read_word_list()
    print(word_list)
    chat_log = read_chat_log(word_list)
    for chat in chat_log:
        print(chat)
if __name__ == "__main__":
    if (len(sys.argv) == 3):
        main()
    else:
        print("Usage : ", str(sys.argv[0]), " <chat_log> <word_list(optional)>")
