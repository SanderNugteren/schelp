#!/usr/bin/env python2
#from pyparsing import Forward, nestedExpr, Word, alphanums


from pyparsing import *
from base64 import b64decode
import pprint

def verifyLen(s,l,t):
    t = t[0]
    if t.len is not None:
        t1len = len(t[1])
        if t1len != t.len:
            raise ParseFatalException(s,l,\
                    "invalid data of length %d, expected %s" % (t1len, t.len))
    return t[1]

# define punctuation literals
LPAR, RPAR, LBRK, RBRK, LBRC, RBRC, VBAR = map(Suppress, "()[]{}|")

decimal = Regex(r'0|[1-9]\d*').setParseAction(lambda t: int(t[0]))
hexadecimal = ("#" + OneOrMore(Word(hexnums)) + "#")\
                .setParseAction(lambda t: int("".join(t[1:-1]),16))
bytes = Word(printables)
raw = Group(decimal("len") + Suppress(":") + bytes).setParseAction(verifyLen)
token = Word(alphanums + "-./_:*+=")
base64_ = Group(Optional(decimal|hexadecimal,default=None)("len") + VBAR 
    + OneOrMore(Word( alphanums +"+/=" )).setParseAction(lambda t: b64decode("".join(t)))
    + VBAR).setParseAction(verifyLen)
    
qString = Group(Optional(decimal,default=None)("len") + 
                        dblQuotedString.setParseAction(removeQuotes)).setParseAction(verifyLen)
simpleString = base64_ | raw | decimal | token | hexadecimal | qString

# extended definitions
decimal = Regex(r'-?0|[1-9]\d*').setParseAction(lambda t: int(t[0]))
real = Regex(r"[+-]?\d+\.\d*([eE][+-]?\d+)?").setParseAction(lambda tokens: float(tokens[0]))
token = Word(alphanums + "-./_:;*+=!<>@&`',?%#$\\")

simpleString = real | base64_ | raw | decimal | token | hexadecimal | qString











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
