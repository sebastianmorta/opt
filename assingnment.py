from docplex.mp.model import Model

from randomgen import assignment

n = 4
m = Model(name='lewap')
values = assignment(n, 123123)
print(values)

x = []
for i in range(n):
    x.append([m.binary_var(name='x{0}{1}'.format(i, j)) for j in range(n)])
m.minimize(m.sum(x[i][j] * values[i][j] for i in range(n) for j in range(n)))

for i in range(n):
    m.add_constraint(m.sum(x[i][j] for j in range(n)) == 1)

m.solve(log_output=True)
m.print_solution()