import re
from nltk.corpus import brown

# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst, item):
    if (item not in lst):
        lst.insert(len(lst), item)


class Lexicon:
    """stores known word stems of various part-of-speech categories"""

    def __init__(self):
        self.lb = []   # LexBase

    def add(self, stem, cat):
        if (cat in "PAINT"):
            add(self.lb, [stem, cat])
        else:
            print(cat + " is not one of the valid POS categories: P, A, I, N or T")
            return ''

    def getAll(self, cat):
        if (cat in "PAINT"):
            return [f for f in self.lb if f[1] == cat]
        else:
            print(cat + " is not one of the valid POS categories: P, A, I, N or T")
            return ''


class FactBase:
    """stores unary and binary relational facts"""

    def __init__(self):
        self.fb = []   # FactBase

    def addUnary(self, pred, e1):
        add(self.fb, [pred, e1])

    def addBinary(self, pred, e1, e2):
        add(self.fb, [pred, e1, e2])

    def queryUnary(self, pred, e1):
        return True if ([pred, e1] in self.fb) else False

    def queryBinary(self, pred, e1, e2):
        return True if ([pred, e1, e2] in self.fb) else False


def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""

    # ends in s,x,y,z,ch,sh -> add s
    # ends in y preceded by a vowel -> add s
    # form Xie where x is a letter not a vowel -> add s
    # ends in se or ze but not sse or zze -> add s
    # ends in e not preceeded by i,o,s,x,z,ch,sh -> add s
    if (re.match('(.+([^aeiousxyz(ch)(sh)]|[aeiou]y|([^s]se|[^z]ze)|[^iosxz](?<!(ch|sh))e)$)|[^aeiou]ie$', s)):
        s += "s"
        return s
    # ends in y preceeded by a non vowel and contains at least three letters -> change y to ies
    elif (re.match('.+[^aeiou]y$', s)):
        s = s[:-1] + "ies"
        return s
    # ends in o,x,ch,sh,ss,zz -> add es
    elif (re.match('.+([ox]|(?<=(ch|sh|ss|zz)))$', s)):
        s += "es"
        return s
    # have -> has
    elif (re.match('have', s)):
        s[-2] = "s"
        s = s[:-2]
        return s
    else:
        return ""


def add_proper_name(w, lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] <= 'Z'):
        lx.add(w, 'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement(lx, wlist, fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name(wlist[0], lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a', 'an']):
                lx.add(wlist[3], 'N')
                fb.addUnary('N_'+wlist[3], wlist[0])
            else:
                lx.add(wlist[2],'A')
                fb.addUnary('A_'+wlist[2], wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add(stem, 'I')
                fb.addUnary('I_'+stem, wlist[0])
            else:
                msg = add_proper_name(wlist[2], lx)
                if (msg == ''):
                    lx.add(stem, 'T')
                    fb.addBinary('T_'+stem, wlist[0], wlist[2])
    return msg

# End of PART A.


# Testing

if __name__ == "__main__":
    print("========Testing========")
    # lx = Lexicon()
    # lx.add("John", "P")
    # lx.add("Mary", "P")
    # lx.add("like", "T")
    # lx.add("fly", "I")
    # lx.add("fly", "N")
    # print(lx.getAll("P"))

    # fb = FactBase()
    # fb.addUnary("duck", "John")
    # fb.addBinary("love", "John", "Mary")
    # print(fb.queryUnary("duck", "John"))           # True
    # print(fb.queryBinary("love", "Mary", "John"))  # False

    threesgverbs = ["eat", "tell", "show", "pay", "buy", "fly", "try", "unify", "die", "lie", "tie", "go", "box", "attach", "wash", "dress", "fizz", "lose", "daze", "lapse", "analyse"]
    [print(verb_stem(s)) for s in threesgverbs]
    print("=======================")

