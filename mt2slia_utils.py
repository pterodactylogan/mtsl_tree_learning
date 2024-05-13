from nltk.tree import Tree
import re

'''
label: string node label
returns: list of features represented as strings. The last feature without
a + or - symbol is assumed to be the category feature. Others are assumed to be
selectors.
'''
def get_features_MGbank(label):
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

'''
label: string node label
returns: list of features represented as strings. The label is simply assumed
to be "exponent::f1:f2:f3..."
'''
def get_features(label):
    chunks = label.split(":")            
    return [c for c in chunks if c != ""]

'''
tree: input tree with node labels
returns: set of bigrams of the form "x.y" or "x/y", with the first representing
the immediate left sibling relation and the second representing immediate dominance.
The set contains all possible combinations of features that hold each relation in
the tree.
'''
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


def preceeds(addr1, addr2):
    i = 0
    while i<len(addr1) and i<len(addr2):
        if addr1[i] != addr2[i]:
            break
        else:
            i += 1
    if i == len(addr1) or i == len(addr2):
        return False
    
    if int(addr1[i]) < int(addr2[i]):
        return True
    return False


'''
addr1: gorn address of first node
addr2: gorn address of second node
rel: either "sib" or "dom". The relation 'interveningness' should be computed over
tree: the input tree to find interveners in
returns: set of all intervening symbols (features) between the two addresses
for the given relation
'''
def get_interveners(addr1, addr2, rel, tree):
    interveners = set()
    q = [("", tree)]
    if rel=="sib":
        i = 0
        while i<len(addr1) and i<len(addr2):
            if addr1[i] != addr2[i]:
                break
            else:
                i += 1
        if i == len(addr1) or i == len(addr2):
            return None
        prefix = addr1[:i]
        index = addr1[i]

        if int(addr2[i]) < int(index):
            return None
        
        while not q==[]:
            address, node = q.pop(0)
            
            # ignore nodes which do not share least common ancestor
            if address[:i] != prefix or address in [prefix, addr1, addr2]:
                for j in range(len(node)):
                    q.append((address + str(j), node[j]))
                continue

            # if ancestor of one of these nodes, it's an intervener
            if addr1[:len(address)] == address:
                interveners = interveners.union(set(get_features(node.label())))

            if addr2[:len(address)] == address:
                interveners = interveners.union(set(get_features(node.label())))

            if preceeds(address, addr2) and preceeds(addr1, address):
                interveners = interveners.union(set(get_features(node.label())))
                         
            for j in range(len(node)):
                q.append((address + str(j), node[j]))
                
        return frozenset(interveners)
            
                    
    if rel=="dom":
        # nodes do not stand in dominance relation
        if addr2[:len(addr1)] != addr1:
            return None
        
        gorn = addr1
        node = tree
        for char in gorn:
            node = node[int(char)]

        for char in addr2[len(addr1):-1]:
            node = node[int(char)]
            interveners = interveners.union(set(get_features(node.label())))

        return frozenset(interveners)

    return None

        
'''
bigram: bigram to search for intervener sets between
tree: tree to search over
returns: set of sets, each containing all symbols intervening between a single instance
of the specified bigram
'''
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

    intervener_sets = set()
    for addr0 in sig0_adds:
        for addr1 in sig1_adds:
            if dom:
                interveners =get_interveners(addr0,
                                                    addr1,
                                                    "dom", tree)
                if interveners != None:
                    intervener_sets.add(interveners)
            else:
                interveners =get_interveners(addr0,
                                                    addr1,
                                                    "sib", tree)
                if interveners != None:
                    intervener_sets.add(interveners)
    return intervener_sets