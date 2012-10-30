#!/usr/bin/env python2
from pyparsing import *

sample = "(TOP (S (NP (DT A) (NP@ (NN record) (NN date))) (S@ (VP (VBZ has) (VP@ (RB n't) (VP (VBN been) (VP (VBN set))))) (. .))) )"

enclosed = Forward()
nestedParens = nestedExpr('(', ')', content=enclosed)
enclosed << (Word(alphas+"@"+"'"+".") | nestedParens)

print enclosed.parseString(sample).asList()
