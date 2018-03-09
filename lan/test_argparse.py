import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--CASE', type=str, required=True, help="CASE can be 'calculate' or 'merge'")
parser.add_argument('-MICE', '--MOUSENAMELIST', type=str, nargs='*', help="Enter mouse names separated by space")
args = parser.parse_args()
CASE = args.CASE
mouseNameList = args.MOUSENAMELIST

print('CASE:', CASE)
print('mouseNameList:', mouseNameList, type(mouseNameList))

