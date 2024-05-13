from nltk.tree import Tree
import os
from mt2slia_utils import *

# TODO: Think about represenations / efficiency

path = os.path.dirname(os.path.realpath(__file__))

directory = path + "/trees"
file = "comp_agreement.json"

trees = []
for filename in os.listdir(directory):
    print(filename)
    if filename[-5:] == ".json" and (file == "" or file == filename):
        name = os.path.join(directory, filename)
        f = open(name, "r")
        treestrings = f.read().strip("[]").split(",")
        for s in treestrings:
            trees.append(Tree.fromstring(s.strip("\"\n ")))
        f.close()

bigrams = set()
for tree in trees:
    bigrams = bigrams.union(get_bigrams(tree))

alphabet = set()
for bigram in bigrams:
    if "/" in bigram:
        symbols = bigram.split("/")
    else:
        symbols = bigram.split(".")
    alphabet.add(symbols[0])
    alphabet.add(symbols[1])

possible_bigrams = set()
for symb1 in alphabet:
    for symb2 in alphabet:
        possible_bigrams.add(symb1 + "/" + symb2)
        possible_bigrams.add(symb1 + "." + symb2)

unattested = possible_bigrams.difference(bigrams)

constraints = {}
for bigram in unattested:
    print(bigram)
    if "/" in bigram:
        symbols = bigram.split("/")
    else:
        symbols = bigram.split(".")
    # initialize tier to bigram symbols
    tier = {s for s in symbols}
    # find all intervener sets for the bigram
    intervener_sets = set()
    for tree in trees:
        intervener_sets = intervener_sets.union(get_2paths(bigram, tree))

    # find the highest cardinality of intervener set
    max_c = 0
    for s in intervener_sets:
        if len(s) > max_c:
            max_c = len(s)
    for i in range(max_c+1):
        to_add = set()
        for s in intervener_sets:
            print(s)
            if len(s) == i and len(s.intersection(tier)) == 0:
                print("adding", s)
                to_add = to_add.union(s)
        tier = tier.union(to_add)

    tier = frozenset(tier)
    if tier in constraints:
        constraints[tier].append(bigram)
    else:
        constraints[tier] = [bigram]

print(constraints)

# TODO: implement tier projection and TSL child string language learning

# test_directory = "./dep-trees-json/autos/01"

# test_trees = []
# for filename in os.listdir(directory):
#     if filename[-5:] == ".json":
#         name = os.path.join(directory, filename)
#         f = open(name, "r")
#         treestrings = f.read().strip("[]").split(",")
#         for s in treestrings:
#             test_trees.append(Tree.fromstring(s.strip("\" ")))
#         f.close()


# obeyed = 0
# disobeyed = 0
# for tier in constraints:
#     for con in constraints[tier]:
#         intervener_sets = set()
#         for tree in test_trees:
#             intervener_sets = intervener_sets.union(get_2paths(bigram, tree))
#         fine = True
#         for path in intervener_sets:
#             if path.intersection(tier) == frozenset():
#                 fine = False
#                 break
#         if fine:
#             obeyed +=1
#         else:
#             disobeyed +=1

#         if (obeyed+disobeyed)%100 == 0:
#             print(obeyed, disobeyed)
            



    
