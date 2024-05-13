from mt2slia_utils import *
from nltk.tree import Tree

# Test get_interveners()
t1 = Tree.fromstring("(a (b (c) (d)) (e (f (h) (i)) (g)))")

print("expect {b}", get_interveners("", "01", "dom", t1))
print("expect {e, f}", get_interveners("", "100", "dom", t1))
print("expect {f}", get_interveners("1", "101", "dom", t1))

print("expect {b}", get_interveners("01", "1", "sib", t1))
print("expect {e, f, h, i}", get_interveners("0", "11", "sib", t1))
print("expect {b, d, e, f, h}", get_interveners("00", "101", "sib", t1))
print("expect {f, i}", get_interveners("100", "11", "sib", t1))

