#!/usr/bin/env python

# # Standard Python 2.7 Library
# import argparse
# from pipes import quote

# # Third-Party Libraries
# import sh as pbs # https://github.com/amoffat/pbs

# def convert(*filenames):
#     for filename in filenames:
#         output = filename[:-4] + ".avi"
#         pbs.mencoder(quote(filename), "-ovc copy", o=output)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Convert MKV to AVI.")
#     parser.add_argument('filenames', metavar='FILENAMES', type=str, nargs='+')
#     args = parser.parse_args()
#     convert(*args.filenames)

import argparse
import subprocess

def convert(*filenames):
    for filename in filenames:
        output = filename[:-4] + ".avi"
        subprocess.run(["mencoder", filename, "-ovc", "copy", "-o", output])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert MKV to AVI.")
    parser.add_argument('filenames', metavar='FILENAMES', type=str, nargs='+')
    args = parser.parse_args()
    convert(*args.filenames)