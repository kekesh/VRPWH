from utilities import *
import numpy as np
from numpy import random
from numpy.random import uniform
import logging
import math

def randomized_expansion(instance: VRPWHCircleInstance):
    """ The truck drives in the clockwise direction. We compute the set of neighbors for each service stop. """
    A = instance.service_stops
    alpha = instance.alpha
    solution_cost = 2 * math.pi * instance.radius

    # While there are service stops that need to be serviced...
    while A: 
        # Compute the set of neighbors for each service stop in A.
        n = len(A)
        global_best_subset = []
        global_best_waste = 1e9
        global_best_idx = -1
        done = True

        for idx in range(n):
            # Compute the set of neighbor in both directions
            neighbors = []
            capacity = A[idx].service_time

            # "Left neighbors"
            j = idx - 1
            while j >= 0: 
                total_cost = A[j].service_time + 2 * alpha * ServiceStop.distance(A[idx], A[j], instance.radius)
                if total_cost <= capacity:
                    neighbors.append(A[j])
                j -= 1

            # "Right neighbors"
            j = idx + 1
            while j < n:
                total_cost = A[j].service_time + 2 * alpha * ServiceStop.distance(A[idx], A[j], instance.radius)
                if total_cost <= capacity:
                    neighbors.append(A[j])
                j += 1

            if not len(neighbors):
                continue;

            best_idx, candidate, feasible, set_size, waste = -1, [], False, len(neighbors), 1e9
            while not feasible: 
                # Generate a random bitmask
                bitmask = 0
                for x in range(set_size):
                    coin = uniform(0, 1) 
                    bitmask += (coin >= 0.50)
                    if x != set_size - 1:
                        bitmask <<= 1

                # cost of both
                subset, service_cost = [], 0
                for x in range(set_size):
                    if (bitmask & (1 << x)):
                        subset.append(neighbors[x])
                        service_cost += neighbors[x].service_time
                subset = sorted(subset)

                # Compute the distance costs
                if subset:
                    distance_cost = 2 * alpha * ServiceStop.distance(A[idx], subset[0], instance.radius) 
                    if len(subset) != 1:
                      distance_cost += 2 * alpha * ServiceStop.distance(A[idx], subset[-1], instance.radius)
                    feasible = (distance_cost + service_cost <= capacity)
                    done = done and not feasible

                if feasible and capacity - distance_cost - service_cost < waste:
                    # This is a feasible solution!
                    candidate = subset
                    waste = capacity - distance_cost - service_cost
                    best_idx = x

            if waste < global_best_waste:
                global_best_subset = candidate
                global_best_waste = waste
                global_best_idx = best_idx

        if done:
            for candidate in A:
                solution_cost += candidate.service_time
                instance.remove_service_stop(candidate)
        else:
            solution_cost += A[global_best_idx].service_time
            instance.remove_service_stop(A[global_best_idx])
            for service_stop in global_best_subset:
                instance.remove_service_stop(service_stop)

        A = instance.service_stops

    return solution_cost
