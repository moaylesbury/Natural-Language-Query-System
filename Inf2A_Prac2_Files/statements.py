import re
import nltk
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
        #if (cat in "PAINT"):
        print("LEX ADDITION: ", stem, cat)
        add(self.lb, [stem, cat])

    def getAll(self, cat):
        #if (cat in "PAINT"):
        return [f[0] for f in self.lb if f[1] == cat]


class FactBase:
    """stores unary and binary relational facts"""

    def __init__(self):
        self.fb = []   # FactBase

    def addUnary(self, pred, e1):
        print("UNARY   ", pred, e1)
        add(self.fb, [pred, e1])

    def addBinary(self, pred, e1, e2):
        print("BINARY  ", pred, e1, e2)
        add(self.fb, [pred, e1, e2])

    def queryUnary(self, pred, e1):
        print("query unary", pred, e1)
        print([pred, e1] in self.fb)
        return True if ([pred, e1] in self.fb) else False

    def queryBinary(self, pred, e1, e2):
        print("query binary")
        return True if ([pred, e1, e2] in self.fb) else False


def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    """3s = third person singular form, eg flies -> fly"""
    #nltk.download('brown')

    # copies s to a string that will be the verbstem
    verbstem = s

    # finding verb stem

    # have -> has
    if (re.match('has', s)):
        print("1")
        #return "has"
        return "have"
    # ends in s,x,y,z,ch,sh -> add s
    # ends in y preceded by a vowel -> add s
    # form Xie where x is a letter not a vowel -> add s
    # ends in se or ze but not sse or zze -> add s
    # ends in e not preceeded by i,o,s,x,z,ch,sh -> add s
    elif (re.match('((.+([^aeiousxyz(ch)(sh)]|[aeiou]y|([^s]se|[^z]ze)|[^iosxz](?<!(ch|sh))e))|[^aeiou]ie)s$', s)):
        print("2")
        #return s + "s"
        verbstem = verbstem[:-1]
    # ends in y preceeded by a non vowel and contains at least three letters -> change y to ies
    elif (re.match('.*[^aeiou]ies$', s)):
        print("3")
        #return s[:-1] + "ies"
        verbstem = verbstem[:-3] + 'y'
    # ends in o,x,ch,sh,ss,zz -> add es
    elif (re.match('.+([ox]|(?<=(ch|sh|ss|zz)))es$', s)):
        print("4")
        #return s + "es"
        verbstem = verbstem[:-2]
    #else:
     #   return ""

    # Checking with the corpus

    print("3s form: ", s, " Verbstem: ", verbstem)

    # number of  3gs and verb stem tags counted
    stags, vstags = 0, 0

    # don't check have, are, do so just return the stem

    if s == "have" or s == "are" or s == "do":
        return verbstem
    # otherwise count tags
    else:
        # verb stem tagged VB and 3s form VBZ
        for m in brown.tagged_words():
            if m[0] == s:
                if m[1] == "VBZ":
                    stags += 1
            elif m[0] == verbstem:
                if m[1] == "VB":
                    vstags += 1

    print("stags ", stags, " vstags: ", vstags)

    if stags == vstags == 0:
        return ""

    if stags + vstags > 0:
        return verbstem





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
    print("msg: " + msg)
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
    lx = Lexicon()
    lx.add("Michael", "P")
    lx.add("duck", "N")
    fb = FactBase()
    fb.addUnary("duck", "Michael")
    fb.queryUnary("duck", "Michael")
    print(lx.getAll("P"))
    #print("========Testing========")
    #words = ["eats", "tells", "shows", "pays", "buys", "flies", "tries", "unifies", "dies", "lies", "ties", "goes", "boxes", "attaches", "washes", "dresses", "fizzes", "loses", "dazes", "lapses", "analyses", "has", "likes", "hates", "bathes"]
    #correct = ["eat", "tell", "show", "pay", "buy", "fly", "try", "unify", "die", "lie", "tie", "go", "box", "attach", "wash", "dress", "fizz", "lose", "daze", "lapse", "analyse", "have", "like", "hate", "bathe"]

    #for i in words:
    #    print("--------------------------------------------------")
    #    print("[--]", i, " --> ", verb_stem(i), "[--]")
    #    print("--------------------------------------------------")
    #stems = [verb_stem(i) for i in words]
    #print(words)
    #print(stems)
    #print("========Testing========")
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

   # threesgverbs = ["eat", "tell", "show", "pay", "buy", "fly", "try", "unify", "die", "lie", "tie", "go", "box", "attach", "wash", "dress", "fizz", "lose", "daze", "lapse", "analyse", "have"]
    ##[print(verb_stem(s)) for s in threesgverbs]


