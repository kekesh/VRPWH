from utilities import *
import numpy as np
import logging
import math

def lookahead(instance: VRPWHCircleInstance):
    """ The truck drives in the clockwise direction. We greedily utilize the helping agent whenever possible 
        to service future service stops without increasing the idle time of the truck driver. """

    # Add the point (-r, 0) as an "imaginary" service stop with service time zero.
    instance.add_service_stop(ServiceStop(-instance.radius, 0, 0, 0))
    instance.service_stops = sorted(instance.service_stops)
    cost = 2 * math.pi * instance.radius

    truck_location = 0
    alpha = instance.alpha

    while truck_location != instance.num_points:
        # Now processing service stop #[truck_location]
        truck_service_stop = instance.service_stops[truck_location]
        idle_time = truck_service_stop.service_time
        cost += idle_time

        # We use the helping agent to "lookahead" and process as many service stops as possible without exceeding #[idle_time].
        stops_left = instance.num_points - truck_location - 1
        cumulative_service_cost, trying = 0, 1
        while trying != stops_left + 1:
            distance_cost = alpha * ServiceStop.distance(truck_service_stop, instance.service_stops[trying + truck_location], instance.radius)
            if instance.service_stops[trying + truck_location].flag:
                cumulative_service_cost += instance.service_stops[trying + truck_location].service_time
            if idle_time >= distance_cost + cumulative_service_cost:
                if instance.service_stops[trying + truck_location].flag:
                    instance.remove_service_stop(instance.service_stops[trying + truck_location])
                    stops_left -= 1
                    continue
            else:
                break
            trying += 1
        truck_location += 1

    return cost
