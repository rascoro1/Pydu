#!/usr/bin/python3

"""
Estimate File Space Usage with Python


"""
import os
import sys

# To get the time in nice format
import time

# Sorting the Sizes
from operator import itemgetter

VERSION = 0.1

class Pydu(object):
    """
    Class represents files/directories, size, time created/modified of a directory
    """

    def __init__(self, dir, autoinit=True, file_time=False):

        # Checking if given directory is valid
        if os.path.isdir(dir) or os.path.isfile(dir):
            self.dir = dir
        else:
            print ("Error #1: Directory", dir, "does no Exist.")
            sys.exit(1)

        # Initializing Variables
        self.files = []
        self.dirs = []
        self.total_size = ""
        self.file_time = file_time

        # Get File/Directory Size and Total Size
        if autoinit:
            self.set_files_dirs()
            self.set_total_size()
            if file_time:
                self.set_time()

    def set_files_dirs(self):
        """
        Set self.files and self.dirs to  aList of Dictionaries = {'path', 'size'}
        """

        for (root, dirs, files) in os.walk(self.dir, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                try:
                    size = os.path.getsize(path)
                except OSError:
                    continue
                file_info = {'path': path, 'size': size}
                self.files.append(file_info)
            for name in dirs:
                path = os.path.join(root, name)
                try:
                    size = os.path.getsize(path)
                except OSError:
                    continue
                dir_info = {'path': path, 'size': size}
                self.dirs.append(dir_info)

    def set_files(self):
        """
        Set self.files to a List of Dictionaries = {'path', 'size'}
        """
        for root, dirs, files in os.walk(self.dir, topdown=False):
            for name in files:
                path = os.path.join(root, name)
                try:
                    size = os.path.getsize(path)
                except OSError:
                    continue
                file_info = {'path': path, 'size': size}
                self.files.append(file_info)

    def set_dirs(self):
        """
        Set self.dirs to a List of Dictionaries = {'path', 'size'}
        """
        for root, dirs, files in os.walk(self.dir, topdown=False):
            for name in dirs:
                path = os.path.join(root, name)
                try:
                    size = os.path.getsize(path)
                except OSError:
                    continue
                dir_info = {'path': path, 'size': size}
                self.dirs.append(dir_info)

    def set_total_size(self):
        """
        Get total size in Bytes using self.files and self.dirs
        IMPORTANT: set_files() and set_dirs() must be executed before set_total_size()
        """
        total_size = 0
        for file in self.files:
            total_size += file['size']
        for dir in self.dirs:
            total_size += dir['size']

        self.total_size = total_size

    def round_size(self, size, type):
        """
        Round Size Based on 'size type'

        Args:
            - size: size to evaluate (int)
            - type: data displayed in (char: 'B', 'K', 'M', 'G' or 'H')

        Returns:
            - rounded size with corresponding type ([int, char])
        """

        types = [('B', 1, -1), ('K', 1024, 0), ('M', 1048576, 1), ('G', 1073741824, 2)]
        if type == 'B' or type == 'K' or type == 'M' or type == 'G':
            for key, multiplier, n_round in types:
                if type == key:
                    size = size / multiplier
                    size = round(size, n_round)
                    if str(size).endswith(".0"):
                        size = format(size, '.0f')
                    return [size, type]
        elif type == 'H':
            """Human Readable Type"""
            type = self.human_readable(size)
            for key, multiplier, n_round in types:
                if type == key:
                    size = size / multiplier
                    size = round(size, n_round)
                    if str(size).endswith(".0"):
                        size = format(size, '.0f')
                    return [size, type]
        else:
            print ("Error #2 Type:", type, "is not a Valid Type. Valid Types are B,K,M,G,H")
            sys.exit(2)

    def all(self, type='B'):
        """
        Print all Files and Directories

        Args:
            - type: data displayed in (char: 'B', 'K', 'M', 'G' or 'H')
        """

        type = type.upper()

        for dir in self.dirs:
            temp_type = type # reassagin type to 'H' after mutation
            size, type = self.round_size(dir['size'], type)

            if self.file_time:
                print ('%-0s%-5s%-125s%-40s%-12s' % (str(size), type, dir['path'], str(dir['modified']), str(dir['created'])))
            else:
                print ('%-0s%-5s%-125s' % (str(size), type, dir['path']))
            type = temp_type

        # Print Files

        for file in self.files:
            temp_type = type  # reassagin type to 'H' after mutation
            size, type = self.round_size(file['size'], type)

            if self.file_time:
                print ('%-0s%-5s%-125s%-40s%-12s' % (str(size), type, file['path'], str(file['modified']), str(file['created'])))
            else:
                print ('%-0s%-5s%-125s' % (str(size), type, file['path']))
            type = temp_type

        # Print Total
        size, type = self.round_size(self.total_size, type)
        print("Total of ", self.dir + ":", str(size) + type)

    def total(self, type='B'):
        """
        Display Total of files and directories only

        Args:
            - type: data displayed in (char: 'B', 'K', 'M', 'G' or 'H')

        """

        type = type.upper()
        print ("Total:", str(self.round_size(self.total_size, type)) + type)

    def human_readable(self, size):
        """
        return size appropriate for human readable format (e.g., B K M G)

        Args:
            - size: size to evaluate (int)

        Returns:
            - Human Readable type (char: 'B', 'K', 'M', 'G' or 'H')
        """

        type = 'B'

        if size >= 1073741824:
            """GigaBytes"""
            type = 'G'
        elif size >= 1048576:
            """Megebytes"""
            type = 'M'
        elif size >= 1024:
            """Kilobyte"""
            type = 'K'
        return type


    def sort(self, direction='asc'):
        """
        Will sort self.files and self.dirs on file size

        Args:
            - direction: which way to display sorting (char: 'asc', 'desc')

        """

        if direction == 'asc':
            self.files = sorted(self.files, key=itemgetter('size'))
            self.dirs = sorted(self.dirs, key=itemgetter('size'))
        elif direction == 'desc':
            self.files = sorted(self.files, key=itemgetter('size'), reverse=True)
            self.dirs = sorted(self.dirs, key=itemgetter('size'), reverse=True)

    def set_time(self):
        """
        Will set self.files and self.dirs dictionaries to display when the file was last modified/created
        """
        i = 0
        for f in self.files:
            created = time.ctime(os.path.getmtime(f['path']))
            modified = time.ctime(os.path.getctime(f['path']))
            self.files[i]['created'] = created
            self.files[i]['modified'] = modified
            i += 1

        i = 0
        for d in self.dirs:
            created = time.ctime(os.path.getmtime(d['path']))
            modified = time.ctime(os.path.getctime(d['path']))
            self.dirs[i]['created'] = created
            self.dirs[i]['modified'] = modified
            i += 1
        self.file_time = True

    def help(self):
        """Display this help and exit"""

    def version(self):
        """output version information and exit"""
        print ("Pydu by Andrew Copeland")
        print (str(VERSION) + "v")

    def find(self, path, where='any', type='B', case_sensitive = True):
        """
        Print directory/file that starts with, ends with or contains path Default is 'any'

        Args:
            - path: name of path you are looking for (String)
            - where: where in the directory/file (String: 'any', 'end', 'start')
            - type: data displayed in (char: 'B', 'K', 'M', 'G' or 'H')
            - case_sensitive: search case sensitive (Boolean)
        """
        if where == 'any':
            for f in self.files:
                if case_sensitive:
                    if path in f['path']:
                        if self.file_time:
                            size = self.round_size(size=f['size'], type=type)
                            print ('%-0s%-5s%-100s%-40s%-12s' % (
                            str(size[0]), size[1], f['path'], str(f['modified']), str(f['created'])))
                        else:
                            size = self.round_size(size=f['size'], type=type)
                            print (str(size[0]) + size[1] + '\t' + f['path'])
                else:
                    if path.upper() in f['path'].upper():
                        if self.file_time:
                            size = self.round_size(size=f['size'], type=type)
                            print ('%-0s%-5s%-100s%-40s%-12s' % (
                            str(size[0]), size[1], f['path'], str(f['modified']), str(f['created'])))
                        else:
                            size = self.round_size(size=f['size'], type=type)
                            print (str(size[0]) + size[1] + '\t' + f['path'])
            for d in self.dirs:
                if case_sensitive:
                    if path in f['path']:
                        if self.file_time:
                            size = self.round_size(size=d['size'], type=type)
                            print ('%-0s%-5s%-100s%-40s%-12s' % (
                            str(size[0]), size[1], d['path'], str(d['modified']), str(d['created'])))
                        else:
                            size = self.round_size(size=d['size'], type=type)
                            print (str(size[0]) + size[1] + '\t' + d['path'])
                else:
                    if path.upper() in f['path'].upper():
                        if self.file_time:
                            size = self.round_size(size=d['size'], type=type)
                            print ('%-0s%-5s%-100s%-40s%-12s' % (
                            str(size[0]), size[1], d['path'], str(d['modified']), str(d['created'])))
                        else:
                            size = self.round_size(size=d['size'], type=type)
                            print (str(size[0]) + size[1] + '\t' + d['path'])
        else:
            print ("Error not valid location to look for! where=any, start or end")
            sys.exit(3)


