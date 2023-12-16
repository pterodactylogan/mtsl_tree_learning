from nltk.tree import Tree
import re

f = open("./dep-trees-json/autos/00/wsj_0002.json", "r")
t = f.read()
t = t.strip("[]\"")

sentence = Tree.fromstring(t)
sentence.draw()


def get_features(label):
    chunks = label.split("::")
    features = re.split('=|_', chunks[1])
    #drop empty strings
    features = list(filter(None, features))
    found_cat = False
    for i in range(len(features)-1, -1, -1):
        if features[i][0] != '+' and features[i][0] != '-':
            if not found_cat:
                found_cat = True
                features[i] = "-" + features[i]
            else:
                features[i] = "+" + features[i]
            
    return features

def get_bigrams(tree):
    bigrams = set()
    root_features = get_features(tree.label())
    last_child_feats = []

    for child in tree:
        child_feats = get_features(child.label())

        for rfeat in root_features:
            for cfeat in child_feats:
                bigrams.add(rfeat + "/" + cfeat)

        for lfeat in last_child_feats:
            for cfeat in child_feats:
                bigrams.add(lfeat + "." + cfeat)

        last_child_feats = child_feats

    for child in tree:
        bigrams = bigrams.union(get_bigrams(child))

    return bigrams

def get_interveners(addr1, addr2, rel, tree):
    interveners = set()
    q = [("", tree)]
    if rel=="sib":
        while not q==[]:
            address, node = q.pop(0)
            
            
            

def get_2paths(bigram, tree):
    dom = False
    if "/" in bigram:
        dom = True

    if dom:
        symbols = bigram.split("/")
    else:
        symbols = bigram.split(".")

    q = [("", tree)]
    sig0_adds = []
    sig1_adds = []
    while not q == []:
        address, node = q.pop(0)
        feats = get_features(node.label())
        if symbols[0] in feats:
            sig0_adds.append(address)
        if symbols[1] in feats:
            sig1_adds.append(address)

        for i in range(len(node)):
            q.append((address + str(i), node[i]))

    print(sig0_adds)
    print(sig1_adds)
        

get_2paths("+case.-case", sentence)

f.close()
