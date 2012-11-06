import sys
from freqs import frequencies
from reverse import reverse

def main():
    f = open('data/test_sentence')
    for line in f:
        words = line.strip().split(" ")
        table = [[[]] * i for i in xrange(1, len(words) + 1)]
        for i,j in table_traverse(len(words)):
            if i == j:
                table[i][j] = reverse[word[i]]
                new_keys = []
                keys_added = True
                while keys_added:
                    keys_added = False
                    for rule in table[i][j]:
                        for key in rule.iterkeys():
                            new_keys.append(key)
                            keys_added = True
            else:
                pass
        sys.exit(0)

def table_traverse(table_length)
        for i in xrange(table_length):
            for j in xrange(table_length - i):
                yield j, i+j

if __name__ == '__main__':
    main()
