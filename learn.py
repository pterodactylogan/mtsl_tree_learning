from nltk.tree import Tree
import os
import json
from mt2slia_utils import *

# TODO: Think about represenations / efficiency

path = os.path.dirname(os.path.realpath(__file__))

directory = path + "/trees"
file = "that_trace2.json"

params = {"split_feats": False}

trees = []
for filename in os.listdir(directory):
    if filename[-5:] == ".json" and (file == "" or file == filename):
        name = os.path.join(directory, filename)
        f = open(name, "r")
        treestrings = json.loads(f.read())
        for s in treestrings:
            trees.append(Tree.fromstring(s))
        f.close()

bigrams = set()
for tree in trees:
    bigrams = bigrams.union(get_bigrams(tree, params["split_feats"]))

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
        if symb1 != "#>" and symb2 != "<#":
            possible_bigrams.add(symb1 + "/" + symb2)
        if symb1 not in ["<#", "#>"] and symb2 not in ["<#", "#>"]:
            possible_bigrams.add(symb1 + "." + symb2)

unattested = possible_bigrams.difference(bigrams)

constraints = {}
for bigram in unattested:
    if "/" in bigram:
        symbols = bigram.split("/")
    else:
        symbols = bigram.split(".")
    # initialize tier to bigram symbols
    tier = {s for s in symbols}
    # find all intervener sets for the bigram
    intervener_sets = set()
    for tree in trees:
        intervener_sets = intervener_sets.union(get_2paths(bigram, tree, params["split_feats"]))

    # find the highest cardinality of intervener set
    max_c = 0
    for s in intervener_sets:
        if len(s) > max_c:
            max_c = len(s)
    for i in range(max_c+1):
        to_add = set()
        for s in intervener_sets:
            if len(s) == i and len(s.intersection(tier)) == 0:
                to_add = to_add.union(s)
        tier = tier.union(to_add)

    tier = frozenset(tier)
    if tier in constraints:
        constraints[tier].append(bigram)
    else:
        constraints[tier] = [bigram]

for c in constraints:
    print(c, constraints[c])
    print()

test_file = open(path + "/trees/illicit_simple.json")

test_trees = []
treestrings = json.loads(test_file.read())
for s in treestrings:
    test_trees.append(Tree.fromstring(s))
test_file.close()


obeyed = 0
disobeyed = 0

for tree in test_trees:
    violated = False
    for t in constraints:
        if violated:
            break
        for c in constraints[t]:
            if violates(tree, c, t, params):
                disobeyed += 1
                violated = True
                break

    if not violated:
        obeyed += 1

print(obeyed, disobeyed)
            



    
