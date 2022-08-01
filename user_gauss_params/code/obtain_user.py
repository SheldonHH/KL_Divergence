from functools import reduce
sg = "user_3_2519_gauss.json"
def findNth(a, b, n):
    return reduce(lambda x, y: -1 if y > x + 1 else a.find(b, x + 1), range(n), -1)

print(sg[0:findNth(sg, "_", 2)])