import cyk
import sys

def evaluate():
    sentenceFile = open('data/test_sentence')
    treeFile = open('data/test_trees')
    correct = 0
    incorrect = 0
    for table in cyk.cyk(sentenceFile):
        print ('TOP', ('S', table[-1][0]['S'][1]))
        cykTree = tree_to_string(('TOP', ('S', table[-1][0]['S'][1])))
        print cykTree
        print
        realTree = treeFile.readline()
        print realTree
        sys.exit(0)
        if cykTree == testTree:
            correct += 1
        else:
            incorrect += 1
    print 'correct: ' + str(correct)
    print 'incorrect: ' + str(incorrect)

def tree_to_string(tree):
    tree_str = '(' + str(tree[0])
    for child in tree[1:]:
        tree_str += ' ' + tree_to_string(child)
    return tree_str + ' )'

if __name__ == '__main__':
    evaluate()
