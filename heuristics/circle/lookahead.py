from VRPWHCircleInstance import VRPWHCircleInstance

import numpy as np
import logging

def lookahead(instance):
  instance.sort_clockwise()
  curr_location = (-instance.radius, 0, 180) # (curr_x, curr_y, curr_angle)
  cost, i = 0, 0
  skipped_stations = []

  travel_cost = 0
  while i != len(instance.points):
    # pre-condition: i denotes the index of the next service station (i.e., we have not yet arrived to service station i).

    # add arc length to move to next service station
    cost += VRPWHCircleInstance.get_arc_length(instance.radius, curr_location[2], instance.points[i][2])
    travel_cost += VRPWHCircleInstance.get_arc_length(instance.radius, curr_location[2], instance.points[i][2])

    # update current location to the next service station
    curr_location = (instance.points[i][0], instance.points[i][1], instance.points[i][2])

    # greedily deploy the helping agent for the required number of time units
    cost += instance.points[i][3]

    # can the primary deliverer make other deliveries without increasing the helping agents' idle time?
    can_skip_count = 0
    if i != len(instance.points) - 1:
      service_costs = 0
      for k in range(i + 1, len(instance.points)):
        service_costs += instance.points[k][3]
        round_trip_cost = 2 * VRPWHCircleInstance.get_arc_length(instance.radius, curr_location[2], instance.points[k][2])

        total_cost = service_costs + round_trip_cost

        if instance.points[i][3] >= total_cost:
          # the primary deliverer can service the stations at (i + 1), (i + 2), ... k without any additional cost. 
          skipped_stations.append(k)
          can_skip_count += 1
        else:
          # we cannot service any more customers without any additional cost.
          break

    i += can_skip_count + 1

  # post-condition: all service stations have been serviced.
  # finally, we need to add the cost of returning back to (-r, 0)
  cost += VRPWHCircleInstance.get_arc_length(instance.radius, curr_location[2], -180)
  travel_cost += VRPWHCircleInstance.get_arc_length(instance.radius, curr_location[2], -180)
  assert(abs(travel_cost - np.pi * 2 * instance.radius) < 1e-6)
  return cost

instance = VRPWHCircleInstance(num_points=1000, radius=1000, mu=100, sigma=1)
instance.sort_clockwise()
print(str(instance))
print(lookahead(instance))
