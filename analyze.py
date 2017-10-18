import ast
from collections import Counter
import sys
import os
import re

# log_file_dir = "/home/thomas/Documents/Dev/logs/hnaccesslogs/access.log.1"
filters = ["bot", "magereport", "facebook", "crawler", "slurp", "tws", "spider", "scan"]

count_bots = 0
total_lines = 0

bot_list = []
legit_list = []


def count_bot():
    global count_bots
    count_bots += 1


def add_bot_to_list(useragent):
    global bot_list
    bot_list.append(useragent)


def print_bot_list(list):
    freq_list = Counter(list).most_common()

    print("{:<8} {:<15}".format("Freq", "Useragent"))
    for useragent, freq in freq_list:
        print("{:<8} {:<15}".format(freq, useragent))


def write_bot_list(file, list, title="List", minimum=0):
    file.write("\n====================  {}  =================\n\n".format(title))

    freq_list = Counter(list).most_common()

    file.write("{:<8} {:<15}\n".format("Freq", "Useragent"))
    for useragent, freq in freq_list:
        if freq > minimum:
            file.write("{:<8} {:<15}\n".format(freq, useragent))

def write_stats(file):
    file.write("\n====================  {}  =================\n\n".format("Stats"))

    percentage = (float(count_bots) / float(total_lines)) * 100.00
    one_string = str(count_bots) + " bots\n" + str(total_lines) + " total\n" + str(percentage) + "%" + " is bot\n"
    file.write(one_string)


def do_something_with_line(line):
    if is_bot(line):
        useragent_contains_bot(line)
    else:
        legit_list.append(line["user_agent"])


def is_bot(line):
    useragent = line["user_agent"]
    urls_in_useragent = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', useragent)
    email_in_useragent = re.findall('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', useragent)

    if any(n in useragent.lower() for n in filters):
        return True
    elif useragent is "-":
        return True
    elif useragent is "":
        return True
    elif urls_in_useragent:
        return True
    if email_in_useragent:
        return True


def useragent_contains_bot(line):
    add_bot_to_list(line["user_agent"])
    count_bot()


def read_from_dir(directory):
    count = 0
    total = len(os.listdir(directory))
    for filename in os.listdir(directory):
        path_to_file = directory + filename

        if os.path.isdir(path_to_file):
            one_string = "\nStart reading files from {}".format(path_to_file)
            print(one_string)
            read_from_dir(path_to_file + "/")

        else:
            read_from_file(path_to_file)

            count += 1
            one_string = "Done reading with {} of {} ".format(count, total) + path_to_file
            print(one_string)


def walk_dir(directory):
    for root, dirs, files in os.walk(directory):
        one_string = "\nStart reading files from {}".format(root)
        print(one_string)

        count = 0
        total = len(files)
        for file in files:
            path_to_file = os.path.join(root, file)
            read_from_file(path_to_file)

            count += 1
            one_string = "- Done reading with {0:0>2} of {1:0>2} ".format(count, total) + path_to_file
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
        walk_dir(arg)
    elif os.path.isfile(arg):
        read_from_file(arg)
        print("Done reading single file "+arg)


# ============ PRINT STATS =============

print("")
percentage = (float(count_bots)/float(total_lines)) * 100.00
one_string = str(count_bots) + " bots\n" + str(total_lines) + " total\n" + str(percentage)+"%" + " is bot\n"
print(one_string)

print_bot_list(bot_list)
# print("\n====================================================================\n")
# print_bot_list(legit_list)


# ============ WRITE STATS =============
f = open("loganalysis.txt", "w+")
write_stats(f)
write_bot_list(f, bot_list, title="Bot List")
write_bot_list(f, legit_list, title="Legit List", minimum=10)


