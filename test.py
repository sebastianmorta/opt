from docplex.mp.model import Model

n = 6
k = 4
m = Model(name='test')

x = []
for i in range(n):
    x.append([m.binary_var(name='x{0}{1}'.format(i, j)) for j in range(k)])

values = [
    [7, 2, 9, 3],
    [0, 6, 7, 1],
    [4, 1, 6, 3],
    [1, 4, 8, 5],
    [3, 3, 9, 8],
    [3, 2, 2, 2]
]

m.maximize(m.sum(x[i][j] * values[i][j] for i in range(n) for j in range(k)))

for i in range(n):
    m.add_constraint(m.sum(x[i][j] for j in range(k)) <= 1)

if __name__ == '__main__':
    m.solve(log_output=True)
    m.print_solution()
    print("pak pakeł")
