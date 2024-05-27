import random
import MountainCarController as mc
import numpy as np

class Individual:
    def __init__ (self, steps=None, velocity=None, position=None, bitstring=None):
        self.bitstring = bitstring if bitstring is not None else [random.choice([0, 1]) for _ in range(32)] 
        self.steps = 1000
        self.velocity = velocity if velocity is not None else 0
        self.position = position if position is not None else -0.1
        self.evaluation = 0
    
    def mutate(self, mutation_rate):
        for i in range(len(self.bitstring)):
            if random.random() < mutation_rate:
                self.bitstring[i] = 1 if self.bitstring[i] == 0 else 0
    
    def eval(self):
        self.evaluation = 1 + self.position + self.velocity*4 + 1000 * 2.71828**(-0.03 * self.steps)

# Running the mc on the individual, setting the amount of steps it took to reach the goal
# 1000 steps if truncated (stopped), less if terminated (finished)
global best_individual_found
best_individual_found = Individual()
best_individual_found.steps = 1000
best_individual_found.velocity = 0
best_individual_found.position = -0.1

def evaluate(individual):
    global best_individual_found
    mc.lookup_list = individual.bitstring
    mc.render_mode = None
    mc.initialize()
    best_velocity = 0
    best_position = -0.1
    while not any([mc.iter_count > 1000*10, mc.terminated]):
        mc.update()

        observation = mc.observation[0]+0.5, mc.observation[1]
        if abs(observation[1]) > best_velocity:
            best_velocity = abs(observation[1])
        if observation[0] > best_position:
            best_position = observation[0]


    individual.steps = mc.iter_count // 10
    individual.velocity = best_velocity
    individual.position = best_position
    individual.eval()

    # print("Steps: ", (mc.iter_count // 5)+1, " Finished? ", mc.terminated, "Velocity: ", round(best_velocity, 4), " Position: ", round(best_position,4))

    if(individual.steps < best_individual_found.steps):
        best_individual_found = individual

    if(individual.steps < 199):
        print(f"Found solution: \nsteps: {individual.steps}, \nbitstring: {individual.bitstring} ")

# Selection of the mating pool, based on their fitness.
def selection(population, elite_size):
    selection_counter = 0
    total_fitness = sum([individual.evaluation for individual in population])

    random_number = random.uniform(0, total_fitness)

    running_total = 0
    selected_individuals = []

    population_copy: list = population

    while len(selected_individuals) < len(population)*elite_size:
        selection_counter += 1
        for individual in population_copy:
            running_total += individual.evaluation
            if running_total >= random_number:
                selected_individuals.append(individual)

                total_fitness -= individual.evaluation
                random_number = random.uniform(0, total_fitness)
                running_total = 0
                population_copy.remove(individual)
                if len(selected_individuals) >= len(population)*elite_size:
                    break

    return selected_individuals

def crossover(parent1, parent2):
    midpoint = (1 - (len(parent1.bitstring) -2)) / 2.0
    normal_num = np.random.normal(midpoint, 3)
    crossover_point = int(np.clip(round(normal_num), 1, len(parent1.bitstring) - 2))
    offspring1_bitstring = parent1.bitstring[:crossover_point] + parent2.bitstring[crossover_point:]
    offspring2_bitstring = parent2.bitstring[:crossover_point] + parent1.bitstring[crossover_point:]
    return Individual(bitstring=offspring1_bitstring), Individual(bitstring=offspring2_bitstring)

def clone(parent):
    return Individual(bitstring=parent.bitstring[:]), Individual(bitstring=parent.bitstring[:])

population_history = []
def main():
    population_size = 20
    generation_count = 300
    mutation_rate = 0.03
    elite_size = int(0.2 * population_size)

    population = [Individual() for _ in range(population_size)]

    for generation in range(generation_count):        
        print(f'Generation {generation + 1} of {generation_count}')

        for individual in population:
            evaluate(individual)

        population_history.append(population)

        mating_pool = selection(population, elite_size)
        
        next_generation = []
        generation_counter = 0
        while len(next_generation) < population_size:
            generation_counter += 1
            parent = random.sample(mating_pool, 1)[0]
            offspring1, offspring2 = clone(parent)
            offspring1.mutate(mutation_rate)
            offspring2.mutate(mutation_rate)
            next_generation.extend([offspring1, offspring2])
    
        population = next_generation
    
    else:
        for individual in population:
            evaluate(individual)

    #best_individual = max(population, key=lambda individual: individual.evaluation)
    best_individual = max([max(population, key=lambda individual: individual.evaluation) for population in population_history], key=lambda individual: individual.evaluation)
    print(best_individual.bitstring)
    print(best_individual.steps)
    print(best_individual.velocity)
    print(best_individual.position)
    print(best_individual.evaluation)

    for i in range(0, int(len(population_history)/10)):
        print("Generation ", i*10, " to ", i*10+10)

        total_velocity = 0
        total_position = 0
        for j in population_history[i*10:i*10+10]: 
            for ind in j:
                total_velocity += ind.velocity
                total_position += ind.position

        total_velocity /= population_size*10
        total_position /= population_size*10

        print("Average velocity: ", round(total_velocity, 4))
        print("Average position: ", round(total_position, 4))
        print()

main()