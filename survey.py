from docplex.mp.model import Model
from randomgen import survey, hex_code_colors
import matplotlib.pyplot as plt

n = 50

values = survey(n=n, seed=111111)

print(values)
start_point = [values[-2], values[-1]]

m = Model(name='ins_model')

x = []
x.append([m.continuous_var(lb=start_point[0], ub=start_point[0], name='x{0}'.format(0)),
          m.continuous_var(lb=start_point[1], ub=start_point[1], name='y{0}'.format(0))])
for i in range(1, n + 1):
    x.append([m.continuous_var(name='x{0}'.format(i)),
              m.continuous_var(name='y{0}'.format(i))])
x.append([m.continuous_var(lb=start_point[0], ub=start_point[0], name='x{0}'.format(n + 1)),
          m.continuous_var(lb=start_point[1], ub=start_point[1], name='y{0}'.format(n + 1))])

m.minimize(m.sum(m.abs(x[i - 1][0] - x[i][0]) + m.abs(x[i - 1][1] - x[i][1]) for i in range(1, n + 1)))

for i in range(1, n + 1):
    m.add_constraint(m.sum(m.abs(x[i][0] - values[0][i - 1]) + m.abs(x[i][1] - values[1][i - 1]) <= values[2][i - 1]))
m.solve(log_output=False)
m.print_solution()
s = m.solve().to_string().split()[5:]


print("xhv")
# s = [[float(i[0][3:]), float(i[1][3:])] for i in zip(s[::2], s[1::2])]
# print(s)
s = [[float(i[0][3:]) if i[0][2] == '='else float(i[0][4:]), float(i[1][3:])if i[1][2] == '='else float(i[1][4:])] for i in zip(s[::2], s[1::2])]
print(s)
fig, ax = plt.subplots()
for i in range(n + 1):
    ax.scatter(s[i][0], s[i][1])
    ax.annotate(i, (s[i][0], s[i][1]))
    ax.annotate("", xy=(s[i + 1][0], s[i + 1][1]), xytext=(s[i][0], s[i][1]),
                arrowprops=dict(arrowstyle="simple", connectionstyle="arc3"), )
for i in range(n):
    ax.add_patch(plt.Circle((values[0][i], values[1][i]), values[2][i], color=hex_code_colors(), alpha=0.5))

ax.set_aspect('equal', adjustable='datalim')
ax.plot()  # Causes an autoscale update.
plt.show()
