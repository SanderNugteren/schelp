import cyk
from parse import traverse
import tree_parser
import sys

def evaluate():
    sentenceFile = open('data/test_sentence')
    treeFile = open('data/test_trees')
    correct = 0
    incorrect = 0
    for cykTree in cyk.cyk(sentenceFile):
        print cykTree
        realTree = tree_parser.get_tree(treeFile.readline())
        #TODO use traverse here
        match = True
        r_traverse = traverse(realTree)
        for c in traverse(cykTree):
            r = r_traverse.next()
            if len(c) != len(r):
                match = False
                break
        if match:
            correct += 1
            print 1
        else:
            incorrect += 1
            print 0
    print 'correct: ' + str(correct)
    print 'incorrect: ' + str(incorrect)

if __name__ == '__main__':
    evaluate()
