import os
import re
import sys
from collections import Counter
from memory_profiler import profile

log_file_dir = "/home/thomas/Documents/Dev/logs/lesslogs/one"
filters = ["bot", "magereport", "facebook", "crawler", "slurp", "tws", "spider", "scan"]
filters_string = ' '.join(filters)

bot_list = []
legit_list = []


def add_bot_to_list(useragent):
    global bot_list
    bot_list.append(useragent)


def print_bot_list(list):
    print("{:<8} {:<15}".format("Freq", "Useragent"))
    for useragent, freq in list:
        print("{:<8} {:<15}".format(freq, useragent))


def write_bot_list(file, list, title="List", minimum=0):
    file.write("\n====================  {}  =================\n\n".format(title))

    file.write("{:<8} {:<15}\n".format("Freq", "Useragent"))
    for useragent, freq in list:
        if freq > minimum:
            file.write("{:<8} {:<15}\n".format(freq, useragent))


def get_amount_of_bots():
    total = 0

    for useragent, freq in all_bots:
        total += freq

    return total


def write_stats(file):
    file.write("\n====================  {}  =================\n\n".format("Stats"))

    amount_bots = get_amount_of_bots()
    amount_total = len(all_ua_list)

    percentage = (float(amount_bots) / float(amount_total)) * 100.00
    one_string = str(amount_bots) + " bots\n" + str(amount_total) + " total\n" + str(percentage) + "%" + " is bot\n"
    file.write(one_string)


email_re = re.compile('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
useragent_re = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


def is_bot(line):
    if line in filters_string:
        return True
    elif line is "-":
        return True
    elif line is "":
        return True

    has_email = email_re.search(line)
    if has_email:
        return True

    return useragent_re.search(line)

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

fp = open('memory_profiler_basic_mean.log', 'w+')
@profile(precision=5, stream=fp)
def read_from_file(file):
    global all_ua_list
    # Open log file in 'read' mode
    with open(file, "r") as in_file:
        # Loop over each log line
        lines = in_file.readlines()
        for line in lines:
            useragent = find_text_between_strings(line, '"user_agent":"', '",')

            all_ua_list.append(useragent)


def find_text_between_strings(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def check_for_bots(all_ua_list):
    freq_list = Counter(all_ua_list).most_common()

    global all_bots
    global legit_list

    for useragent in freq_list:
        if is_bot(useragent[0]):
            all_bots.append(useragent)
        else:
            all_legit.append(useragent)


# ============ START SCRIPT =============

all_ua_list = []
all_bots = []
all_legit = []

for arg in sys.argv[1:]:
    if os.path.isdir(arg):
        walk_dir(arg)
    elif os.path.isfile(arg):
        read_from_file(arg)
        print("Done reading single file " + arg)

check_for_bots(all_ua_list)

# ============ PRINT STATS =============

# print_bot_list(all_bots)
# print_bot_list(all_legit)

# ============ WRITE STATS =============

f = open("loganalysis.txt", "w+")
write_stats(f)
write_bot_list(f, all_bots, title="Bot List", minimum=500)
write_bot_list(f, all_legit, title="Legit List", minimum=1000)
