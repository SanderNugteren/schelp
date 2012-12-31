import cyk
from parse import traverse
import tree_parser
import sys

def evaluate():
    sentenceFile = open('data/test_sentence')
    treeFile = open('data/test_trees')
    correct = 0
    incorrect = 0
    for table in cyk.cyk(sentenceFile):
        cykTree = ('TOP', ('S', table[-1][0]['S'][1], table[-1][0]['S'][2]))
        print cykTree
        print
        realTree = tree_parser.get_tree(treeFile.readline())
        print realTree
        #TODO use traverse here
        match = True
        r_traverse = traverse(realTree)
        for c in traverse(cykTree):
            r = r_traverse.next()
            print str(c) + ' a match for ' + str(r)
            if c != r:
                print 'no match'
                match = False
                break
        if match:
            correct += 1
        else:
            incorrect += 1
        sys.exit(0)
    print 'correct: ' + str(correct)
    print 'incorrect: ' + str(incorrect)

if __name__ == '__main__':
    evaluate()
