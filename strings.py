from collections import Counter

# [(abc)|(ebd)]*
words = ["abc",
        "abcebd",
        "abcabcebd",
        "ebdabc",
        "ebdebdebdabcabcabc",
        "ebdabcebdabcebdabcebdebd"
]

# symbol: {symbol: set(paths)}
paths = {}
alphabet = set()

for word in words:
    for i in range(len(word)-1):
        alphabet.add(word[i])
        if word[i] not in paths:
            paths[word[i]] = {}
        if word[i+1] not in paths[word[i]]:
            paths[word[i]][word[i+1]] = set([""])
    alphabet.add(word[-1])

forbidden = set()

print(paths)
print(alphabet)

# compute paths from s1 to s2 such that:
# 1. the path can be constructed from licit bigrams
# 2. the path does not contain s1 or s2
# 3. the path does not contain the same bigram more than once
for i in range(len(alphabet)):
    for s1 in alphabet:
        for s2 in alphabet:
            # add pair to forbidden set if not initialized with empty path
            if (s1 not in paths) or (s2 not in paths[s1]) or ("" not in paths[s1][s2]):
                forbidden.add((s1, s2))
            elif s2 not in paths:
                    continue
            else:
                for p1 in paths[s1][s2]:
                    for s3 in paths[s2]:
                        # to debug: not computing paths with repeated letters
                        # eg a->d should include bceb, generated
                        # by s1=a, s2 = e, s3=d
                        if s1 == 'a' and s3 == 'd':
                            print("a -> d")
                        # already have s1->s2
                        if s3 == s2:
                            continue
                        if s3 not in paths[s1]:
                            paths[s1][s3] = set()
                        # pths = frozenset(paths[s2][s3])
                        for p2 in paths[s2][s3]:
                            if s1 == 'a' and s3 == 'd':
                                print(s2, p2)
                            if s3 in p1 or s3 in p2:
                                continue
                            if s1 in p1 or s1 in p2:
                                continue
                            path = p1+s2+p2
                            if len(path) < 2:
                                paths[s1][s3].add(path)
                                continue
                            bigrams = Counter(path[idx : idx + 2] for idx in range(len(path) - 1))
                            if bigrams.most_common(1)[0][1] > 1:
                                continue
                            paths[s1][s3].add(path)



# compute paths from s1 to s2 such that:
# 1. the path can be constructed from licit bigrams
# 2. the path does not contain s1 or s2
# 3. the path does not contain the same bigram more than once

print("RESULTS")
for pair in forbidden:
    print(pair)
    if pair[0] in paths and pair[1] in paths[pair[0]]:
        print(paths[pair[0]][pair[1]])
    print()
