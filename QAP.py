from docplex.mp.model import Model

from randomgen import QAP

n = 5
w, d = QAP(n, 141141)
print(w)
print(d)
m = Model(name='lewap')
x = []
for i in range(n):
    x.append([m.binary_var(name='x{0}y{1}'.format(i, j)) for j in range(n)])


# m.minimize(m.sum(x[i][j] * values[i][j] for i in range(n) for j in range(n)))
m.minimize(m.sum(m.sum(x[i][j] * d[i][j] * w[i][j] for i in range(n)) for j in range(n)))

for i in range(n):
    m.add_constraint(m.sum(x[i][j] for j in range(n)) == 1)

m.solve(log_output=True)
m.print_solution()