from utilities import *
import numpy as np
import logging
import math

def neighbor_expansion(instance: VRPWHCircleInstance):
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



            # We have the neighbors of A[idx].
            # Compute the "best subset" we can get with these neighbors.
            waste, best, set_size = 1e9, [], len(neighbors)

            for bitmask in range(1, 1 << set_size):
                subset = []
                service_cost = 0
                for x in range(set_size):
                    if (bitmask & (1 << x)):
                        subset.append(neighbors[x])
                        service_cost += neighbors[x].service_time
                # We need to calculate the cost of servicing neighbors.
                subset = sorted(subset)

                # Compute distance costs
                distance_cost = 2 * alpha * ServiceStop.distance(A[idx], subset[0], instance.radius) 
                if len(subset) != 1:
                    distance_cost += 2 * alpha * ServiceStop.distance(A[idx], subset[-1], instance.radius)

                    
                if distance_cost + service_cost <= capacity and capacity - distance_cost - service_cost < waste:
                    # This is a feasible solution!
                    best = subset
                    waste = capacity - distance_cost - service_cost



            # Update global values
            if waste <= global_best_waste:
                global_best_subset = best 
                global_best_waste = waste
                best_idx = idx

        # Remove from A.
        if best_idx == -1:
            # We can't improve; treat everything individually.
            for service_stop in A:
                solution_cost += service_stop.service_time
                instance.remove_service_stop(service_stop)
        else:
            solution_cost += A[best_idx].service_time
            instance.remove_service_stop(A[best_idx])
            for service_stop in global_best_subset:
                instance.remove_service_stop(service_stop)
        A = instance.service_stops

    return solution_cost
