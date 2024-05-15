This README describes how to use the following three files:

	- learn.py: This program executes the MT2SLIA on a provided sample of positive data
	
	- simplify_tree.py: This program converts MG-formatted trees into a simplified representation based on the features provided
	
	- view_trees.py: This program allows you to view a graphical representation of all trees in a file or directory
	
Prerequisites:
you must have python3 with nltk installed on your machine.
	- python: https://www.python.org/downloads/
	- nltk: https://www.nltk.org/install.html
	
learn.py:

to run the algorithm on an input data file use:

`python3 learn.py filename`

The file must contain a json-formatted list of nltk tree strings. 

You can also evaluate the learned grammar's behavior on a test file as follows:

`python3 learn.py learningfile -e testfile`

The program will print the number of test trees which were accepted and rejected by the grammar.

simplify_tree.py:

to convert a file of MG-formatted tree strings (also in json-format list) to a simplified format use:

`python3 simplify_tree.py mgtreefile -o outputfile -f '["feature1","feature2","feature3", ...]'`

The program will write the resulting simplified trees to the specified output file.

view_trees.py

to view all the trees in a directory use:

`python3 view_trees.py dirpath/`

This will visualize all the trees from all json files in that directory in a single canvas. The trees can be dragged around the screen, and there is a zoom option to enlarge them (this will undo any dragging).

to view all the trees in a single file use:

`python3 view_trees.py dirpath/ -f filename`
