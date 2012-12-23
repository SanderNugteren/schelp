#!/usr/bin/env python2
from pyparsing import Forward, nestedExpr, Word, alphanums
import tree_parser
import sys


def get_p(t, f):
    if t[0] in f:
        return f[t[0]][t[1:]] / float(sum(f[t[0]].values()))
    return 0.0

def get_logp(t, f):
    return log(get_p(t, f))


def traverse(o):
    if isinstance(o[1], basestring):
        yield (o[0], o[1])  # Terminal
    else:
        if len(o) > 2:      # Non-terminal
            yield (o[0], o[1][0], o[2][0])
        else:
            yield (o[0], o[1][0])
        for value in o[1:]:
            for subvalue in traverse(value):
                yield subvalue


def main():
    f = open('data/train_trees')
    frequencies = dict()
    for i, line in enumerate(f):
        l = tree_parser.get_tree(line)  # charity from Patrick de Kok
        for t in traverse(l[1]): # skip TOP
            if t[0] in frequencies:
                if t[1:] in frequencies[t[0]]:
                    frequencies[t[0]][t[1:]] += 1
                else:
                    frequencies[t[0]][t[1:]] = 1
            else:
                frequencies[t[0]] = {t[1:]: 1}
    print frequencies


def main():
    f = open('data/train_trees')
    frequencies = dict()
    for line in f:
        l = tree_parser.get_tree(line)  # charity from Patrick de Kok
        for t in traverse(l[1]): # skip TOP
            if t[1:] in frequencies:
                if not t[0] in frequencies[t[1:]]:
                    frequencies[t[1:]].append(t[0])
            else:
                frequencies[t[1:]] = [t[0]]
    print frequencies

if __name__ == '__main__':
    main()
