import sys
from itertools import combinations
from freqs import frequencies, r_rules
from parse import get_logp
from pprint import pprint
from math import log
import cProfile

def main(filename):
    f = open(filename)
    for table in cyk(f):
        pprint(table)


def cyk(f):
    for line in f:
        words = line.strip().split(" ")
        table = [[set()] * i for i in xrange(1, len(words) + 1)] # CYK table
        for i, j in table_traverse(len(words)):
            if i == j:  # Unary rules
                print 'unary'
                terminals = r_rules[(words[i],)]
                if len(terminals) == 1: # log p(rule|terminal) = 0
                    table[i][j] |= set([(terminals[0], 0)])
                else: # log p(rule|terminal)
                    total = 0.0
                    for t in terminals:
                        total += frequencies[t][(words[i],)]
                    for t in terminals:
                        table[i][j] |= set([(t,
                            log(frequencies[t][(words[i],)]/total))])
                new_keys = set()
                keys_added = True
                while keys_added: # Add nonterminal unary rules
                    keys_added = False
                    for rule in table[i][j]:
                        if (rule,) in r_rules:
                            for key in r_rules[(rule,)]:
                                if key not in new_keys:
                                    new_keys |= set([key])
                                    keys_added = True
                table[i][j] |=  new_keys
            else:   # Binary rules
                print 'binary'
                for ll in range(i, j):
                    #dd = ll + 1
                    #down = set(table[j][dd])
                    down = set(table[j][ll+1])
                    left = set(table[ll][i])
                    addRule = True
                    for l in left:
                        for d in down:
                            #print 'ld: ' + str((l, d))
                            if (l[0], d[0]) in r_rules:
                                for parent in r_rules[(l[0], d[0])]:
                                    #print parent + '->' + str(l[0]) + ' ' + str(d[0])
                                    rule = (parent, l[0], d[0])
                                    p = get_logp(rule , frequencies) + l[-1] + d[-1]
                                    #new code
                                    #check if there already is an entry for this rule
                                    addRule = True
                                    for t in table[j][i]:
                                        if t[:-1] == rule:
                                            if t[-1] < p:
                                                #and if so, if it is higher
                                                table[j][i].remove(t)
                                            else:
                                                addRule = False
                                            break
                                    if addRule:
                                        table[j][i].add((parent, l[0], d[0], p))
        yield table


def table_traverse(table_length):
    for i in xrange(table_length):
        for j in xrange(table_length - i):
            yield j, i+j


if __name__ == '__main__':
    cProfile.run("main('data/one_sentence')")
