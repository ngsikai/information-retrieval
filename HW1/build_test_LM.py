#!/usr/bin/python
from __future__ import division
import re
import nltk
import sys
import getopt
import math


def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and an URL separated by a tab(\t)
    """
    print 'building language models...'
    # This is an empty method
    # Pls implement your code in below

    input_file = open(in_file, 'r')
    train_input_list = input_file.read().split("\r\n")

    four_gram_table = {}
    ngram_count = {'malaysian': 0, 'indonesian': 0, 'tamil': 0}
    for sentence in train_input_list:
        sentence_parts = sentence.split(None, 1)
        # To handle possible empty strings or weird strings in training input
        if (len(sentence_parts) != 2):
            break
        language = sentence_parts[0]
        sentence_body = sentence_parts[1]
        char_list = list(sentence_body)
        for index in range(3):
            char_list.insert(0, 'START')
            char_list.append('END')
        for index in range(len(char_list) - 4):
            four_gram = (char_list[index], char_list[index + 1],
                         char_list[index + 2], char_list[index + 3])
            if four_gram in four_gram_table:
                four_gram_table[four_gram][language] += 1
                ngram_count[language] += 1
            else:
                four_gram_table[four_gram] = {'malaysian': 1, 'indonesian': 1,
                                              'tamil': 1}
                for value in ngram_count.itervalues():
                    value += 1
                four_gram_table[four_gram][language] += 1
                ngram_count[language] += 1
    return [four_gram_table, ngram_count]

    input_file.close()


def test_LM(in_file, out_file, LM):
    """
    test the language models on new URLs
    each line of in_file contains an URL
    you should print the most probable label for each URL into out_file
    """
    print "testing language models..."
    # This is an empty method
    # Pls implement your code in below

    four_gram_table = LM[0]
    ngram_count = LM[1]

    input_file = open(in_file, 'r')
    test_input_list = input_file.read().split("\r\n")
    for sentence in test_input_list:
        if sentence == "":
            break
        ngram_score = {'malaysian': 0, 'indonesian': 0, 'tamil': 0}
        invalid_ngram_count = 0
        total_ngram_count = 0
        char_list = list(sentence)
        for index in range(3):
            char_list.insert(0, 'START')
            char_list.append('END')
        for index in range(len(char_list) - 4):
            four_gram = (char_list[index], char_list[index + 1],
                         char_list[index + 2], char_list[index + 3])
            if four_gram in four_gram_table:
                for language, count in four_gram_table[four_gram].iteritems():
                    ngram_score[language] += math.log10(count/ngram_count[language])
            else:
                invalid_ngram_count += 1
            total_ngram_count += 1
        invalid_ngram_ratio = invalid_ngram_count / total_ngram_count
        if max(ngram_score.itervalues()) is 0 or invalid_ngram_ratio > 0.6:
            predicted_language = 'other'
        else:
            predicted_language = max(ngram_score.iterkeys(), key=(lambda language: ngram_score[language]))
        # print ngram_score
        print predicted_language
        # print predicted_language


def usage():
    print "usage: " + sys.argv[0] + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"

input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], 'b:t:o:')
except getopt.GetoptError, err:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == '-b':
        input_file_b = a
    elif o == '-t':
        input_file_t = a
    elif o == '-o':
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
