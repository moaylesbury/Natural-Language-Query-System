# File: semantics.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised October 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu with help from Kiniorski Filip


# PART D: Semantics for the Query Language.

    #    S      -> WHO QP[y] QM | WHICH Nom[y] QP[y] QM
    #    QP[x]  -> VP[x] | DO[y] NP[y] T[p]
    #    VP[x]  -> I[x] | T[x] NP | BE[x] A | BE[x] NP[x] | VP[x] AND VP[x]
    #    NP[s]  -> P | AR Nom[s]
    #    NP[p]  -> Nom[p]
    #    Nom[x] -> AN[x] | AN[x] Rel[x]
    #    AN[x]  -> N[x] | A AN[x]
    #    Rel[x] -> WHO VP[x] | NP[y] T[y]
    #    N[s]   -> "Ns"  etc.
    '''
       S     -> WHO QP QM | WHICH Nom QP QM
       QP    -> VP | DO NP T
       VP    -> I | T NP | BE A | BE NP | VP AND VP
       NP    -> P | AR Nom | Nom
       Nom   -> AN | AN Rel
       AN    -> N | A AN
       Rel   -> WHO VP | NP T

       N     -> "Ns" | "Np"
       I    -> "Is" | "Ip"
       T    -> "Ts" | "Tp"
       A     -> "A"
       P     -> "P"
       BE    -> "BEs" | "BEp"
       DO    -> "DOs" | "DOp"
       AR    -> "AR"
       WHO   -> "WHO"
       WHICH -> "WHICH"
       AND   -> "AND"
       QM    -> "?"
    '''

from agreement import *

def sem(tr):
    """translates a syntax tree into a logical lambda expression (in string form)"""
    rule = top_level_rule(tr)


    if (tr.label() == 'P'):       # entities
        return tr[0][0]
    elif (tr.label() == 'N'):     # unary predicate
        return '(\\x.' + tr[0][0] + '(x))'  # \\ is escape sequence for \
    elif (tr.label() == 'A'):     # unary predicate
        return '(\\x.' + tr[0][0] + '(x))'
    elif (tr.label() == 'I'):     # unary predicate
        return '(\\x.' + tr[0][0] + '(x))'
    elif (tr.label() == 'T'):     # binary predicate
        return '(\\x. (exists y.(' + tr[0][0] + ' & ' + tr[0][1] + ')))'



    elif rule == "S -> WHO QP QM":
        return '(\\x.' + sem(tr[1]) + '(x))'
    elif rule == "S -> WHICH Nom QP QM":
        return '(\\x.' + sem(tr[1]) + ') & (' + sem(tr[2]) + ')'
    elif rule == "QP -> VP":
        return '(\\x.' + sem(tr[0]) + '(x))'
    elif rule == "QP -> DO NP T":
        return ''
    elif rule == "VP -> I":
    elif rule == "VP -> T NP":
    elif rule == "VP -> BE A":
    elif rule == "VP -> BE NP":
    elif rule == "Nom -> AN":
    elif rule == "Nom -> AN Rel":
    elif rule == "AN -> VP AND VP":
        return '(\\x.' + sem(tr[0]) + '(x) & '+ sem(tr[2]) + '(x))'
    elif rule == "AN -> N":
        return sem(tr[0])
    elif (rule == 'AN -> A AN'):
        return '(\\x.(' + sem(tr[0]) + '(x) & ' + sem(tr[1]) + '(x)))'
    elif rule == "Rel -> WHO VP":
    elif rule == "Rel -> NP T":
    elif (rule == 'NP -> AR Nom'):
    elif (rule == 'NP -> Nom'):
    elif (rule == 'NP -> P'):
        return '(\\x.(x = ' + sem(tr[0]) + '))'
    elif  # add more code here











# Logic parser for lambda expressions

from nltk.sem.logic import LogicParser
lp = LogicParser()

# Lambda expressions can now be checked and simplified as follows:

#   A = lp.parse('(\\x.((\\P.P(x,x))(loves)))(John)')
#   B = lp.parse(sem(tr))  # for some tree tr
#   A.simplify()
#   B.simplify()


# Model checker

from nltk.sem.logic import *

# Can use: A.variable, A.term, A.term.first, A.term.second, A.function, A.args

def interpret_const_or_var(s,bindings,entities):
    if (s in entities): # s a constant
        return s
    else:               # s a variable
        return [p[1] for p in bindings if p[0]==s][0]  # finds most recent binding

def model_check (P,bindings,entities,fb):
    if (isinstance (P,ApplicationExpression)):
        if (len(P.args)==1):
            pred = P.function.__str__()
            arg = interpret_const_or_var(P.args[0].__str__(),bindings,entities)
            return fb.queryUnary(pred,arg)
        else:
            pred = P.function.function.__str__()
            arg0 = interpret_const_or_var(P.args[0].__str__(),bindings,entities)
            arg1 = interpret_const_or_var(P.args[1].__str__(),bindings,entities)
            return fb.queryBinary(pred,arg0,arg1)
    elif (isinstance (P,EqualityExpression)):
        arg0 = interpret_const_or_var(P.first.__str__(),bindings,entities)
        arg1 = interpret_const_or_var(P.second.__str__(),bindings,entities)
        return (arg0 == arg1)
    elif (isinstance (P,AndExpression)):
        return (model_check (P.first,bindings,entities,fb) and
                model_check (P.second,bindings,entities,fb))
    elif (isinstance (P,ExistsExpression)):
        v = str(P.variable)
        P1 = P.term
        for e in entities:
            bindings1 = [(v,e)] + bindings
            if (model_check (P1,bindings1,entities,fb)):
                return True
        return False

def find_all_solutions (L,entities,fb):
    v = str(L.variable)
    P = L.term
    return [e for e in entities if model_check(P,[(v,e)],entities,fb)]


# Interactive dialogue session

def fetch_input():
    s = raw_input('$$ ')
    while (s.split() == []):
        s = raw_input('$$ ')
    return s    

def output(s):
    print ('     '+s)

def dialogue():
    lx = Lexicon()
    fb = FactBase()
    output('')
    s = fetch_input()
    while (s.split() == []):
        s = raw_input('$$ ')
    while (s != 'exit'):
        if (s[-1]=='?'):
            sent = s[:-1] + ' ?'  # tolerate absence of space before '?'
            if len(sent) == 0:
                output ("Eh??")
            else:
                wds = sent.split()
                trees = all_valid_parses(lx,wds)
                if (len(trees)==0):
                    output ("Eh??")
                elif (len(trees)>1):
                    output ("Ambiguous!")
                else:
                    tr = restore_words (trees[0],wds)
                    lam_exp = lp.parse(sem(tr))
                    L = lam_exp.simplify()
                    # print L  # useful for debugging
                    entities = lx.getAll('P')
                    results = find_all_solutions (L,entities,fb)
                    if (results == []):
                        if (wds[0].lower() == 'who'):
                            output ("No one")
                        else:
                            output ("None")
                    else:
                        buf = ''
                        for r in results:
                            buf = buf + r + '  '
                        output (buf)
        elif (s[-1]=='.'):
            s = s[:-1]  # tolerate final full stop
            if len(s) == 0:
                output ("Eh??")
            else:
                wds = s.split()
                msg = process_statement(lx,wds,fb)
                if (msg == ''):
                    output ("OK.")
                else:
                    output ("Sorry - " + msg)
        else:
            output ("Please end with \".\" or \"?\" to avoid confusion.")
        s = fetch_input()
            
if __name__ == "__main__":
    dialogue()
# End of PART D.
