from randomgen import rosen
import random
import numpy as np

def rosenbrock(x):
    n = len(x)
    sum = 0
    for i in range(n-1):
        sum += 100 * (x[i+1]-x[i]**2)**2 + (1-x[i]**2) # nie wiem czy dobrze
    return sum

#PARAMETRY
# praticles_number  - liczba czastek
# W - kierunek (inertia coefficient),
# c1 - przyspieszenie osobiste (cognitive coefficient),
# c2 - przyspieszenie globalne (social coefficient)

W = 0.5
c1 = 0.8
c2 = 0.9
praticles_number = 30
max_iterations = 10

num_variables = 5
seed = 123123

class Particle():
    def __init__(self):
        self.position = np.array(rosen(num_variables, seed))
        self.pbest_position = self.position
        self.pbest_value = float('inf')
        self.velocity = np.array([0] * num_variables)

    def __str__(self):
        print("I am at ", self.position, ",my pbest is ", self.pbest_position)

    def move(self):
        self.position = self.position + self.velocity


class Space():

    def __init__(self, n_particles):
        self.n_particles = n_particles
        self.particles = []
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random() * 50] * num_variables) #byc moze do poprawy

    def print_particles(self):
        for particle in self.particles:
            particle.__str__()

    def fitness(self, particle):
        ret = 0
        for coordinate in particle.position:
            ret += coordinate ** 2
        return ret + 1

    def set_pbest(self):
        for particle in self.particles:
            fitness_cadidate = self.fitness(particle)
            if (particle.pbest_value > fitness_cadidate):
                particle.pbest_value = fitness_cadidate
                particle.pbest_position = particle.position

    def set_gbest(self):
        for particle in self.particles:
            best_fitness_cadidate = self.fitness(particle)
            if (self.gbest_value > best_fitness_cadidate):
                self.gbest_value = best_fitness_cadidate
                self.gbest_position = particle.position

    def move_particles(self):
        for particle in self.particles:
            global W
            new_velocity = (W * particle.velocity) + (c1 * random.random()) * (
                        particle.pbest_position - particle.position) + \
                           (random.random() * c2) * (self.gbest_position - particle.position)
            particle.velocity = new_velocity
            particle.move()

search_space = Space(n_particles=praticles_number)
particles_vector = [Particle() for _ in range(search_space.n_particles)]
search_space.particles = particles_vector
search_space.print_particles()

# iteration = 0
# while (iteration < max_iterations):
#     search_space.set_pbest()
#     search_space.set_gbest()
#     search_space.move_particles()
#     iteration += 1

for i in range(max_iterations):
    search_space.set_pbest()
    search_space.set_gbest()
    search_space.move_particles()


print("The best solution is: ", search_space.gbest_position)

particle_position_vector = np.array([np.array([(-1) ** (bool(random.getrandbits(1))) * random.random() * 50] * num_variables) for _ in
                                     range(praticles_number)]) # nie wiem czy tu nie powinien pobierac naszych wylosowanych danych

pbest_position = particle_position_vector
pbest_fitness_value = np.array([float('inf') for _ in range(praticles_number)])
gbest_fitness_value = float('inf')
gbest_position = np.array([float('inf')] * num_variables)

velocity_vector = ([np.array([0] * num_variables) for _ in range(praticles_number)])

for i in range(max_iterations):
    for i in range(praticles_number):
        fitness_cadidate = rosenbrock(particle_position_vector[i])
        print(fitness_cadidate, ' ', particle_position_vector[i])

        if (pbest_fitness_value[i] > fitness_cadidate):
            pbest_fitness_value[i] = fitness_cadidate
            pbest_position[i] = particle_position_vector[i]

        if (gbest_fitness_value > fitness_cadidate):
            gbest_fitness_value = fitness_cadidate
            gbest_position = particle_position_vector[i]

    for i in range(praticles_number):
        new_velocity = (W * velocity_vector[i]) + (c1 * random.random()) * (
                    pbest_position[i] - particle_position_vector[i]) + (c2 * random.random()) * (
                                   gbest_position - particle_position_vector[i])
        new_position = new_velocity + particle_position_vector[i]
        particle_position_vector[i] = new_position

print("Best x:", gbest_position, "| f(x)=", rosenbrock(gbest_position), "| iterations:", max_iterations)
