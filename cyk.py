# vim: set nowrap:
import sys
from itertools import combinations
from freqs import frequencies, r_rules
from parse import get_logp
from pprint import pprint
from math import log
import cProfile

def main(filename):
    f = open(filename)
    for tree in cyk(f):
        #pprint(table)
        print tree
        return 0

def cyk(f):
    for line in f:
        try:
            words = line.strip().split(" ")
            table = []
            for i in xrange(1, len(words) + 1):
                row = []
                for j in xrange(i):
                    row.append({})
                table.append(row)
            for i, j in table_traverse(len(words)):
                if i == j:  # Unary rules
                    terminals = r_rules[(words[i],)]
                    if len(terminals) == 1: # log p(rule|terminal) = 0
                        table[i][j][terminals[0]] = (0.0, words[i])
                    else: # log p(rule|terminal)
                        total = 0.0
                        for t in terminals:
                            total += frequencies[t][(words[i],)]
                        for t in terminals:
                            table[i][j][t] = (log(frequencies[t][(words[i],)]/total), words[i])
                    new_rules = set()
                    new_keys = set()
                    keys_added = True
                    while keys_added: # Add nonterminal unary rules
                        keys_added = False
                        for rule in table[i][j]:
                            if (rule,) in r_rules:
                                for key in r_rules[(rule,)]:
                                    #print key + '->' + rule
                                    if key not in new_keys:
                                        new_keys.add(key)
                                        new_rules.add((key, rule))
                                        keys_added = True
                    for key, rule in new_rules:
                        lp = get_logp((key, rule), frequencies)
                        if key in table[i][j]: # do not add recursive rules with
                            if table[i][j][key][0] > lp:
                                continue
                        table[i][j][key] = (lp, (rule, words[i]))
                else:   # Binary rules
                    for ll in range(i, j):
                        down = table[j][ll+1]
                        left = table[ll][i]
                        for l in left.keys():
                            for d in down.keys():
                                if (l, d) in r_rules:
                                    pl = left[l][0]
                                    pd = down[d][0]
                                    for parent in r_rules[(l, d)]:
                                        rule = (parent, l, d)
                                        p = get_logp(rule , frequencies) + pl + pd
                                        #check if there already is an entry for this rule
                                        if parent not in table[j][i] or table[j][i][parent][0] < p:
                                                lt = tree(l, left)
                                                dt = tree(d, down)
                                                table[j][i][parent] = (p, lt, dt)
        except KeyError:
            pass
        try:
            yield ('TOP', ('S', table[-1][0]['S'][1], table[-1][0]['S'][2]))
        except KeyError:
            yield ()

def tree(node, subtree):
    tree = (node, subtree[node][1:])
    if type(tree[1]) == tuple and type(tree[1][0]) == tuple and len(tree[1]) == 2:
        return (tree[0], tree[1][0], tree[1][1])
    else:
        return (tree[0], tree[1][0])

def table_traverse(table_length):
    for i in xrange(table_length):
        for j in xrange(table_length - i):
            yield j, i+j


if __name__ == '__main__':
    if False:
        cProfile.run("main('data/one_sentence')")
    else:
        main('data/test_sentence')

