# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""

    def __int__(self):
        self.lb = []   # LexBase

    def add(self, stem, cat):
        if (cat in "PAINT"):
            if ((stem, cat) not in self.lb):
                self.lb.insert((stem, cat))
            else:
                print((stem, cat) + " already in lex base")
        else:
            print(cat + " is not one of the valid POS categories: P, A, I, N or T")

    def getAll(self, cat):
        return [f for f in self.lb if f[1] == cat]



class FactBase:
    """stores unary and binary relational facts"""

    def __init__(self):
        self.fb = []   # FactBase

    def addUnary(self, pred, e1):
        if ((pred, e1) not in self.fb):
            self.fb.insert((pred, e1))
        else:
            print((pred, e1) + " already in fact base")

    def addBinary(self, pred, e1, e2):
        if ((pred, e1, e2) not in self.fb):
            self.fb.insert((pred, e1, e2))
        else:
            print((pred, e1, e2) + " already in fact base")

    def queryUnary(self, pred, e1):
        return True if ((pred, e1) in self.fb) else False

    def queryBinary(self, pred, e1, e2):
        return True if ((pred, e1, e2) in self.fb) else False

import re
from nltk.corpus import brown 
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""

    if (re.match('.*[^aeiousxyz(ch)(sh)]$', s)):                  # ends in s,x,y,z,ch,sh -> add s
        s += 's'
    elif (re.match('.*[aeiou]y', s)):                             # ends in y preceeded by a vowel -> add s
        s += 's'
    elif (re.match('.+[^aeiou]y', s)):              # ends in y preceeded by a non vowel and contains at least three letters -> change y to ies
        s[-1] = 'i'
        s += 'es'
    elif (re.match('[^aeiou]ie', s)):                            # form Xie where x is a letter not a vowel -> add s
        s += 's'
    elif (re.match('.*[ox]|.*(ch|sh|ss|zz)', s)):                           # ends in o,x,ch,sh,ss,zz -> add es
    elif (re.match('.*[^s]se|.*[^z]ze', s)):                        # ends in se or ze but not sse or zze -> add s
    elif (re.match('have', s)):                                 # have -> has
    elif (re.match('', s)):                                     # ends in e not preceeded by i,o,s,x,z,ch,sh -> add s
    else:
        return None

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg
                        
# End of PART A.

