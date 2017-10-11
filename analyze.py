import ast
from collections import Counter

import sys

import os

log_file_dir = "/home/thomas/Documents/Dev/logs/hnaccesslogs/access.log.1"

count_bots = 0
bot_list = []
total_lines = 0


def count_bot():
    global count_bots
    count_bots += 1


def add_bot_to_list(useragent):
    global bot_list
    bot_list.append(useragent)


def print_bot_list():
    global bot_list
    freq_dict = dict(Counter(bot_list))

    print("{:<8} {:<15}".format("Freq", "Useragent"))
    for useragent, freq in freq_dict.items():
        print("{:<8} {:<15}".format(freq, useragent))


def do_something_with_line(line):
    if "bot" in line["user_agent"]:
        add_bot_to_list(line["user_agent"])
        count_bot()


def read_from_dir(directory):
    count = 0
    total = len(os.listdir(directory))
    for filename in os.listdir(directory):
        path_to_file = directory + filename
        read_from_file(path_to_file)

        count += 1
        one_string = "Done reading with {} of {} ".format(count, total) + path_to_file
        print(one_string)


def read_from_file(file):
    # Open log file in 'read' mode
    with open(file, "r") as in_file:
        global total_lines
        # Loop over each log line
        for string_line in in_file:
            line = ast.literal_eval(string_line)
            do_something_with_line(line)
            total_lines += 1



# ============ START SCRIPT =============

for arg in sys.argv[1:]:
    if os.path.isdir(arg):
        read_from_dir(arg)
    elif os.path.isfile(arg):
        read_from_file(arg)




# ============ PRINT STATS =============

print("")
percentage = (float(count_bots)/float(total_lines)) * 100.00
one_string = str(count_bots) + " bots\n" + str(total_lines) + " total\n" + str(percentage)+"%" + " is bot\n"
print(one_string)

print_bot_list()

