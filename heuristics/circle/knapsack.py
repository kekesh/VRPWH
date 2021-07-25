from .utilities import *
import numpy as np
import logging
import math

def knapsack(instance: VRPWHCircleInstance):
    """ The truck drives in the clockwise direction. We greedily utilize the helping agent whenever possible 
        to service future service stops without increasing the idle time of the truck driver. """

    # Add the point (-r, 0) as an "imaginary" service stop with service time zero.
    instance.add_service_stop(ServiceStop(-instance.radius, 0, 0, 0))
    instance.service_stops = sorted(instance.service_stops)
    serviced = set()
    cost = 2 * math.pi * instance.radius
    truck_location = 0

    
    while truck_location != instance.num_points:
        # Now processing service stop #[truck_location]
        truck_service_stop = instance.service_stops[truck_location]
        idle_time = truck_service_stop.service_time
        cost += idle_time


        # How close can we sum up to #[idle_time] (including distance traveled)?
        # To get the set of "candidates," we can first find the furthest service stop we can take.
        universal_set = []
        stops_left = instance.num_points - truck_location - 1
        for trying in range(1, stops_left + 1):
            distance_cost = ServiceStop.distance(truck_service_stop, instance.service_stops[trying + truck_location], instance.radius)
            service_cost = instance.service_stops[trying + truck_location].service_time
            if distance_cost + service_cost <= idle_time:
                if instance.service_stops[trying + truck_location].flag:
                    universal_set.append(instance.service_stops[trying + truck_location])
            else:
                break

        # We've constructed the subset. Now let's see what the closest amount we can get to idle_time is.
        waste, best, set_size = 1e9, [], len(universal_set)

        for bitmask in range(1, 1 << set_size): 
            subset = []
            for x in range(set_size):
                if (bitmask & (1 << x)):
                    subset.append(universal_set[x])
            distance_cost = 2 * ServiceStop.distance(truck_service_stop, subset[-1], instance.radius)
            service_cost = sum([x.service_time for x in subset])
            if service_cost + distance_cost <= idle_time and idle_time - service_cost - distance_cost < waste:
                waste = idle_time - service_cost - distance_cost
                best = subset

        # We've found the best "skippable" subset
        for service_stop in best:
            instance.remove_service_stop(service_stop)

        truck_location += 1


        
    return cost


# The knapsack heuristic should lookahead and service stop number 3, whereas the standard lookahead heuristic would service stop number 2.
instance = VRPWHCircleInstance(
                                num_points = 3,
                                radius = 1,
                                service_stops =
                                [

                                   ServiceStop(x = -math.sqrt(3) / 2, y = 1 / 2, service_time = 20, flag = True),
                                   ServiceStop(x = -math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 8, flag = True),
                                   ServiceStop(x = 0, y = 1, service_time = 10, flag = True)
                                ],
                                alpha = 1,
                                p = 1
                             )
print(knapsack(instance))
