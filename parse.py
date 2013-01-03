#!/usr/bin/env python2
#from pyparsing import Forward, nestedExpr, Word, alphanums
import tree_parser
from math import log


def get_p(t, f):
    ft = f[t[0]]
    if t[0] in f:
        return ft[t[1:]] / float(sum(ft.values()))
    else:
        return 0.0

def get_logp(t, f):
    return log(get_p(t, f))


def traverse(o):
    try:
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
    except IndexError:
        yield ()

def traverse_parent(parent, o):
    """Append parent tag to child for better context awareness.
    """
    try:
        if isinstance(o[1], basestring):
            yield (parent + '/' + o[0], o[1])  # Terminal
        else:
            if len(o) > 2:      # Non-terminal
                yield (parent + '/' + o[0], o[0] + '/' + o[1][0], o[0] + '/' + o[2][0])
            else:
                yield (parent + '/' + o[0], o[0] + '/' + o[1][0])
            for value in o[1:]:
                for subvalue in traverse_parent(o[0], value):
                    yield subvalue
    except IndexError:
        yield ()


def main():
    f = open('data/train_trees')
    frequencies = dict()
    for i, line in enumerate(f):
        l = tree_parser.get_tree(line)  # charity from Patrick de Kok
        for t in traverse_parent('TOP', l[1]): # skip TOP
            if t[0] in frequencies:
                if t[1:] in frequencies[t[0]]:
                    frequencies[t[0]][t[1:]] += 1
                else:
                    frequencies[t[0]][t[1:]] = 1
            else:
                frequencies[t[0]] = {t[1:]: 1}
    print frequencies


if __name__ == '__main__':
    main()
