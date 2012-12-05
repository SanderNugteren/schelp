import sys
from itertools import combinations
from freqs import frequencies, r_rules
from parse import get_logp
from pprint import pprint

def main(filename):
    f = open(filename)
    for table in cyk(f):
        pprint(table)
        sys.exit(0)
        print(viterbi(table))


def viterbi(table, i, j, parent):
    l = len(table)
    if j >= l or i < 0:
        return table[...]
    else:
        return viterbi(table, i-1, j, left) + viterbi(table, i, j+1, right)


def cyk(f):
    for line in f:
        words = line.strip().split(" ")
        table = [[set()] * i for i in xrange(1, len(words) + 1)] # CYK table
        for i, j in table_traverse(len(words)):
            if i == j:  # Unary rules
                table[i][j] = set(r_rules[(words[i],)]) # Add terminal rules
                new_keys = set()
                keys_added = True
                while keys_added: # Add nonterminal unary rules
                    keys_added = False
                    for rule in table[i][j]:
                        if rule in r_rules:
                            for key in r_rules[rule]:
                                new_keys |= key
                                keys_added = True
            else:   # Binary rules
                for ll in range(i, j):
                    dd = ll + 1
                    left = set(table[j][dd])
                    down = set(table[ll][i])
                    for l in left:
                        for d in down:
                            if (l, d) in r_rules:
                                for parent in r_rules[(l, d)]:
                                    p = get_logp((parent, l, d), frequencies)
                                    table[j][i].add((parent, l, d, p))
        yield table


def table_traverse(table_length):
        for i in xrange(table_length):
            for j in xrange(table_length - i):
                yield j, i+j


if __name__ == '__main__':
    main('data/test_sentence')
