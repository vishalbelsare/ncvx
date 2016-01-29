from cvxpy import *
from ncvx import *
import numpy as np

# Feature selection on a linear kernel SVM classifier.
# Uses the Alternating Direction Method of Multipliers
# with a (non-convex) cardinality constraint.

# Generate data.
np.random.seed(1)
N = 50
M = 40
n = 10
data = []
for i in xrange(N):
    data += [(1, np.random.normal(1.0, 2.0, (n, 1)))]
for i in xrange(M):
    data += [(-1, np.random.normal(-1.0, 2.0, (n, 1)))]

# Construct problem.
gamma = Parameter(sign="positive")
gamma.value = 0.1
# 'a' is a variable constrained to have at most 6 non-zero entries.
a = Card(n, k=6)
b = Variable()

slack = [pos(1 - label*(sample.T*a - b)) for (label, sample) in data]
objective = Minimize(norm(a, 2) + gamma*sum(slack))
p = Problem(objective)
# Extensions can attach new solve methods to the CVXPY Problem class.
p.solve(method="NC-ADMM", max_iter=50, rho=[5])
# p.solve(method="repeated_rr")
# p.solve(method="relax_and_round")

# Count misclassifications.
error = 0
for label, sample in data:
    if not label*(a.value.T*sample - b.value)[0] >= 0:
        error += 1

print "%s misclassifications" % error
print a.value
print b.value
