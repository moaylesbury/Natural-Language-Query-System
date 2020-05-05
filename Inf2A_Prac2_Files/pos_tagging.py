# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    # holds unchanging plurals
    u_p = []
    nn_s = {}
    with open("sentences.txt", "r") as f:
        for line in f:
            # splits into word|tag
            for wordtag in line.split():
                # splits into word and tag
                word, tag0 = wordtag.split('|')
                # removes dollar sign from the end of tags where a new line would be
                tag = remove_new_line_char(tag0)
                # only dealing with nouns
                if tag == "NN" or tag == "NNS":
                    if word in nn_s.keys():
                        if nn_s.get(word) != tag:
                            if word not in u_p:
                                u_p.append(word)
                    else:
                        nn_s[word] = tag
    print(u_p)

def remove_new_line_char(tag):
    return tag[:-2] if tag[-1] == "$" else tag

unchanging_plurals_list = unchanging_plurals()


def noun_stem(s):
    """extracts the stem from a plural noun, or returns empty string"""    
    # if noun stem ends in man, plural replaces with men
    if (re.match('.*man$', s)):
        s[-2] = "e"
        return s
    # otherwise use rules for 3s formation
    else:
        # if verb_stem(s) returns the empty string then s must be an unchanging plural
        return verb_stem(s) if verb_stem(s) != "" else ""



def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.