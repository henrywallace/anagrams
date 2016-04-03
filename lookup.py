import argparse
import re

with open('enable1.txt') as f:
    words = [word.strip() for word in f]

parser = argparse.ArgumentParser(description="Lookup regex pattern in ENABLE dicitonary")
parser.add_argument('pattern')
args = parser.parse_args()

matches = [word for word in words if re.fullmatch(args.pattern, word)]
for word in sorted(matches, key=len):
    print(word)