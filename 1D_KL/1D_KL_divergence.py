# example of calculating the kl divergence between two mass functions
from math import log2
import numpy as np
 
# calculate the kl divergence
data = np.loadtxt('divergence.csv', delimiter=',')
p = data[:,0]
q = data[:,1]


def kl_divergence(p, q):
	return sum(p[i] * log2(p[i]/q[i]) for i in range(len(p)))
 
# define distributions
# p = [0.10, 0.40, 0.50]
# q = [0.80, 0.15, 0.05]
# calculate (P || Q)
kl_pq = kl_divergence(p, q)
print('KL(P || Q): %.3f bits' % kl_pq)
# calculate (Q || P)
kl_qp = kl_divergence(q, p)
print('KL(Q || P): %.3f bits' % kl_qp)