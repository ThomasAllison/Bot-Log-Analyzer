"""Analyze Bots.

Usage:
  analyze_bots.py directory <directory> [options] [<output>]
  analyze_bots.py file <file> [options] [<output>]
  analyze_bots.py (-h | --help)

Options:
  -h --help     Show this screen.
  -v --verbose  Be verbose.
  -o --output   Specify an output file.

"""
from docopt import docopt
from analyze import Analyze

if __name__ == '__main__':
    arguments = docopt(__doc__)
    analyze = Analyze(arguments['--verbose'], arguments['<output>'])

    if arguments['directory']:
        analyze.analyze_directory(arguments['<directory>'])
    elif arguments['file']:
        analyze.analyze_file(arguments['<file>'])
