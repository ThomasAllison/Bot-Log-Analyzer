import ast
from collections import Counter

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

# Open log file in 'read' mode
with open(log_file_dir, "r") as in_file:
    # Loop over each log line
    for string_line in in_file:
        line = ast.literal_eval(string_line)
        do_something_with_line(line)
        total_lines += 1

print("==============>", count_bots, "bots")
print("==============>", total_lines, "total")
print("==============>", str((count_bots/total_lines) * 100.0) + "%", "is bot")

print_bot_list()

