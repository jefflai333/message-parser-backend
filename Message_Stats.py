import re, os, json, time, pathlib
import numpy as np
import matplotlib.pyplot as plt
import codecs
from functools import partial
from html.parser import HTMLParser
from html.entities import name2codepoint
from operator import itemgetter
from natsort import natsort_key, natsorted, ns
from datetime import datetime
import emoji

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        #initialize variables in addition to the base class
        self.name_data = []
        self.text_data = []
        self.date_data = []
        self.data = []
        self.data_inserted = True
        self.flag = ''
        self.title = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.flag = 'title'
        if tag == 'img' and attrs[0][1].startswith('messages'):
            #if there are multiple images in the same message, it will enter this if statement
            #it will append the two images into one message instead of having two seperate messages
            if self.data_inserted == True:
                self.text_data[-1] = self.text_data[-1] + ' ' + attrs[0][1]
            else:
                self.text_data.append(attrs[0][1])
            self.data_inserted = True
            self.flag = ''
        for attr in attrs:
            #checks for the attributes in the html and sets the flag accordingly
            if attr[1] == '_3-96 _2let': 
                self.flag = 'text'
                self.data_inserted = False
            elif attr[1] == '_3-96 _2pio _2lek _2lel':
                self.flag = 'name'
            elif attr[1] == '_3-94 _2lem':
                self.flag = 'date'
                #edge case where message has been removed, if data still hasn't been inserted at this point,
                #that means that the messsage has been removed.
                if self.data_inserted == False:
                    self.text_data.append('Message has been removed')

    def handle_data(self, data):
        if self.flag == 'title':
            self.title = data
        elif self.flag == 'text' and self.data_inserted == False:
            self.text_data.append(data)
            self.data_inserted = True
        elif self.flag == 'name':
            self.name_data.append(data)
        #data != 'Quiet' is to check if you have been removed from the group
        elif self.flag == 'date' and data != 'Quiet':
            self.date_data.append(data)
        self.flag = ''

    def combine_data(self, filepath):
        #checks to see that the length of each set of data is the same so that it can be combined into one array
        if len(self.name_data) == len(self.text_data) and len(self.text_data) == len(self.date_data):
            for i in range(0, len(self.name_data)):
                self.data.append([self.name_data[i], self.text_data[i], self.date_data[i]])
            self.data.append(self.title)
        else:
            print('Error Verifying Data', filepath)

def messages_per_person(data):
    count_per_person = dict()
    for person in data:
        if person in count_per_person:
            count_per_person[person] += 1
        else:
            count_per_person[person] = 1
    return count_per_person

def add_count_to_dict(key, dict):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1

def create_stats(data_list):
    stats = []
    for data in data_list:
        title = data[-1]
        del data[-1]
        if 'Say hi' in data[-1][1]:
            if len(data) == 1:
                msged_first = "Nobody"
            else:
                msged_first = data[-2][0]
        else:
            msged_first = data[-1][0]
        total_stats = dict()
        word_stats = dict()
        length_of_word_stats = dict()
        emoji_stats = dict()
        date_stats = dict()
        daily_stats = dict()
        monthly_stats = dict()
        yearly_stats = dict()
        people_who_msged_in_convo = set()
        total_msg_count = 0
        for message in data:
            person = message[0]
            people_who_msged_in_convo.add(person)
            msg = message[1]
            date_time = datetime.strptime(message[2], "%b %d, %Y, %I:%M %p")
            date = date_time.date()
            add_count_to_dict(date, daily_stats)
            date = date.replace(day=1)
            add_count_to_dict(date, monthly_stats)
            date = date.replace(month=1)
            add_count_to_dict(date, yearly_stats)
            date = date_time.date()
            total_msg_count += 1
            if person in total_stats:
                split_msg = msg.split()
                length_of_msg = len(split_msg)
                unique_words = word_stats[person]
                unique_emojis = emoji_stats[person]
                word_length_dict = length_of_word_stats[person]
                date_dict = date_stats[person]
                count_per_person = total_stats[person][0]
                word_count = total_stats[person][1]
                char_count = total_stats[person][2]
                #count unique words
                for word in split_msg:
                    add_count_to_dict(word.lower(), unique_words)
                #count unique emojis
                emoji_data = emoji.emoji_lis(msg)
                for i in range(0, len(emoji_data)):
                    emoji_key = emoji_data[i]['emoji']
                    add_count_to_dict(emoji_key, unique_emojis)
                #count different lengths of msgs
                add_count_to_dict(length_of_msg, word_length_dict)
                #count different days of msgs sent
                add_count_to_dict(date, date_dict)
                count_per_person += 1
                word_count += length_of_msg
                char_count += len(msg)
                word_stats[person] = unique_words
                emoji_stats[person] = unique_emojis
                length_of_word_stats[person] = word_length_dict
                date_stats[person] = date_dict
                total_stats[person] = [count_per_person, word_count, char_count]
            else:
                split_msg = msg.split()
                length_of_msg = len(split_msg)
                unique_words = dict()
                unique_emojis = dict()
                word_length_dict = dict()
                date_dict = dict()
                #count unique words
                for word in split_msg:
                    add_count_to_dict(word.lower(), unique_words)
                #count unique emojis
                emoji_data = emoji.emoji_lis(msg)
                for i in range(0, len(emoji_data)):
                    emoji_key = emoji_data[i]['emoji']
                    add_count_to_dict(emoji_key, unique_emojis)
                #count different lengths of msgs
                word_length_dict[length_of_msg] = 1
                date_dict[date] = 1
                count_per_person = 1
                word_count = length_of_msg
                char_count = len(msg) if 'messages/inbox/' not in msg else 1
                word_stats[person] = unique_words
                emoji_stats[person] = unique_emojis
                length_of_word_stats[person] = word_length_dict
                date_stats[person] = date_dict
                total_stats[person] = [count_per_person, word_count, char_count]
        sort_stats(word_stats, 1, 20, True)
        sort_stats(emoji_stats, 1, 10, True)
        sort_stats(length_of_word_stats, 0, 99999999999, False)
        sort_stats(date_stats, 0, 99999999999, False)
        daily_stats = sort_time_stats(daily_stats)
        monthly_stats = sort_time_stats(monthly_stats)
        yearly_stats = sort_time_stats(yearly_stats)
        num_consecutive_days, start_date, end_date = consecutive_days_msged(daily_stats)
        consecutive_days = [num_consecutive_days, start_date, end_date]
        general_stats = [msged_first, total_msg_count, title]
        stats.append([general_stats, total_stats, word_stats, emoji_stats, length_of_word_stats, date_stats, daily_stats, monthly_stats, yearly_stats, consecutive_days, people_who_msged_in_convo])
    return stats

def sort_stats(stats, element_to_sort, num_elements_to_sort, reverse_sort_order):
    for person in stats:
        list = stats[person].items()
        list = sorted(list, key=lambda x:x[element_to_sort], reverse=reverse_sort_order)
        if len(list) > num_elements_to_sort:
            list = list[0:num_elements_to_sort]
        stats[person] = list

def sort_time_stats(stats):
    list = stats.items()
    list = sorted(list, key=lambda x:x[0])
    return list

def consecutive_days_msged(daily_stats):
    start_date = daily_stats[0][0]
    end_date = daily_stats[0][0]
    if len(daily_stats) == 1:
        return 1, start_date, end_date
    max_consecutive_days_msged = -1
    consecutive_days_msged = 1
    curr_start_date = daily_stats[0][0]
    curr_end_date = daily_stats[0][0]
    for i in range(0, len(daily_stats)-1):
        if daily_stats[i+1][0].toordinal() - daily_stats[i][0].toordinal() == 1:
            consecutive_days_msged += 1
            curr_end_date = daily_stats[i+1][0]
        else:
            consecutive_days_msged = 1
            curr_start_date = daily_stats[i+1][0]
        if consecutive_days_msged > max_consecutive_days_msged:
            max_consecutive_days_msged = consecutive_days_msged
            start_date = curr_start_date
            end_date = curr_end_date
    return max_consecutive_days_msged, start_date, end_date

def date_stats(date_stats):
    return 0
    
def create_file_list(rootdir):
    rootdir = rootdir
    file_list = []
    path_list = []
    prevFilepath = ''
    #iterates through all the file paths and appends any html files into array
    for subdir, dirs, files in os.walk(rootdir):
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(".html"):
                #checks to see if the html is from the same person (i.e prevFilepath is the same)
                #adds it into the same array if so
                if subdir + os.sep == prevFilepath:
                    file_list[-1].append(filepath)
                #otherwise, it will append the html into a new array
                else:
                    path_list.append(subdir + os.sep)
                    file_list.append([filepath])
                prevFilepath = subdir + os.sep
    #does a natural sort for messages with more than 10 html files
    #eg messages_1.html, messages_10.html, messages_2.html will sort into
    #messages_1.html, messages_2.html, messages_10.html
    for i in range(0, len(file_list)):
        if len(file_list[i]) > 9:
            file_list[i] = sorted(file_list[i], key=lambda x: list(natsort_key(s) for s in pathlib.Path(x).parts))
    return file_list, path_list

def parse_files(file_list):
    for i in range(0, len(file_list)):
        for j in range(0, len(file_list[i])):
            filepath = file_list[i][j]
            with open(filepath, 'r', encoding='utf-8') as utf_8_data:
                data = utf_8_data.read()
            file_list[i][j] = parse_html(data, filepath)
        print("Parsing File " + str(i+1) + " out of " + str(len(file_list)) + "\n")

def parse_html(data, filepath):
    parser = MyHTMLParser()
    parser.feed(data)
    parser.combine_data(filepath)
    print(parser.data[-1])
    return parser.data

def combine_parsed_list(parsed_list):
    data_list = []
    for people in parsed_list:
        arr = []
        title = ''
        for messages in people:
            title = messages[-1]
            del messages[-1]
            for sublist in messages:
                arr.append(sublist)
        arr.append(title)
        data_list.append(arr)
    return data_list

def combined_stats_list(stats_list):
    person_count = dict()
    for i in range(0, len(stats_list)):
        people_who_msged_in_convo = stats_list[i][10]
        for person in people_who_msged_in_convo:
            if person in person_count:
                person_count[person] += 1
            else:
                person_count[person] = 1
        #stats_list[i] = sorted(stats_list[i], key=lambda x:x[0][1], reverse=True)
    person_count_list = list(person_count.items())
    person_count_list = sorted(person_count_list, key=lambda x:x[1], reverse=True)
    user_of_msgs = person_count_list[0][0]
    first_msg_count = [0,0,0]
    first_msg_count_group = [0,0,0]
    sent_per_person = []
    sent_per_group = []
    received_per_person = []
    received_per_group = []
    total_msg_per_chat = []
    total_msg_per_group_chat  = []
    for i in range(0, len(stats_list)):
        first_msg = stats_list[i][0][0]
        total_msg_count = stats_list[i][0][1]
        title = stats_list[i][0][2]
        total_stats = stats_list[i][1]
        word_stats = stats_list[i][2]
        emoji_stats = stats_list[i][3]
        length_of_word_stats = stats_list[i][4]
        date_stats = stats_list[i][5]
        daily_stats = stats_list[i][6]
        monthly_stats = stats_list[i][7]
        yearly_stats = stats_list[i][8]
        consecutive_days = stats_list[i][9]
        people_who_msged_in_convo = stats_list[i][10]
        #check to see if it is a direct message
        if user_of_msgs in people_who_msged_in_convo and len(people_who_msged_in_convo) == 2 or len(people_who_msged_in_convo) == 1:
            if first_msg != "Nobody":
                total_msg_per_chat.append([title, total_msg_count])
                if user_of_msgs in total_stats:
                    sent_per_person.append([title, total_stats[user_of_msgs][0]])
                    received_per_person.append([title, total_msg_count-total_stats[user_of_msgs][0]])
            count_first_msg(first_msg, user_of_msgs, first_msg_count)
        else:
            if first_msg != "Nobody":
                total_msg_per_group_chat.append([title, total_msg_count])
                if user_of_msgs in total_stats:
                    sent_per_group.append([title, total_stats[user_of_msgs][0]])
                    received_per_group.append([title, total_msg_count-total_stats[user_of_msgs][0]])
            count_first_msg(first_msg, user_of_msgs, first_msg_count_group)
    user_of_msgs_sent_total = sum(x[1] for x in sent_per_person)
    user_of_msgs_receive_total = sum(x[1] for x in received_per_person)
    user_of_msgs_group_sent_total = sum(x[1] for x in sent_per_group)
    user_of_msgs_group_receive_total = sum(x[1] for x in received_per_group)
    sent_per_person = sort_combined_stats(sent_per_person, 10)
    sent_per_group = sort_combined_stats(sent_per_group, 10)
    received_per_person = sort_combined_stats(received_per_person, 10)
    received_per_group = sort_combined_stats(received_per_group, 10)
    user_of_msgs_count_arr = [user_of_msgs_sent_total, user_of_msgs_receive_total]
    user_of_msgs_count_group_arr = [user_of_msgs_group_sent_total, user_of_msgs_group_receive_total]
    total_msg_per_chat = sort_combined_stats(total_msg_per_chat, 10)
    total_msg_per_group_chat = sort_combined_stats(total_msg_per_group_chat, 10)
    return [first_msg_count, first_msg_count_group, user_of_msgs_count_arr, user_of_msgs_count_group_arr, total_msg_per_chat, total_msg_per_group_chat, sent_per_person, received_per_person, sent_per_group, received_per_group]

def sort_combined_stats(list, top_num):
    list = sorted(list, key=lambda x:x[1], reverse=True)
    if len(list) > top_num:
        list = list[0:top_num]
    return list

def write_total_stats(rootdir, total_stats_list):
    stats = codecs.open(rootdir + "stats.txt", "w", "utf-8")
    first_msg_count = total_stats_list[0]
    first_msg_count_group = total_stats_list[1]
    user_of_msgs_count_arr = total_stats_list[2]
    user_of_msgs_count_group_arr = total_stats_list[3]
    total_msg_per_chat = total_stats_list[4]
    total_msg_per_group_chat = total_stats_list[5]
    sent_per_person = total_stats_list[6]
    received_per_person = total_stats_list[7]
    sent_per_group = total_stats_list[8]
    received_per_group = total_stats_list[9]
    stats.write("Out of the " + str(sum(first_msg_count)) + " direct messages, you started " + str(first_msg_count[0]) + " of them, ")
    stats.write("or " + str(first_msg_count[0]/sum(first_msg_count)*100) + " percent\n")
    stats.write("They started " + str(first_msg_count[1]) + " of them, ")
    stats.write("or " + str(first_msg_count[1]/sum(first_msg_count)*100) + " percent\n")
    stats.write("You haven't messaged " + str(first_msg_count[2]) + " of them, ")
    stats.write("or " + str(first_msg_count[2]/sum(first_msg_count)*100) + " percent\n")
    stats.write("Out of the " + str(sum(first_msg_count_group)) + " group messages, you started " + str(first_msg_count_group[0]) + " of them, ")
    stats.write("or " + str(first_msg_count_group[0]/sum(first_msg_count_group)*100) + " percent\n")
    stats.write("Someone else started " + str(first_msg_count_group[1]) + " of them, ")
    stats.write("or " + str(first_msg_count_group[1]/sum(first_msg_count_group)*100) + " percent\n")
    stats.write("You haven't messaged in " + str(first_msg_count_group[2]) + " of them, ")
    stats.write("or " + str(first_msg_count_group[2]/sum(first_msg_count_group)*100) + " percent\n")
    stats.write("You have a total of " + str(user_of_msgs_count_arr[0]+user_of_msgs_count_arr[1]) + " direct messages\n")
    stats.write("Out of those messages, you have sent a total of " + str(user_of_msgs_count_arr[0]) + " direct messages, ")
    stats.write("or " + str(user_of_msgs_count_arr[0]/(user_of_msgs_count_arr[0]+user_of_msgs_count_arr[1])*100) + " percent\n")
    stats.write("You have received a total of " + str(user_of_msgs_count_arr[1]) + " direct messages, ")
    stats.write("or " + str(user_of_msgs_count_arr[1]/(user_of_msgs_count_arr[0]+user_of_msgs_count_arr[1])*100) + " percent\n\n")
    stats.write("Lifetime messages sent: " + str(user_of_msgs_count_arr[0] + user_of_msgs_count_group_arr[0]) + "\n")
    stats.write("Lifetime messages received: " + str(user_of_msgs_count_arr[1] + user_of_msgs_count_group_arr[1]) + "\n")
    stats.write("Lifetime direct messages sent: " + str(user_of_msgs_count_arr[0]) + "\n")
    stats.write("Lifetime direct messages received: " + str(user_of_msgs_count_arr[1]) + "\n")
    stats.write("Lifetime group messages sent: " + str(user_of_msgs_count_group_arr[0]) + "\n")
    stats.write("Lifetime group messages received: " + str(user_of_msgs_count_group_arr[1]) + "\n\n")
    stats.write("The people you have the most messages with:\n")
    for stat in total_msg_per_chat:
        stats.write(stat[0] + ": " + str(stat[1]) + " total messages\n")
    stats.write("\nThe people you sent the most messages to:\n")
    for stat in sent_per_person:
        stats.write(stat[0] + ": " + str(stat[1]) + " total messages\n")
    stats.write("\nThe people you received the most messages from:\n")
    for stat in received_per_person:
        stats.write(stat[0] + ": " + str(stat[1]) + " total messages\n")
    stats.write("\nThe group chats you have the most messages with:\n")
    for stat in total_msg_per_group_chat:
        stats.write(stat[0] + ": " + str(stat[1]) + " total messages\n")
    stats.write("\nThe group chats you sent the most messages to:\n")
    for stat in sent_per_group:
        stats.write(stat[0] + ": " + str(stat[1]) + " total messages\n")
    stats.write("\nThe group chats you received the most messages from:\n")
    for stat in received_per_group:
        stats.write(stat[0] + ": " + str(stat[1]) + " total messages\n")

def count_first_msg(first_msg, user_of_msgs, first_msg_count):
    if first_msg == user_of_msgs:
        first_msg_count[0] += 1
    elif first_msg == "Nobody":
        first_msg_count[2] += 1
    else:
        first_msg_count[1] += 1

def count_per_person_list_count(count_per_person, user_of_msgs):
    user_of_msgs_count_total = count_per_person[user_of_msgs]
    count_per_person.pop(user_of_msgs)
    count_per_person_list = count_per_person.items()
    count_per_person_list = sorted(count_per_person_list, key=lambda x:x[1], reverse=True)
    user_of_msgs_receive_total = sum(x[1] for x in count_per_person_list)
    if len(count_per_person_list) > 20:
        count_per_person_list = count_per_person_list[0:20]
    return user_of_msgs_count_total, user_of_msgs_receive_total, count_per_person_list

def write_stats(path_list, stats_list):
    for i in range(0, len(path_list)):
        first_msg = stats_list[i][0][0]
        total_msg_count = stats_list[i][0][1]
        title = stats_list[i][0][2]
        total_stats = stats_list[i][1]
        word_stats = stats_list[i][2]
        emoji_stats = stats_list[i][3]
        length_of_word_stats = stats_list[i][4]
        date_stats = stats_list[i][5]
        daily_stats = stats_list[i][6]
        monthly_stats = stats_list[i][7]
        yearly_stats = stats_list[i][8]
        consecutive_days = stats_list[i][9]
        stats = codecs.open(path_list[i] + "stats.txt", "w", "utf-8")
        stats.write("Chat with: " + title + "\n")
        stats.write("First ever message was sent by: " + first_msg + "\n")
        stats.write("Total messages sent: " + str(total_msg_count) + "\n")
        for name in total_stats:
            stats.write(name + ":\n")
            stats.write("Number of messages sent: " + str(total_stats[name][0]) + " accounting for " + str(total_stats[name][0]/total_msg_count*100) + " percent of all messages\n")
            stats.write("Number of words sent: " + str(total_stats[name][1]) + "\n")
            stats.write("Number of characters sent: " + str(total_stats[name][2]) + "\n")
            stats.write("Average message length: " + str(total_stats[name][1]/total_stats[name][0]) + " words\n")
        stats.write("\nTop Words per person:\n")
        for name in word_stats:
            stats.write(":\n" + name + ":\n")
            for words in word_stats[name]:
                stats.write("Word: " + words[0] + " appeared " + str(words[1]))
                if words[1] == 1:
                    stats.write(" time")
                else:
                    stats.write(" times")
                stats.write(", accounting for " + str(words[1]/total_stats[name][1]*100) + " percent of all words\n")
        stats.write("\nTop Emojis per person:\n")
        for name in emoji_stats:
            stats.write(name + ":\n")
            for emojis in emoji_stats[name]:
                stats.write("Emoji: " + emojis[0] + " appeared " + str(emojis[1]))
                if emojis[1] == 1:
                    stats.write(" time")
                else:
                    stats.write(" times")
                stats.write(", accounting for " + str(emojis[1]/total_stats[name][1]*100) + " percent of all emojis\n")
        stats.write("\nMessage Lengths:\n")
        for name in length_of_word_stats:
            stats.write(name + ":\n")
            for lengths in length_of_word_stats[name]:
                stats.write("Message word length of " + str(lengths[0]) + " appeared " + str(lengths[1]))
                if lengths[1] == 1:
                    stats.write(" time\n")
                else:
                    stats.write(" times\n")
        # stats.write("\nDaily Messages Sent:\n")
        # for name in date_stats:
            # stats.write(name + ":\n")
            # for dates in date_stats[name]:
                # stats.write(str(dates[1]))
                # if dates[1] == 1:
                    # stats.write(" message ")
                # else:
                    # stats.write(" messages ")
                # stats.write("were sent on " + str(dates[0]) + "\n")
        # stats.write("\nCombined Daily Messages Sent:\n")
        # for dates in daily_stats:
            # stats.write(str(dates[1]))
            # if dates[1] == 1:
                # stats.write(" message ")
            # else:
                # stats.write(" messages ")
            # stats.write("were sent on " + str(dates[0]) + "\n")
        stats.write("\nCombined Monthly Messages Sent:\n")
        for dates in monthly_stats:
            stats.write(str(dates[1]))
            if dates[1] == 1:
                stats.write(" message ")
            else:
                stats.write(" messages ")
            stats.write("were sent in " + dates[0].strftime("%b %Y") + "\n")
        stats.write("\nCombined Yearly Messages Sent:\n")
        for dates in yearly_stats:
            stats.write(str(dates[1]))
            if dates[1] == 1:
                stats.write(" message ")
            else:
                stats.write(" messages ")
            stats.write("were sent in " + str(dates[0].year) + "\n")
        stats.write("Max consecutive days msged is " + str(consecutive_days[0]) + "\n")
        stats.write("Achieved during the time frame " + str(consecutive_days[1]) + " to " + str(consecutive_days[2]) + "\n")
        stats.close()
    
def main():
    rootdir = 'D:\\Facebook Data\\2020 April\\messages\\inbox\\'
    print("Creating file list")
    file_list, path_list = create_file_list(rootdir)
    print("Parsing file list")
    parse_files(file_list)
    data_list = combine_parsed_list(file_list)
    print("Creating stats")
    stats_list = create_stats(data_list)
    print("Writing stats to files")
    write_stats(path_list, stats_list)
    total_stats_list = combined_stats_list(stats_list)
    write_total_stats(rootdir, total_stats_list)
    
def plot_graph():
    count_per_person_dm = {'Jeff Lai': 432683, 'Aaron Hum': 85, 'Aaron Tan': 341, 'Abdullah Khan': 34, 'Abhinav Chanda': 8, 'Adrian Carpenter': 178, 'Agathe Merceron': 142, 'Ahmed Abdulkadir': 125, 'Aidan Lui': 3, 'Aidan Tsang': 1, 'Akshaya Venkatesh': 200, 'Alan Chen': 1, 'Alexander Woo': 497, 'Alex Barkin': 59, 'Alexei Tsybulsky': 3, 'Alexis Chen': 188, 'Alex Wang': 2461, 'Aliana Versi': 10, 'Alice Liuu': 9, 'Alice Peng': 180, 'Alice Zhou': 8, 'Alicia Ng': 17, 'Ali Isnotonfire': 9, 'Aloïse Delizy': 29, 'Amal Yusuf': 19, 'Amaris He': 200, 'Amio Rahman': 181, 'Amy Liu': 1977, 'Amy Luo': 914, 'Andrée Tsoungui': 208, 'Andrew Daly': 9, 'Andy Rei Kou': 34, 'Nicholas Kwong': 118, 'Angela Yu': 14, 'Angel Cai': 3358, 'Anita Ning': 58, 'Anna Wang': 3782, 'Anne-Charlotte Plessy': 1, 'Anne Marie Klein': 4, 'Anson Wong': 153, 'Anthony Chang': 18, 'Anushka Birla': 27, 'Arjun Bhushan': 12, 'Arooj Asrar': 1, 'Arqum Latif': 2, 'Ashiqa Boo': 14, 'Astrid Popescu': 235, 'Austin Jiang': 4, 'Austin Kranc': 3, 'Avi Fischer': 4, 'Aviv PB': 43, 'Baptiste Simon': 6, 'Ben Iain Morehead': 59, 'Benjamin Duo': 739, 'Benjamin Griffith': 3, 'Ben Zhang': 458, 'Bernard Lucas': 37, 'Bilawal Nisar': 3, 'Billy Li': 1, 'Bilun Sun': 245, 'Bob Bao': 1, 'Brandon Hum': 10, 'Brendan Arciszewski': 23, 'Brendan Johnston': 2, 'Brendan Zhang': 5, 'Brian Yeung': 51, 'Brooke Ellis': 221, 'Bruce Kuwahara': 11, 'Bryant Ng': 167, 'Caitlin Annan': 6, 'Jessica Zhang': 32773, 'Caleb Tseng-Tham': 2665, 'Callum Moffat': 92, 'Camille Chiron': 129, 'Camille Tsang': 8708, 'Candy Liu': 1, 'Cara de Belle': 1, 'Carla Da Costa': 7, 'Caroline Bld': 5, 'Carrie Chen': 386, 'Cathy Li': 1282, 'Charles Hunter': 20, 'Charles Yu': 19, 'Cherie Chan': 29, 'Chris Ji': 218, 'Chris Thi': 91, 'Christian Wai-Forssell': 2, 'Christie Ma': 13, 'Christina Lim': 8, 'Christina Lin': 151, 'Christopher Sheedy': 61, 'Christopher Song': 152, 'Chuqian Susan Li': 6, 'Cindy DoubleveeYou': 1254, 'Cindy Wei': 2, 'Cody Zhang': 18, 'Daniela Garcia Orellana': 8, 'Daniel Ding': 46, 'Daniel Goldstein': 3, 'Daniel Ku': 4, 'Daniell Yang': 3, 'Daniel Tran': 104, 'Dan Nguyen': 1, 'Darian Ho': 9, 'Gene Liang': 1915, 'David Li': 48, 'Dennis Deng': 1, 'Dorian Cailleau': 1, 'Dove Bhuiyan': 17, 'Duncan Bennie': 66, 'Elbert Lai': 1483, 'Elena Andreev': 27, 'Elina Ma': 7052, 'Elin Liu': 27725, 'Emilien Tison': 77, 'Emily Yu': 125, 'Emma Bazantay': 3, 'Emma Kawczy': 240, 'Emon Sen Majumder': 8, 'Erica Gun': 4, 'Eric Wang': 2, 'Erika Cao': 142, 'Erika Narimatsu': 54163, 'Erin Leung': 131, 'Eugene Wang': 38, 'Eva-Marie Turpin': 27, 'Evan Kim': 72, 'Eva Retailleau-Morille': 15, 'Evelyn Vo': 121, 'EverWing': 281, 'Facebook User': 602, 'Faisal Khan': 4, 'Farhan Khan': 21, 'Felicia Jiang': 4557, 'Felix Sung': 309, 'Felix Wong': 121, 'Fouzia Shoily Ahsan': 37, 'Francois Barnard': 3, 'Frank Christian Wang': 3, 'Gabriel Kwan': 2, 'Ganashsai Vannithamby': 2, 'Gary Ye': 19, 'Gauvain Guern': 4, 'Geetha Jeyapragasan': 571, 'Gillian Giovannetti': 111, 'Girik Sur': 1, 'Glen Gong': 6, "Grace 'Graceface' Xu": 23, 'Hannah Rosenberg': 24, 'Haseeb Akram': 1, 'Hasib Ahmed': 1, 'Helen Lin': 729, 'Hillary Chan': 533, 'Hohyun Ryu': 4, 'Houston Tsui': 126, 'Hussain Shah': 46, 'Ignatius Sinn': 404, 'Igor Jovanović': 845, 'Irene Chen': 446, 'Irene Situ': 11, 'Iris Zou': 6, 'Isaac Chang': 558, 'Isabela Hernandes': 25, 'Isabel Hu': 703, 'Isabelle Li': 6, 'Issac Mathew': 44, 'Jack Cygness': 121, 'Jack Dai': 4, 'Jackie Du': 38, 'Jack Ruan': 98, 'Jacky Ho': 3, 'Jacob Kelly': 6, 'Jaehyung Park': 18, 'Jae Woo Jun': 15, 'Jake Muchynski': 18, 'Jameson Weng': 9, 'Jamie Dang': 11, 'Jamie Tang': 238, 'Jason  Jiang': 3, 'Jason Maximillian Elsted': 41, 'Jason Zhao': 49, 'Jawad Noor': 1, 'Chris Xi': 3, 'Rahim Baird': 2, 'Derek Yates': 3, 'Jeff Ma': 9, 'Jennie Xu': 131, 'Jennifer Anderson': 18, 'Jennifer Xie': 20, 'Jenny Huynh': 1944, 'Jenny Ly': 641, 'Jesse Becerra': 11, 'Jessica Kwong': 11071, 'Jessy de Leeuw': 8227, 'Jingchun Jackie Wang': 9, 'Jin Liang': 629, 'Joanna Tang': 2, 'Joey Hung': 3, 'Joey Kuang': 274, 'John Albert': 2, 'John Huang': 29, 'John Pan': 10, 'Jonah Ho': 3, 'Jonah William Kim': 15, 'Jonathan Chang': 154, 'Jordan Fung': 134, 'Joseph Huang': 7, 'Josephine Chan': 7, 'Josh Liu': 27, 'Joshua Sukhra': 56, 'Julia Garbe': 70, 'Julia Gorbet': 199, 'Julie Bondu': 226, 'Justin Lai': 738, 'Justin Li': 99, 'Justin Lu': 41, 'Amber Tsetsos': 1, 'Kai Ostermann': 96, 'Kaitlyn Tse': 573, 'Keith Lai': 680, 'Kelly Chu': 30, 'Kelvin Vuu': 429, 'Kenneth Tjie': 1, 'Ken Ny': 5243, 'Kevin An': 1, 'Kevin LeeZh': 22, 'Kevin Lu': 19, 'Kevin Mathew Mukalel': 53, 'Kevin Wang': 5, 'King Chan': 34, 'Kingsley Chu': 673, 'Kin Ping Ng': 4, 'Kishan Rampersad': 23, 'Kyle Cox': 116, 'Kyle Robinson': 5, 'Langni Zeng': 901, 'Lan Jing Li': 3, 'Lanny Han': 429, 'Larry Li': 83, 'Laura Dang': 197, 'Laura Wong': 19804, 'Leah Xu': 18, 'LeAnn Chan': 20, 'Léa Richard': 39, 'Lee Nguyen': 1, 'Leighton Shum': 90, 'Leo Liu': 13, 'Leon Ang': 128, 'Leon Lam': 89, 'Leon Lin': 188, 'Leo Tao': 17, 'Leroy Zhao': 29, 'Lester Lim': 9, 'Gabbynot Mendoza': 1, 'Lily Chow': 1, 'Lily Liu': 4, 'Lily Yang': 69, 'Linda Lin': 77, 'Linda Mao': 8, 'Lins Hoang': 23, 'Lisa Tang': 2300, 'Lisa Yu': 133, 'Louisa Chan': 10739, 'Louise Monk': 508, 'Lucas Btrd': 2, 'Lucie Mallet': 2, 'Lucille Huang': 18, 'Lucy Liu': 2, 'Luke Ning': 12, 'Luna Yyx': 26, 'Mabel Kwok': 8, 'Mackenzie Annis': 5572, 'Mackenzie Chau': 384, 'Maher Absar': 14, 'Mahir Khan': 181, 'Maisha Sha Sharyar': 10, 'Mako Sorensen': 21, 'Malcolm A. Nichols': 2, 'Mali Zhang': 7, 'Manon Breteaudeau': 2, 'Manuel Lok': 21, 'Margaret Lin': 3, 'Maria Zhang': 155, 'Marie Gallard': 11, 'Marielle Jolene Peñamora Loro': 52, 'Marija Cvetkovik': 8, 'Marine Besnard': 13, 'Mark Kao': 2, 'Marley Liu': 21, 'Martin Boissinot': 32, 'Marylou Gouin': 201, 'Mathilde Galichet': 13, 'Mathis Coutant': 1, 'Mathys Imari': 19, 'Matthew Barclay': 61, 'Matthew Ho': 28, 'Matthew Reynolds': 1, 'Max Chang': 19, 'Max Rand': 65, 'Melody Li': 6073, 'Melvin Wang': 12517, 'Michael McLean': 12, 'Michelle Liu': 31, 'Michelle Mei': 166, 'Mitchell Hoyt': 14, 'Muhaimin Choudhury': 5, 'Muhammad Ali': 13, 'Muhammad Subhan Altaf': 2, 'Murray Bai': 64, 'Namjun Kim': 10, 'Neien Wei': 20, 'Newton Paul': 19, 'Nick Yuhe Wang': 3, 'Nico Duke': 851, 'Niel Mistry': 49, 'Nikhil Melgiri': 2, 'Olivia Tom': 1114, 'Olivia Yung': 79, 'Parth Shah': 37, 'Patrick Liu': 121, 'Pat Young': 16, 'Peilin Wang': 9, 'Phillip Wu': 4, 'Phoebe Zhou': 415, 'Preet Sangha': 2, 'Prithvi Verghese': 5, 'Purva Amin': 2, 'Rachel Yang': 8, 'Rachel Yuan': 5, 'Rafeed Choudhury': 30874, 'Raymond DiCecco': 7, 'Regina GU': 22, 'Remeny Elsa': 2067, 'Remya Philips': 578, 'Richard Sun': 30, 'Ricky Yuen': 17, 'Rolina Wu': 9, 'Ronathan Ip': 7856, 'Ron Li': 22, 'Rosalee Hui': 30, 'Roy Chen': 16, 'Rui Li': 362, 'Rupert Wu': 63, 'Rushil Nagarsheth': 3, 'Rushnan Anusha': 115, 'Ryu Lien': 74, 'Saad Chowdhury': 264, 'Sajid Ajmal': 20, 'Saksham Aggarwal': 6, 'Sakura Shane Bruno': 53, 'Sammi Wong': 396, 'Sam Noguchi': 7, 'Samuel Cho': 1, 'Saraf Azad': 97, 'Sarah Bahreinian': 11, 'Saumya Gupta': 654, 'Seb Dg': 5, 'Serena Ong': 11, 'Shamanth Hampali': 4, 'Shangbing Jiang': 215, 'Shao Curtis Li': 13, 'Shashwat Deolal': 33, 'Shiblul Hasan': 45, 'Sifad Chowdhury': 1, 'Simon Tison': 206, 'Sivasan Sivagunalan': 2, 'Siyi Yan': 8570, 'Skylar Liang': 8, 'Smith John': 10, 'Sophie Jiang': 13, 'Stephanie Sarker': 6, 'Stephen Li': 91, 'Steven Ha': 4194, 'Steven Cheung': 32, 'Steven Feng': 510, 'Swapnil Patel': 326, 'Tam Tran': 1, 'Tashfia Hussain': 1, 'Taylor PL': 31, 'Teddy Frank': 45, 'Tiffany Sum': 2, 'Tiger Zhao': 3, 'Tina Wu': 2335, 'Tina Zhao': 3, 'Tingyun Zuo': 1322, 'Tommy Tang': 45, 'Tou Noomor': 6, 'Tracy Ngan': 20, 'Tristan Le': 6, 'Tyler Jacob': 3, 'Tyler Zhang': 88, 'Vanessa Kam': 396, 'Vevina Trinh': 104, 'Vicky Hou': 25, 'Victor Pham-Ho': 3, 'Vincent Lai': 914, 'Vincent Tan': 15, 'Vivek Philips': 74, 'Vivek Agarwal': 6, 'Vivian Chau': 67, 'Walter Raftus': 38, 'Waterloo Engineering Society': 2, 'Wendy Deng': 58, 'William Tang': 8, 'Will Mui': 14, 'Xiluo Emily Zhang': 104, 'Ya Lim': 10, 'Yanyan Law': 6, 'Yeva Yu': 21, 'Yilena Xu': 13, 'Yu Carl': 962, 'Zackary Tsang': 1769, 'Zak Hu': 11, 'Zhaoyang Yu': 10, 'Zheng He': 1112, 'Zhiyong Wang': 3, 'ZiCheng Huang': 45, 'Zoë Sherar': 6}
    count_per_person_dm_list = list(count_per_person_dm.items())
    for x in count_per_person_dm_list:
        x = list(x)
        x[1] = int(x[1])
    count_per_person_dm_list = sorted(count_per_person_dm_list, key=lambda msg: msg[1], reverse=True)
    names = list()
    num_msgs = []
    for x in range(1, 10):
        names.append(count_per_person_dm_list[x][0])
        num_msgs.append(count_per_person_dm_list[x][1])
    y_pos = np.arange(len(names))
    plt.bar(y_pos, num_msgs, align='center', alpha=0.5)
    plt.xticks(y_pos, names)
    plt.ylabel('Number of Msgs')
    plt.title('Most Frequent People Msged')

    plt.show()

if __name__ == "__main__":
    main()
    #plot_graph()