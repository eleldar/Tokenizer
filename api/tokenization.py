import re
import icu
import regex
from argparse import ArgumentParser

filters = [
        {"replace_ks_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "ks",
          "type": "pattern_replace",
          "replacement": "x"
        }},
        {"replace_ts_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "ts",
          "type": "pattern_replace",
          "replacement": "c"
        }},
        {"replace_sch_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "(sch)|(shch)",
          "type": "pattern_replace",
          "replacement": "s"
        }},
        {"replace_cszh_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "([csz])h",
          "type": "pattern_replace",
          "replacement": "$1"
        }},
        {"replace_ph_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "ph",
          "type": "pattern_replace",
          "replacement": "f"
        }},
        {"replace_kh_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "kh",
          "type": "pattern_replace",
          "replacement": "h"
        }},
        {"replace_jo_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "[iyj]o",
          "type": "pattern_replace",
          "replacement": "e"
        }},
        {"replace_ij_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "([aeiouy])[iyj]\\b",
          "type": "pattern_replace",
          "replacement": "$1"
        }},
        {"replace_j_filter": {
          "flags": "CASE_INSENSITIVE",
          "pattern": "[iyj]([aeiuy])",
          "type": "pattern_replace",
          "replacement": "$1"
        }},
#        {"remove_double": {
#          "flags": "CASE_INSENSITIVE",
#          "pattern": "(\\p{IsAlphabetic})\\1+",
#          "type": "pattern_replace",
#          "replacement": "$1"
#        }},
]

def remove_double(word):
    return re.sub(r'(.)\1', lambda x: x.group(1), word) 


def re_filters(word, filters=filters):
    '''apply filter with re to word'''
    for filter in filters:
        for items in filter.values():
            pattern = items['pattern']
            replacement = items['replacement']
            word = regex.subf(pattern, replacement, word) if '$' not in replacement else re.sub(pattern, replacement.replace('$', '\\'), word)
    return word


def transliterate(word):
    '''transliterate by icu'''
    tr = icu.Transliterator.createInstance(
        "Any-Latin; Latin-ASCII; NFD; [:Nonspacing Mark:] Remove; ['\"] Remove; [\\p{Z}] Remove; NFC"
    )
    return tr.transliterate(word)


def tokenize(string):
    '''get full result'''
    # 1. split and lower
    words = [word.lower() for word in string.split()]

    # 2. ICU
    words = list(map(transliterate, words))
    pass

    # 3. re
    words = list(map(re_filters, words))

    words = list(map(remove_double, words))
    return " ".join(words)


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(
        "-t", "--text", dest="text", default='"Александр Aleksandr Alexandr"',
        help=f'Enter text; default="Александр Aleksandr Alexandr"'
    )

    args = parser.parse_args()
    print(f'{args.text}: "{tokenize(args.text)}"')
