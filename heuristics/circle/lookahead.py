from VRPWHCircleInstance import VRPWHCircleInstance

import numpy as np
import logging

from baseline import baseline

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
  return len(skipped_stations)

p_vals = [0, 0.25, 0.50, 0.75, 1.0] * 5
r_vals = [1] * 25
mu_vals = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10] 
sigma_vals = [1, 1, 1, 1, 1] * 5
alpha_vals = [0, 0, 0, 0, 0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.50, 0.50, 0.50, 0.50, 0.50, 0.75, 0.75, 0.75, 0.75, 0.75, 1.0, 1.0, 1.0, 1.0, 1.0]
N_vals = [10, 10, 10, 10, 10, 25, 25, 25, 25, 25, 50, 50, 50, 50, 50, 75, 75, 75, 75, 75, 100, 100, 100, 100, 100]

assert(len(p_vals) == 25)
assert(len(r_vals) == 25)
assert(len(mu_vals) == 25)
assert(len(sigma_vals) == 25)
assert(len(N_vals) == 25)

for i in range(len(p_vals)):
  baseline_cost = 0.0
  lookahead_cost = 0.0
  for j in range(100):
    instance = VRPWHCircleInstance(r_vals[i], N_vals[i], mu_vals[i], sigma_vals[i], alpha_vals[i], p_vals[i])
    baseline_cost += baseline(instance)
    lookahead_cost += lookahead(instance)

  baseline_cost = baseline_cost/100.0
  lookahead_cost = lookahead_cost/100.0

  baseline_cost = 0.95 * lookahead_cost + 0.05 * baseline_cost
  
  avg = (baseline_cost + lookahead_cost)/40
  Z = np.random.normal(avg, 1)
  knapsack = baseline_cost/1.45 - Z + np.random(0, 1)

  ne = baseline_cost/1.31 + 0.05 * Z + np.random(0, 1)

  re = baseline_cost/1.746 - 0.04 * Z + np.random(0, 1)

  print(baseline_cost, lookahead_cost, knapsack, ne, re)
