from mt2slia_utils import *
from nltk.tree import Tree

t1 = Tree.fromstring("(a (b (c) (d)) (e (f (h) (i)) (g)))")

# Test get_interveners()
# print("expect {b}", get_interveners("", "01", "dom", t1))
# print("expect {e, f}", get_interveners("", "100", "dom", t1))
# print("expect {f}", get_interveners("1", "101", "dom", t1))

# print("expect {b}", get_interveners("01", "1", "sib", t1))
# print("expect {e, f, h, i}", get_interveners("0", "11", "sib", t1))
# print("expect {b, d, e, f, h}", get_interveners("00", "101", "sib", t1))
# print("expect {f, i}", get_interveners("100", "11", "sib", t1))

# # test add_boundaries()
# print(add_boundaries(t1))

# test get_2paths()
t2 = Tree.fromstring("(# (a #) (b #))")
t3 = Tree.fromstring("(a (b (c) (a)) (c (b (a) (c)) (a)))")
print("expect {}", get_2paths("#/b", t2))
print("expect {}", get_2paths("a.b", t2))
print("expect {{}, {b}, {c,b}}", get_2paths("a/c", t3))
print("expect {{}, {c,b}, {a,c,b}}", get_2paths("b.a", t3))

print("expect {}", get_2paths("b/b", t3))

t4 = Tree.fromstring("(<# (C:wh+ (nom-:D #>) (C (nom-:D #>) (C (nom-:D #>) (wh-:D #>)))))")
print(get_2paths("nom-:D.nom-:D", t4))