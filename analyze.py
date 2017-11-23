import logging
import os

import re

from bot_counter import BotCounter


class Analyze:
    verbose = False
    logger = None
    output_file = None
    email_re = re.compile('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
    useragent_re = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    filters = ["bot", "magereport", "facebook", "crawler", "slurp", "tws", "spider", "scan"]
    filters_string = ' '.join(filters)
    all_useragents = BotCounter()
    all_bots = []
    all_legit = []

    def __init__(self, verbose, output_file):
        self.output_file = output_file
        self.verbose = verbose

        logging.basicConfig(level=logging.INFO, format='%(asctime)-15s: %(message)s')
        self.logger = logging.getLogger(__name__)

    def analyze_file(self, file):
        self.read_from_file(file)
        self.check_for_bots(self.all_useragents.get_sorted_list_by_frequency())
        self.done()

    def analyze_directory(self, directory):
        self.walk_directory(directory)
        self.check_for_bots(self.all_useragents.get_sorted_list_by_frequency())
        self.done()

    def walk_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            self.logger.info("Start reading files from {}".format(root))

            count = 0
            total = len(files)
            for file in files:
                path_to_file = os.path.join(root, file)
                self.read_from_file(path_to_file)

                if self.verbose:
                    count += 1
                    self.logger.info("- Done reading with {0:0>2} of {1:0>2} ".format(count, total) + path_to_file)

    def read_from_file(self, file):
        with open(file, "r") as in_file:
            lines = in_file.readlines()
            for line in lines:
                useragent = self.find_text_between_strings(line, '"user_agent":"', '",')

                self.all_useragents.add(useragent)

    def find_text_between_strings(self, s, first, last):
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""

    # checking useragent strings to identify bots
    def check_for_bots(self, all_useragents):

        for useragent in all_useragents:
            if self.is_bot(useragent[0]):
                self.all_bots.append(useragent)
            else:
                self.all_legit.append(useragent)

    def is_bot(self, line):
        if line in self.filters_string:
            return True
        elif line is "-":
            return True
        elif line is "":
            return True

        if self.email_re.search(line):
            return True

        return self.useragent_re.search(line)

    def print_bot_list(self, bots):
        self.logger.info("\t{:<8} {:<15}".format("Freq", "Useragent"))

        if len(bots) > 10 and not self.verbose:
            bots = bots[:10]
        elif len(bots) > 10 and self.verbose:
            bots = bots[:50]

        for useragent, freq in bots:
            self.logger.info("\t{:<8} {:<15}".format(freq, useragent))

    def print_stats(self):
        amount_bots = self.get_amount_of_bots()
        amount_total = self.all_useragents.get_total_amount_of_requests()

        percentage = (float(amount_bots) / float(amount_total)) * 100.00
        self.logger.info("Total {} request".format(amount_total))
        self.logger.info("Bots {}".format(amount_bots))
        self.logger.info("{}% is bot".format(percentage))

    def get_amount_of_bots(self):
        total = 0
        for useragent, freq in self.all_bots:
            total += freq

        return total

    def write_stats(self, file):
        amount_bots = self.get_amount_of_bots()
        amount_total = self.all_useragents.get_total_amount_of_requests()

        percentage = (float(amount_bots) / float(amount_total)) * 100.00
        one_string = str(amount_bots) + " bots\n" + str(amount_total) + " total\n" + str(percentage) + "%" + " is bot\n"
        file.write(one_string)

    def write_bot_list(self, file, list, minimum=0):
        file.write("{:<8} {:<15}\n".format("Freq", "Useragent"))
        for useragent, freq in list:
            if freq > minimum:
                file.write("{:<8} {:<15}\n".format(freq, useragent))

    def done(self):
        if self.output_file:
            f = open(self.output_file, "w+")
            self.write_stats(f)
            self.write_bot_list(f, self.all_bots)
            self.logger.info("Done writing.")
        else:
            print()
            self.print_stats()
            print()
            self.print_bot_list(self.all_bots)
            print()

        self.logger.info("Done with analysis.")
        print()
