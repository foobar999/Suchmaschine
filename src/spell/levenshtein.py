import numpy as np



def levenshtein_superslow(a, b):
    if not a: return len(b)
    if not b: return len(a)
    return min(levenshtein_superslow(a[1:], b[1:])+(a[0] != b[0]), levenshtein_superslow(a[1:], b)+1, levenshtein_superslow(a, b[1:])+1)



# src?
def levenshtein_numpy(source, target):
    if len(source) < len(target):
        return levenshtein_numpy(target, source)

    if len(target) == 0:
        return len(source)

    source = np.array(tuple(source))
    target = np.array(tuple(target))

    previous_row = np.arange(target.size + 1)
    for s in source:
        current_row = previous_row + 1

        current_row[1:] = np.minimum(
                current_row[1:],
                np.add(previous_row[:-1], target != s))

        current_row[1:] = np.minimum(
                current_row[1:],
                current_row[0:-1] + 1)

        previous_row = current_row

    return previous_row[-1]



# Christopher P. Matthews
# christophermatthews1985@gmail.com
# Sacramento, CA, USA
def levenshtein_wiki(s, t):
    ''' From Wikipedia article; Iterative with two matrix rows. '''
    if s == t: return 0
    elif len(s) == 0: return len(t)
    elif len(t) == 0: return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
            
    return v1[len(t)]


def levenshtein_mat(s, t):
    m, n = len(s), len(t)
    D = np.empty((m+1, n+1), dtype=np.int)
    #print(D)
    #for i in range(0, m+1):
    #    D[i,0] = i
    #for j in range(0, n+1):
    #    D[0,j] = j
    D[:,0] = range(0, m+1)
    D[0,:] = range(0, n+1)
        
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s[i-1] == t[j-1] else 1
            D[i,j] = min(D[i-1,j]+1, D[i,j-1]+1, D[i-1,j-1]+cost)
        
    return D[m,n]
        
    


# https://pypi.python.org/pypi/python-Levenshtein/0.12.0
# :?