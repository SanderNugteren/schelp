#!/usr/bin/env python2
from pyparsing import Forward, nestedExpr, Word, alphas

sample = "(TOP (S (NP (DT A) (NP@ (NN record) (NN date))) (S@ (VP (VBZ has) (VP@ (RB n't) (VP (VBN been) (VP (VBN set))))) (. .))) )"

characters = alphas + '@' + "'" + "," + "."

enclosed = Forward()
nestedParens = nestedExpr('(', ')', content=enclosed)
enclosed << (Word(characters) | nestedParens)

l = enclosed.parseString(sample).asList()


def get_p(t, f):
    return f[t[0]][t[1:]] / float(sum(f[t[0]].values()))


def traverse(o):
    if isinstance(o, list):
        if isinstance(o[1], str):
            yield (o[0], o[1])
        else:
            if len(o) > 2:
                yield (o[0], o[1][0], o[2][0])
            for value in o:
                for subvalue in traverse(value):
                    yield subvalue


frequencies = dict()
for t in traverse(l[0][1]): # skip TOP
    if t[0] in frequencies:
        if t[1:] in frequencies[t[0]]:
            frequencies[t[0]][t[1:]] += 1
        else:
            frequencies[t[0]][t[1:]] = 1
    else:
        frequencies[t[0]] = {t[1:]: 1}


#print frequencies

#print get_p(('S', 'NP', 'S@'), frequencies)
