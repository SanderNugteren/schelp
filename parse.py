#!/usr/bin/env python2
from pyparsing import Forward, nestedExpr, Word, alphanums

characters = alphanums + "_:;~/<>@',.`$%+-&!?\"i#=*\\"

enclosed = Forward()
nestedParens = nestedExpr('(', ')', content=enclosed)
enclosed << (Word(characters) | nestedParens)


def get_p(t, f):
    if t[0] in f:
        return f[t[0]][t[1:]] / float(sum(f[t[0]].values()))
    return 0.0


def traverse(o):
    if not isinstance(o, basestring):
        if isinstance(o[1], basestring):
            yield (o[0], o[1])
        else:
            if len(o) > 2:
                yield (o[0], o[1][0], o[2][0])
            for value in o:
                for subvalue in traverse(value):
                    yield subvalue


def main():
    f = open('data/train_trees')
    frequencies = dict()
    for i, line in enumerate(f):
        if i > 99:
            break
        try:
            l = enclosed.parseString(line).asList()
            print i
        except:
            print 'X\t'+str(i)
            continue
        for t in traverse(l[0][1]): # skip TOP
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
