import sys
from itertools import combinations
from freqs import frequencies
from reverse import reverse

def main():
    f = open('data/test_sentence')
    for line in f:
        words = line.strip().split(" ")
        table = [[set()] * i for i in xrange(1, len(words) + 1)]
        for i, j in table_traverse(len(words)):
            if i == j:
                table[i][j] = set(reverse[(words[i],)])
                new_keys = set()
                keys_added = True
                while keys_added:
                    keys_added = False
                    for rule in table[i][j]:
                        if rule in reverse:
                            for key in reverse[rule]:
                                new_keys |= key
                                keys_added = True
            else:
                left = set(table[j-1][i])
                down = set(table[j][i+1])
                for l in left:
                    for d in down:
                        if (l, d) in reverse:
                            table[j][i] |= set(reverse[(l, d)])
        print table
        sys.exit(0)

def table_traverse(table_length):
        for i in xrange(table_length):
            for j in xrange(table_length - i):
                yield j, i+j

if __name__ == '__main__':
    main()
