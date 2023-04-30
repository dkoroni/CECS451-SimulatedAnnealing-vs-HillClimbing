import random
import math
import time
import matplotlib.pyplot as plt
import os

clear = lambda: os.system('cls')

# The distance between cities
def distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)

# The cost of a tour
def tour_cost(tour):
    return sum(distance(tour[i], tour[i+1]) for i in range(len(tour)-1)) + distance(tour[-1], tour[0])

# A general print function for the algorithms
def format_print(algorithm, city_length, iteration, time_taken, current_tour_cost):
    clear()
    print(f'{algorithm}: \n\tCities {city_length} \n\tIteration {iteration} \n\tTime: {time_taken:.3f} \n\tCurrent tour cost: {current_tour_cost}')

# The Hill Climbing Algorithm
def hill_climb(cities, run_time, update_fn=None):
    global time_taken
    # Generate a random tour
    current_tour = random.sample(cities, len(cities))
    # Loop through for a specific amount of time
    start_time = time.time()
    
    i = 0
    format_print("Hill Climbing", len(cities), i, 0, tour_cost(current_tour))
    while True:
        # Create a list of neighboring tours
        neighbors = []
        for j in range(len(cities)):
            for k in range(j+1, len(cities)):
                neighbor = current_tour.copy()
                neighbor[j], neighbor[k] = neighbor[k], neighbor[j]
                neighbors.append(neighbor)
        last_tour_cost = tour_cost(current_tour)
        # Evaluate the neighbors and select the best one
        best_neighbor = min(neighbors, key=lambda x: tour_cost(x))
        if tour_cost(best_neighbor) < tour_cost(current_tour):
            current_tour = best_neighbor
        
        # Update callback function with current tour parameter 
        if update_fn:
            update_fn(current_tour)
        
        i += 1
        end_time = time.time()
        time_taken = end_time - start_time
        format_print("Hill Climbing", len(cities), i, time_taken, tour_cost(current_tour))
        
        # Hill climbing is prone to getting stuck in local minima
        # We end the loop early to save time in these cases
        if last_tour_cost == tour_cost(current_tour):
            break

        # Breaks the infinite loop after a certain amount of time
        if end_time - start_time > run_time:
            break
    return current_tour

# The Simulated Annealing algorithm
def simulated_annealing(cities, run_time, temperature, cool, update_fn=None):
    global time_taken
    # Generate a random tour
    current_tour = random.sample(cities, len(cities))
    # Loop through for a specific amount of time
    start_time = time.time()

    i = 0
    format_print("Simulated Annealing", len(cities), i, 0, tour_cost(current_tour))
    while temperature > 1:
        # Create a neighbor tour by swapping two cities
        neighbor = current_tour.copy()
        j, k = random.sample(range(len(cities)), 2)
        neighbor[j], neighbor[k] = neighbor[k], neighbor[j]
        # Calculate the cost of the current and neighbor tours
        current_cost = tour_cost(current_tour)
        neighbor_cost = tour_cost(neighbor)
        
        # Decrease the temperature to lower risk of next iteration
        temperature *= cool
        # Determine whether to accept the neighbor tour
        cost = neighbor_cost - current_cost
        probability = math.exp(cost*-1 / temperature)
        if neighbor_cost < current_cost or probability > random.uniform(0, 1):
            current_tour = neighbor
        
        # Update callback function with current tour parameter 
        if update_fn:
            update_fn(current_tour)
        
        i += 1
        end_time = time.time()
        time_taken = end_time - start_time
        format_print("Simulated Annealing", len(cities), i, time_taken, tour_cost(current_tour))

        # Breaks the infinite loop after a certain amount of time
        if end_time - start_time > run_time:
            break
    return current_tour

# Variables to configure
# List of number of cities to run
num_cities_list = [50, 100, 150, 200, 250, 300]
run_time = 60

result_cost_HC = []
result_cost_SA = []
for num_cities in num_cities_list:
    global time_taken
    cities = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(num_cities)]

    # A function to update the plot
    def update_plot(tour, axis):
        x = [city[0] for city in tour]
        y = [city[1] for city in tour]
        axis.cla()
        axis.scatter(x, y, color='b')
        axis.plot(x + [x[0]], y + [y[0]], color='r')
        axis.set_title('Iteration: %i, Cost: %i' % (i, tour_cost(tour)))
        axis.set_xlim(-110, 110)
        axis.set_ylim(-110, 110)

    # Preinitialization
    fig, axis = plt.subplots(2, 2)

    # Initialize the plot
    axis[0, 0].set_xlim(-110, 110)
    axis[0, 0].set_ylim(-110, 110)
    axis[0, 0].scatter([city[0] for city in cities], [city[1] for city in cities], color='b')
    axis[0, 0].set_title('Cities')

    # Run the hill climbing algorithm and display the final result
    i = 0
    hill_climb_tour = hill_climb(cities, run_time, update_fn=lambda x: update_plot(x, axis[0, 1]))
    result_cost_HC.append(tour_cost(hill_climb_tour))
    axis[0, 1].cla()
    x = [city[0] for city in hill_climb_tour]
    y = [city[1] for city in hill_climb_tour]
    axis[0, 1].scatter(x, y, color='b')
    axis[0, 1].plot(x + [x[0]], y + [y[0]], color='r')
    axis[0, 1].set_title(f'Hill Climbing Result, Cost: {tour_cost(hill_climb_tour)}, Number of Cities: {num_cities}, Time taken: {time_taken:.3f} seconds')
    axis[0, 1].set_xlim(-110, 110)
    axis[0, 1].set_ylim(-110, 110)

    # Initialize the plot
    axis[1, 0].set_xlim(-110, 110)
    axis[1, 0].set_ylim(-110, 110)
    axis[1, 0].scatter([city[0] for city in cities], [city[1] for city in cities], color='b')
    axis[1, 0].set_title('Cities')

    # Run the simulated annealing algorithm and display the final result
    i = 0
    temperature = 10000
    cool = 0.9955
    simulated_annealing_tour = simulated_annealing(cities, run_time, temperature, cool, update_fn=lambda x: update_plot(x, axis[1, 1]))
    result_cost_SA.append(tour_cost(simulated_annealing_tour))
    axis[1, 1].cla()
    x = [city[0] for city in simulated_annealing_tour]
    y = [city[1] for city in simulated_annealing_tour]
    axis[1, 1].scatter(x, y, color='b')
    axis[1, 1].plot(x + [x[0]], y + [y[0]], color='r')
    axis[1, 1].set_title(f'Simulated Annealing Result, Cost: {tour_cost(simulated_annealing_tour)}, Number of Cities: {num_cities}, Time taken: {time_taken:.3f} seconds')
    axis[1, 1].set_xlim(-110, 110)
    axis[1, 1].set_ylim(-110, 110)
    
fig = plt.figure(figsize=(8, 8))

# Line plot of result costs of algorithms 
plt.plot(num_cities_list, result_cost_HC, label='Hill Climbing')
plt.plot(num_cities_list, result_cost_SA, label='Simulated Annealing')
plt.xlabel("Number of Cities")
plt.ylabel("Tour Cost")
plt.legend()
plt.title('Number of Cities vs. Tour Cost of Heuristics')
plt.show()