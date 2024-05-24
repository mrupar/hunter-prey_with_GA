import random

class Buki:
    def __init__(self, energy, speed):
        self.energy = energy
        self.speed = speed

    def fitness(self):
        return (self.energy - self.speed)

class Kiki(Buki):
    def __init__(self, energy, speed, attack):
        super().__init__(energy, speed)
        self.attack = attack

    def __str__(self):
        return f"Kiki | Fitness: {self.fitness()} | Energy: {self.energy} | Speed: {self.speed} | Attack: {self.attack}"

    def fitness(self, add=0):
        return super().fitness() + add

class Buba(Buki):
    def __init__(self, energy, speed, defense):
        super().__init__(energy, speed)
        self.defense = defense

    def __str__(self):
        return f"Buba | Fitness: {self.fitness()} | Energy: {self.energy} | Speed: {self.speed}| Defense: {self.defense}"

    def fitness(self, add=0):
        return super().fitness() + add

def create_population(size):
    kiki_population = []
    buba_population = []
    for _ in range(size):
        energy = random.randint(0,100)
        speed = random.randint(0,20)
        if random.random() > 0.5: 
            attack = random.randint(0,10)
            kiki = Kiki(energy=energy, speed=speed, attack=attack)
            kiki_population.append(kiki)
        else: 
            defense = random.randint(0,10)
            buba = Buba(energy=energy, speed=speed, defense=defense)
            buba_population.append(buba)
    return {"kiki": kiki_population, "buba": buba_population}

def crossover(parent1, parent2):
    if isinstance(parent1, Kiki) and isinstance(parent2, Kiki):
        child = Kiki(
            (parent1.energy + parent2.energy) / 2,
            (parent1.speed + parent2.speed) / 2, 
            (parent1.attack + parent2.attack) / 2
        )
    elif isinstance(parent1, Buba) and isinstance(parent2, Buba):
        child = Buba(
            (parent1.energy + parent2.energy) / 2,
            (parent1.speed + parent2.speed) / 2, 
            (parent1.defense + parent2.defense) / 2
        )
    else:
        raise ValueError("ERROR in crossover")
    return child

def mutate(buki, mutation_rate):
    if random.random() < mutation_rate:
        buki.energy = random.randint(0, 100)
    if random.random() < mutation_rate:
        buki.speed = random.randint(0, 20)
    if isinstance(buki, Kiki) and random.random() < mutation_rate:
        buki.attack = random.uniform(0, 100)
    if isinstance(buki, Buba) and random.random() < mutation_rate:
        buki.defense = random.uniform(0, 100)

def tournament_selection(population, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, tournament_size)
        winner = max(tournament, key=lambda individual: individual.fitness())
        selected.append(winner)
    return selected

def hunt(kiki, buba):
    if int(kiki.attack) > int(buba.defense):
        buba.energy -= kiki.attack 
        kiki.fitness(100)
        buba.fitness(-50) 
        if buba.energy < 20:
            del buba
    elif int(kiki.attack) < int(buba.defense):
        kiki.energy -= buba.defense
        buba.fitness(100)
        kiki.fitness(-50)   
        if kiki.energy < 20:
            del kiki
    else:
        kiki.energy -= 10
        buba.energy -= 10


def run_genetic_algorithm(population_size, generations, mutation_rate):
    population = create_population(population_size)
    kiki_population = population["kiki"]
    buba_population = population["buba"]

    kiki_selected = tournament_selection(kiki_population)
    buba_selected = tournament_selection(buba_population)
    
    for generation in range(generations):
        for kiki in kiki_selected:
            buba = random.choice(buba_population)
            if kiki.speed > buba.speed:
                hunt(kiki, buba)
            else:
                buba.fitness(50)
                kiki.fitness(-50)

        new_kiki_population = []
        new_buba_population = []
        
        for i in range(0, len(kiki_selected), 2):
            if i + 1 < len(kiki_selected):
                parent1 = kiki_selected[i]
                parent2 = kiki_selected[i + 1]
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
                new_kiki_population.append(child1)
                new_kiki_population.append(child2)
        
        for i in range(0, len(buba_selected), 2):
            if i + 1 < len(buba_selected):
                parent1 = buba_selected[i]
                parent2 = buba_selected[i + 1]
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
                new_buba_population.append(child1)
                new_buba_population.append(child2)
        
        for individual in new_kiki_population:
            mutate(individual, mutation_rate)
        for individual in new_buba_population:
            mutate(individual, mutation_rate)
        
        kiki_fitness_values = [individual.fitness() for individual in new_kiki_population]
        buba_fitness_values = [individual.fitness() for individual in new_buba_population]
        print(f"Generation {generation}, Best Kiki Fitness: {max(kiki_fitness_values)}, Best Buba Fitness: {max(buba_fitness_values)}")
        
        # Replace old population with new population
        kiki_population = new_kiki_population
        buba_population = new_buba_population
    
    return {"kiki": kiki_population, "buba": buba_population}

# Run the genetic algorithm
final_population = run_genetic_algorithm(population_size=1000, generations=50000, mutation_rate=0.1)
best_kiki = max(final_population["kiki"], key=lambda individual: individual.fitness())
best_buba = max(final_population["buba"], key=lambda individual: individual.fitness())
print(f"Best Kiki: {best_kiki}")
print(f"Best Buba: {best_buba}")
