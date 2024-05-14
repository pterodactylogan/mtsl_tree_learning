from nltk.tree import Tree
import os
import argparse
import json

'''
return a list of trees corresponding to the simplified version
'''
def simplify(tree, feats):
    if type(tree) is str:
        label = tree
    else:
        label = tree.label()

    chunks = label.split("::")
    phon = chunks[0]
    label = ""
    if phon in feats:
        label = phon
    
    label += "::"
    for f in chunks[1].split(":"):
        if f in feats:
            if label[-2:] == "::":
                label += ":"
            label += f

    if type(tree) is str and label != "::":
        return [Tree(label, ["#>"])]

    if label == "::":
        if type(tree) is str:
            return []
        else:
            children = []
            for t in tree:
                children += simplify(t, feats)
            return children
    
    children = []
    for t in tree:
        children += simplify(t, feats)

    if children == []:
        return [Tree(label, ["#>"])]
    return [Tree(label, children)]
    

'''
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw trees from a file or directory")
    parser.add_argument("MG_file", type=str, default="", help="The file containing list of MG grammar tree strings")
    parser.add_argument("-o", "--outfile", type=str, default = "", help="The file to write simplified trees to")
    parser.add_argument("-f", "--feats", type=str, default = "[]", help="The features to keep in the simplified trees")
    args = parser.parse_args()

    infile = open(args.MG_file, "r")
    outfile = open(args.outfile, "w")

    treestrings = json.loads(infile.read())
    outtrees = []
    for s in treestrings:
        oldtree = Tree.fromstring(s.strip("\"\n"))
        print(oldtree)
        newtree = simplify(oldtree, json.loads(args.feats))
        newtree = [Tree("<#", newtree)]
        outtrees.append(str(newtree[0]))
    
    outfile.write(json.dumps(outtrees))
        
    infile.close()
    outfile.close()