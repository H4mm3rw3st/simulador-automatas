from itertools import product

def subcadenas(c):
    return sorted({c[i:j] for i in range(len(c)) for j in range(i+1, len(c)+1)})

def prefijos(c):
    return sorted({c[:i] for i in range(len(c)+1)})

def sufijos(c):
    return sorted({c[i:] for i in range(len(c)+1)})

def kleene(alfabeto, n=3):
    res = [""]
    for i in range(1, n+1):
        for p in product(alfabeto, repeat=i):
            res.append("".join(p))
    return res