from nltk.tree import Tree
import os
from nltk.draw.tree import draw_trees
import argparse
import json

'''
Visualizes trees from a file or directory. If no filename is given,
all .json files in the specified directory will be used. Otherwise, only
trees from the specified file will be visualized.

Usage: python3 view_trees.py directory [-f file]
'''
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw trees from a file or directory")
    parser.add_argument("directory", type=str, default="", help="The directory containing the trees")
    parser.add_argument("-f", "--file", type=str, default = "", help="The file containing the trees")
    args = parser.parse_args()

    directory = args.directory
    file = args.file
    trees = []
    for filename in os.listdir(directory):
        if filename[-5:] == ".json" and (file == "" or file == filename):
            name = os.path.join(directory, filename)
            f = open(name, "r")
            treestrings = json.loads(f.read())
            for s in treestrings:
                trees.append(Tree.fromstring(s))
            f.close()

    draw_trees(*trees)