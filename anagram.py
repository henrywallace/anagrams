"""Command-line script to find anagrams of subsets of letters.

This script was built with the intent to aid in playing Words With Friends.
Hence, the letter scoring and dictionary match that game."""

import re
from collections import Counter, namedtuple
from itertools import groupby
from tabulate import tabulate
from operator import attrgetter

with open('enable1.txt') as f:
    words = [line.strip() for line in f]

SCORES = [(0, '_'), (1, 'srtioae'), (2, 'ludn'), (3, 'ygh'), (4, 'bcfmpw'), 
    (5, 'kv'), (8, 'x'), (10, 'jqz')]
letter_scores = {}
for score, letters in SCORES:
    for letter in letters:
        letter_scores[letter] = score

def sub_anagram(letters):
    """Compile regex that matches an anagram of a subset of `letters`"""
    pattern = r''
    counts = Counter(letters)
    for letter, count in counts.items():
        pattern += '(?!(.*{}){{{},}})'.format(letter, count + 1)
    pattern += '[{}]*'.format(''.join(counts.keys()))
    return re.compile(pattern)

def word_score(word):
    """Score word based on points: sum of letter scores"""
    return sum(letter_scores[letter] for letter in word)

def print_matches(letters, words):
    pattern = sub_anagram(letters)
    is_anagram = lambda word: pattern.fullmatch(word)
    Word = namedtuple('Word', ['word', 'len', 'score'])
    table = []
    for anagram in filter(is_anagram, words):
        table.append(Word(anagram, len(anagram), word_score(anagram)))
    table = sorted(table, key=attrgetter('len'))
    print(tabulate(table, headers=Word._fields))

print_matches('hello', words)

"""
References:
===========
- http://stackoverflow.com/a/14562594
- https://en.wikipedia.org/wiki/Words_with_Friends
- http://gaming.stackexchange.com/a/7163
"""