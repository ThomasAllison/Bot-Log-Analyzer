import random
import string

good_useragents = []
bad_useragents = []

def read_from_file(file):
    lines = []
    # Open log file in 'read' mode
    with open(file, "r") as in_file:
        # Loop over each log line
        for string_line in in_file:
            lines.append(string_line)

    return lines


def get_useragents():
    global good_useragents
    global bad_useragents

    good_useragents = read_from_file("/home/thomas/Documents/Dev/Bot-Log-Analyzer/minchar/gooduseragents.txt")
    bad_useragents = read_from_file("/home/thomas/Documents/Dev/Bot-Log-Analyzer/minchar/baduseragents.txt")


def count_hits_in_list(value, list):
    counter = 0

    for entry in list:
        if value.lower() in entry.lower():
            counter += 1

    return counter

# start script
get_useragents()

# ======== try your self ========
while True:
    part_of_useragent = input("Part of useragent:")
    print("Hits for legit useragents:", count_hits_in_list(part_of_useragent, good_useragents), "/", len(good_useragents))
    print("Hits for bad useragents:  ", count_hits_in_list(part_of_useragent, bad_useragents), "/", len(bad_useragents))
    print("\n")


# =========== get stats ==========
# def get_random_string(amount_of_characters):
#     c = 'abcdefghijklmnopqrstuvwxyz'
#     random_string = ""
#
#     for i in range(amount_of_characters):
#         random_string += random.choice(c)
#
#     return random_string
#
#
# def test_ranges():
#     for i in range(8):
#         total_good = 0
#         total_bad = 0
#         rep = 100
#         for j in range(rep):
#             total_good += count_hits_in_list(get_random_string(i+1), good_useragents)
#             total_bad += count_hits_in_list(get_random_string(i+1), bad_useragents)
#
#         print("{} characters averaged {:<12} good hits and {:<12} bad hits".format(i+1, total_good/rep, total_bad/rep))

# test_ranges()