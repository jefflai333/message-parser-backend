import re, os, json, time, pathlib
import numpy as np
import matplotlib.pyplot as plt
import codecs
from functools import partial
from html.parser import HTMLParser
from html.entities import name2codepoint
from operator import itemgetter
from natsort import natsort_key, natsorted, ns
from datetime import datetime, date
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

def create_search_list(data_list, msg_to_search_for, start_date, end_date):
    search_list = []
    for data in data_list:
        del data[-1]
        search = []
        for message in data:
            msg = message[1]
            date_time = datetime.strptime(message[2], "%b %d, %Y, %I:%M %p")
            if msg_to_search_for.lower() in msg.lower() and date_time >= start_date and date_time <= end_date:
                search.insert(0, message)
        search_list.append([search])
    return search_list

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
                emoji_count += len(emoji_data)
                word_stats[person] = unique_words
                emoji_stats[person] = unique_emojis
                length_of_word_stats[person] = word_length_dict
                date_stats[person] = date_dict
                total_stats[person] = [count_per_person, word_count, char_count, emoji_count]
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
                emoji_count = len(emoji_data)
                word_stats[person] = unique_words
                emoji_stats[person] = unique_emojis
                length_of_word_stats[person] = word_length_dict
                date_stats[person] = date_dict
                total_stats[person] = [count_per_person, word_count, char_count, emoji_count]
        sort_stats(word_stats, 1, 20, True)
        sort_stats(emoji_stats, 1, 10, True)
        sort_stats(length_of_word_stats, 0, 99999999999, False)
        sort_stats(date_stats, 0, 99999999999, False)
        daily_stats = sort_time_stats(daily_stats)
        monthly_stats = sort_time_stats(monthly_stats)
        yearly_stats = sort_time_stats(yearly_stats)
        num_consecutive_days, start_date, end_date = consecutive_days_msged(daily_stats)
        consecutive_days = [num_consecutive_days, start_date, end_date]
        max_one_day_msg_count = max_one_day_msg(daily_stats)
        person_sent_most_msgs = sent_most_msgs_per_day(date_stats)
        general_stats = [msged_first, total_msg_count, title]
        stats.append([general_stats, total_stats, word_stats, emoji_stats, length_of_word_stats, date_stats, daily_stats, monthly_stats, yearly_stats, consecutive_days, people_who_msged_in_convo, max_one_day_msg_count, person_sent_most_msgs])
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

def max_one_day_msg(daily_stats):
    daily_stats = sorted(daily_stats, key=lambda x:x[1], reverse=True)
    return daily_stats[0]

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

def sent_most_msgs_per_day(date_stats):
    max_msgs_per_day = dict()
    max_person_count_per_day = dict()
    for name in date_stats:
        for dates in date_stats[name]:
            if dates[0] not in max_msgs_per_day:
                max_msgs_per_day[dates[0]] = [name, dates[1]]
            elif dates[1] > max_msgs_per_day[dates[0]][1]:
                max_msgs_per_day[dates[0]] = [name, dates[1]]
    for key, value in max_msgs_per_day.items():
        add_count_to_dict(value[0], max_person_count_per_day)
    list = max_person_count_per_day.items()
    list = sorted(list, key=lambda x:x[0])
    return list
    
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
        people_who_msged_in_convo = stats_list[i][10]
        max_one_day_msg_count = stats_list[i][11]
        person_sent_most_msgs = stats_list[i][12]
        stats = codecs.open(path_list[i] + "stats.txt", "w", "utf-8")
        stats.write("Chat with: " + title + "\n")
        stats.write("First ever message was sent by: " + first_msg + "\n")
        stats.write("Total messages sent: " + str(total_msg_count) + "\n")
        for name in total_stats:
            stats.write(name + ":\n")
            stats.write("Number of messages sent: " + str(total_stats[name][0]) + " accounting for " + "{0:.2f}".format(total_stats[name][0]/total_msg_count*100) + " percent of all messages\n")
            stats.write("Number of words sent: " + str(total_stats[name][1]) + "\n")
            stats.write("Number of characters sent: " + str(total_stats[name][2]) + "\n")
            stats.write("Number of emojis sent: " + str(total_stats[name][3]) + "\n")
            stats.write("Average message length: " + "{0:.2f}".format(total_stats[name][1]/total_stats[name][0]) + " words\n")
        stats.write("\nTop Words per person:\n")
        for name in word_stats:
            stats.write("\n" + name + ":\n")
            for words in word_stats[name]:
                stats.write("Word: " + words[0] + " appeared " + str(words[1]))
                if words[1] == 1:
                    stats.write(" time")
                else:
                    stats.write(" times")
                stats.write(", accounting for " + "{0:.2f}".format(words[1]/total_stats[name][1]*100) + " percent of all words\n")
        stats.write("\nTop Emojis per person:\n")
        for name in emoji_stats:
            stats.write(name + ":\n")
            for emojis in emoji_stats[name]:
                stats.write("Emoji: " + emojis[0] + " appeared " + str(emojis[1]))
                if emojis[1] == 1:
                    stats.write(" time")
                else:
                    stats.write(" times")
                stats.write(", accounting for " + "{0:.2f}".format(emojis[1]/total_stats[name][3]*100) + " percent of all emojis\n")
        stats.write("\nMessage Lengths:\n")
        for name in length_of_word_stats:
            stats.write(name + ":\n")
            for lengths in length_of_word_stats[name]:
                stats.write("Message word length of " + str(lengths[0]) + " appeared " + str(lengths[1]))
                if lengths[1] == 1:
                    stats.write(" time\n")
                else:
                    stats.write(" times\n")
        total_days_msged = sum(x[1] for x in person_sent_most_msgs)
        stats.write("\n")
        for person in person_sent_most_msgs:
            stats.write(person[0] + " sent the most messages in " + str(person[1]) + " days, accounting for " + "{0:.2f}".format(person[1]/total_days_msged*100) + " percent of all days\n")
        stats.write("\nMax Number Messages Sent in one day: " + str(max_one_day_msg_count[1]) + " on " + str(max_one_day_msg_count[0]) + "\n")
        stats.write("\nCombined Monthly Messages Sent:\n")
        for dates in monthly_stats:
            stats.write(str(dates[1]))
            if dates[1] == 1:
                stats.write(" message was ")
            else:
                stats.write(" messages were ")
            stats.write("sent in " + dates[0].strftime("%b %Y") + "\n")
        stats.write("\nCombined Yearly Messages Sent:\n")
        for dates in yearly_stats:
            stats.write(str(dates[1]))
            if dates[1] == 1:
                stats.write(" message was ")
            else:
                stats.write(" messages were ")
            stats.write("sent in " + str(dates[0].year) + "\n")
        stats.write("Max consecutive days msged is " + str(consecutive_days[0]) + "\n")
        stats.write("Achieved during the time frame " + str(consecutive_days[1]) + " to " + str(consecutive_days[2]) + "\n")
        stats.close()

def write_search_list(path_list, search_list, msg_to_search_for, start_date, end_date):
    for i in range(0, len(path_list)):
        search = search_list[i][0]
        write_search = codecs.open(path_list[i] + "search.txt", "w", "utf-8")
        match = ""
        if len(search) == 0:
            match = "No matches were "
        elif len(search) == 1:
            match = "1 match was "
        else:
            match = str(len(search)) + " matches were "
        write_search.write(match + "found for the word '" + msg_to_search_for + "' during the period " + str(start_date.date()) + " to " + str(end_date.date()) + "\n")
        for msgs_found in search:
            name = msgs_found[0]
            msg = msgs_found[1]
            time = msgs_found[2]
            write_search.write(name + " at " + str(time) + ": " + msg + "\n")
    write_search.close()

def main():
    rootdir = 'D:\\Facebook Data\\2020 April\\messages\\inbox\\JessicaZhang_Zs11Uy-bpw'
    #if you don't want to search for a msg, leave it as ""
    msg_to_search_for = ""
    #if you don't want a time range for the search function, leave start_date as datetime.min and end_date as datetime.max
    #if you do want a time range for the search function, change the time to datetime(year, month, day)
    start_date = datetime.min
    end_date = datetime.max
    print("Creating file list")
    file_list, path_list = create_file_list(rootdir)
    print("Parsing file list")
    parse_files(file_list)
    data_list = combine_parsed_list(file_list)
    print("Creating stats")
    stats_list = create_stats(data_list)
    print("Writing stats to files")
    write_stats(path_list, stats_list)
    if msg_to_search_for != "":
        print("Searching for keyword")
        search_list = create_search_list(data_list, msg_to_search_for, start_date, end_date)
        print("Writing search results to files")
        write_search_list(path_list, search_list, msg_to_search_for, start_date, end_date)
    if len(stats_list) > 1:
        total_stats_list = combined_stats_list(stats_list)
        write_total_stats(rootdir, total_stats_list)
    
def plot_graph():
    count_per_person_dm = {}
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