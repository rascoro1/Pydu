#!/usr/bin/python3

"""
Estimate File Space Usage with Python using Pydu.py in Command line


"""
from Pydu import Pydu

import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sort', action='store_true',
                    help='Will sort files and print files, largest closest to user displat.')

parser.add_argument('-sr', '--sort-reverse', action='store_true',
                    help='Will reverse sort files and print files, smallest closest to user display.')

parser.add_argument("dir", type=str,
                    help='The directory/file you would like to check the size of.')

parser.add_argument('-f', '--find', type=str,
                  help='Find files based on name')

parser.add_argument('-c', '--case-insensitive', action='store_true',
                    help='Only needed with the --find, case-sensitive')

parser.add_argument('-d', '--display', type=str, choices=['B', 'K', 'M', 'G', 'H', 'b', 'k', 'm', 'g', 'h'],
                    help='Size of files display, default is B')


parser.add_argument('-t', '--time', action='store_true',
                    help='Find time files were last modified and created',
                    )

parser.add_argument('-V', '--version', action='store_true',
                    help='Display Version Number')

args = parser.parse_args()


if __name__ == "__main__":
    print (args)
    pathdir = Pydu(args.dir)

    if args.sort and args.sort_reverse:
        print ("Cannot sort both reverse and normal.")
        sys.exit(1)

    if args.version:
        pathdir.version()
        sys.exit(0)

    if args.time:
        pathdir.set_time()

    if args.sort:
        pathdir.sort(direction='asc')
    elif args.sort_reverse:
        pathdir.sort(direction='desc')

    if args.find:
        if args.case_insensitive: # Case insensitive
            pathdir.find(path=args.find,where='any', type=args.display.upper(), case_sensitive=False)
        else: # Case sensitive
            pathdir.find(path=args.find, where='any', type=args.display.upper(), case_sensitive=True)
    else:
        if args.display is None:
            pathdir.all(type='B')
        else:
            pathdir.all(type=args.display.upper())
    sys.exit(0)




