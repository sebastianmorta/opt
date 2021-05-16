from randomgen import rosen

def rosenbrock(x):
    n = len(x)
    sum = 0
    for i in range(n-1):
        sum += 100 * (x[i+1]-x[i]**2)**2 + (1-x[i]**2) # nie wiem czy dobrze
    return sum

print(rosenbrock(rosen(10, 123123)))

