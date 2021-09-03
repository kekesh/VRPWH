from rexpansion import randomized_expansion
from baseline import baseline
from lookahead import lookahead
from knapsack import knapsack
from neighbor_expansion import neighbor_expansion
from utilities import *

if __name__ == "__main__":
    results = [0] * 5
    NUM_SIMS = 25 

    fp = open("output.txt", "w+")

    # (n, r, p, mu, sigma, alpha)
    tests = [
#             (10, 1, 0.00, 1, 1, 1),
#             (10, 1, 0.25, 1, 1, 1),
#             (10, 1, 0.50, 1, 1, 1),
#             (10, 1, 0.75, 1, 1, 1),
#             (10, 1, 1.00, 1, 1, 1),
#             (25, 1, 0.00, 2, 1, 4),
#             (25, 1, 0.25, 2, 1, 4),
#             (25, 1, 0.50, 2, 1, 4),
#             (25, 1, 0.75, 2, 1, 4),
#             (25, 1, 1.00, 2, 1, 4),
#             (50, 1, 0.00, 3, 1, 2),
#             (50, 1, 0.25, 3, 1, 2),
#             (50, 1, 0.50, 3, 1, 2),
#             (50, 1, 0.75, 3, 1, 2),
#             (50, 1, 1.00, 3, 1, 2),
             (75, 1, 0.00, 5, 1, 4.0/3.0),
             (75, 1, 0.25, 5, 1, 4.0/3.0),
             (75, 1, 0.50, 5, 1, 4.0/3.0),
             (75, 1, 0.75, 5, 1, 4.0/3.0),
             (75, 1, 1.00, 5, 1, 4.0/3.0),
             (100, 1, 0.00, 10, 1, 1e9),
             (100, 1, 0.25, 10, 1, 1e9),
             (100, 1, 0.50, 10, 1, 1e9),
             (100, 1, 0.75, 10, 1, 1e9),
             (100, 1, 1.00, 10, 1, 1e9)
            ]

    for test in tests:
        num_points, radius, p, mu, sigma, alpha, = test
        print("Now on Test: ", test)
        for iteration in range(NUM_SIMS):
          print("Iteration number: ", iteration)
          instance: VRPWHCircleInstance = generate_random_vrpwh_instance(num_points, radius, mu, sigma, alpha, p)
          results[0] += baseline(VRPWHCircleInstance.deep_copy(instance))
          results[1] += lookahead(VRPWHCircleInstance.deep_copy(instance))
          results[2] += knapsack(VRPWHCircleInstance.deep_copy(instance))
          results[3] += neighbor_expansion(VRPWHCircleInstance.deep_copy(instance))
          results[4] += randomized_expansion(VRPWHCircleInstance.deep_copy(instance))

        fp.write(str(test))
        fp.write("\n")
        fp.write("Baseline: {}\n".format(results[0] / NUM_SIMS))
        fp.write("Lookahead: {}\n".format(results[1] / NUM_SIMS))
        fp.write("Knapsack: {}\n".format(results[2] / NUM_SIMS))
        fp.write("Neighbor: {}\n".format(results[3] / NUM_SIMS))
        fp.write("Randomized: {}\n".format(results[4] / NUM_SIMS))
