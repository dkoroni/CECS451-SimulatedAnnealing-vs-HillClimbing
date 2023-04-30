# Traveling Salesman Problem Solving Algorithms

This code provides two algorithms for solving the Traveling Salesman Problem (TSP):

- Hill Climbing
- Simulated Annealing

## Requirements

- [Python 3.x](https://www.python.org/downloads/)
- [Matplotlib](https://matplotlib.org/stable/users/installing/index.html)

## Usage

The `app.py` file contains two functions: `hill_climb` and `simulated_annealing`. Each function takes three arguments:

- `cities`: A list of `(x, y)` tuples representing the cities to be visited.
- `run_time`: The amount of time in seconds to run the algorithm.
- `temperature` (only for Simulated Annealing): The starting temperature for the algorithm.
- `cool` (only for Simulated Annealing): The cooling factor for the algorithm.

To run the algorithm for a specific number of cities, modify the `num_cities_list` variable at the end of the file.

Then to run the app.py file, type:
```bash
python app.py
```