#!/usr/bin/env python2
from pyparsing import Forward, nestedExpr, Word, alphanums
import tree_parser
import sys
from parse import traverse, traverse_parent


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
        for t in traverse_parent('TOP', l[1]): # skip TOP
            if t[1:] in frequencies:
                if not t[0] in frequencies[t[1:]]:
                    frequencies[t[1:]].append(t[0])
            else:
                frequencies[t[1:]] = [t[0]]
    print frequencies

if __name__ == '__main__':
    main()
