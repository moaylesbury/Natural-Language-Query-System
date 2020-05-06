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
    # list to hold unchanging plurals
    u_p = []
    # dictionary to hold key : value = word : tag, where tag is NN or NNS
    nn_s = {}
    # opens corpus
    with open("sentences.txt", "r") as f:
        # loops through each line of the corpus
        for line in f:
            # splits into word|tag
            for wordtag in line.split():
                # splits into word and tag
                word, tag0 = wordtag.split('|')
                # removes dollar sign from the end of tags where a new line would be
                tag = remove_new_line_char(tag0)
                # only dealing with nouns
                if tag == "NN" or tag == "NNS":
                    # if the word is in the key set then the word has been added as NN or NNS
                    if word in nn_s.keys():
                        # if the word's tag is not equal to the current tag then the word can have both NN and NNS tags
                        # thus is an unchanging plural
                        if nn_s.get(word) != tag:
                            # check the word hasn't already been identified as an unchanging plural
                            if word not in u_p:
                                u_p.append(word)
                    else:
                        # if the word isn't in the key set, it needs to be added to the dictionary
                        nn_s[word] = tag
    return u_p


def remove_new_line_char(tag):
    return tag[:-2] if tag[-1] == "$" else tag


unchanging_plurals_list = unchanging_plurals()


def noun_stem(s):
    """extracts the stem from a plural noun, or returns empty string"""
    # if noun is unchanging plural, return the empty string
    if s in unchanging_plurals_list:
        return ""
    # if noun stem ends in man, plural replaces with men
    elif (re.match('.*man$', s)):
        s[-2] = "e"
        return s
    # otherwise use rules for 3s formation
    else:
        return verb_stem(s)


def tag_word(lx, wd):
    """returns a list of all possible tags for wd relative to lx"""
    tags = []

    for i in function_words_tags:
        if wd == i[0]:
            tags.append(i[1])

    for i in "PAINT":
        returned = lx.getAll(i)
        # print(returned)
        if (len(returned) != 0):
            for j in returned:
                if j[0] == wd:

                    if j[1] not in tags:
                        tags.append(j[1])
                    if j[1] == "N":
                        if noun_stem(wd) == "":
                            if j[1] not in tags:
                                tags.append(j[1] + "s")
                        else:
                            if j[1] not in tags:
                                tags.append(j[1] + "p")
                    if j[1] in "IT":
                        if verb_stem(wd) == "":
                            if j[1] not in tags:
                                tags.append(j[1] + "s")
                        else:
                            if j[1] not in tags:
                                tags.append(j[1] + "p")
                    if j[1] in "PA":
                        if j[1] not in tags:
                            tags.append(j[1])
    return tags
        

def tag_words(lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word(lx, wds[0])
        tag_rest = tag_words(lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# Some testing
# print("TESTING")
# lx = Lexicon()
# lx.add("John", "P")
# lx.add("Mary", "P")
# lx.add("like", "T")
# lx.add("fly", "I")
# lx.add("fly", "N")
# wd = "John"

# print(tag_word(lx, "John"))

# End of PART B.
