"""Command-line script to find anagrams of subsets of letters.

This script was built with the intent to aid in playing Words With Friends.
Hence, the letter scoring and dictionary match that game."""

import re
from collections import Counter, namedtuple
from tabulate import tabulate
from operator import attrgetter
import argparse


def sub_anagram(letters):
    """Compile regex that matches an anagram of a subset of `letters`"""
    pattern = r''
    counts = Counter(letters)
    for letter, count in counts.items():
        pattern += '(?!(.*{}){{{},}})'.format(letter, count + 1)
    pattern += '[{}]*'.format(''.join(counts.keys()))
    return re.compile(pattern)


def word_score(word, letter_scores):
    """Score word based on points: sum of letter scores."""
    return sum(letter_scores[letter] for letter in word)


def print_matches(letters, words, letter_scores, sortby='len'):
    """Print table of solutions, with columns: word, len, score."""
    pattern = sub_anagram(letters)
    is_anagram = lambda word: pattern.fullmatch(word)
    Word = namedtuple('Word', ['word', 'len', 'score'])
    table = []
    for anagram in filter(is_anagram, words):
        table.append(Word(anagram, len(anagram),
                     word_score(anagram, letter_scores)))
    table = sorted(table, key=attrgetter(sortby))
    print(tabulate(table, headers=Word._fields))

if __name__ == '__main__':
    # store words from dictionary ENABLE
    with open('enable1.txt') as f:
        WORDS = [line.strip() for line in f]

    # put letter scores into a `dict`
    SCORE_LETTERS = [(0, '_'), (1, 'srtioae'), (2, 'ludn'), (3, 'ygh'),
                     (4, 'bcfmpw'), (5, 'kv'), (8, 'x'), (10, 'jqz')]
    LETTER_SCORES = {}
    for score, letters in SCORE_LETTERS:
        for letter in letters:
            LETTER_SCORES[letter] = score

    # parse command line
    PARSER = argparse.ArgumentParser(description='Get anagrams of subsets.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    PARSER.add_argument('letters', help='Letters whose subsets to find anagrams with.')
    PARSER.add_argument('--sort', default='len',
        choices=['word', 'len', 'score'],
        help='Method to sort by, viz. word, len, score')
    ARGS = PARSER.parse_args()
    print_matches(ARGS.letters, WORDS, LETTER_SCORES, sortby=ARGS.sort)


"""
References:
===========
- http://stackoverflow.com/a/14562594
- https://en.wikipedia.org/wiki/Words_with_Friends
- http://gaming.stackexchange.com/a/7163
"""
