from VRPWHCircleInstance import VRPWHCircleInstance
from lookahead import lookahead

import numpy as np
import logging

def knapsack(instance, arr, start, neighbors):
  res = []
  mini = 1e9
  x = len(neighbors)
  for i in range(1 << x):
    subset = []
    for j in range(x):
      if (i & (1 << j)):
        subset.append(neighbors[j])

    # see if subset works.
    # by assumption, the subset is sorted in clockwise order.
    curr_angle = arr[start][2]
    travel_cost = 0
    service_cost = 0

    for j in range(len(subset)):
      service_cost += arr[subset[j]][3]
      travel_cost += VRPWHCircleInstance.get_arc_length(instance.radius, curr_angle, arr[subset[j]][2])
      curr_angle = arr[subset[j]][2]
    travel_cost += VRPWHCircleInstance.get_arc_length(instance.radius, curr_angle, arr[start][2])

    if travel_cost + service_cost <= arr[start][3] and arr[start][3] - travel_cost - service_cost < mini:
      res = subset
      mini = arr[start][3] - travel_cost - service_cost

  return res, mini

def expansion(instance):
  instance.sort_clockwise()
  A = instance.points
  cost, remaining = 0, 0

  # count the total number of service stations that the helping agent can service
  for i in range(len(A)):
    remaining += A[i][4]

  max_idx = 0
  i = 0
  done = set()

  while remaining > 0:
    (x, y, angle, service_time, agent_can_help) = A[i]
    if agent_can_help and i not in done:
      left_neighbors = []
      right_neighbors = []

      # Get the left neighbors of A[i].
      j = i - 1 if i - 1 >= 0 else i - 1 + remaining
      total_service_time = A[j][3]
      total_travel_time = 2 * (VRPWHCircleInstance.get_arc_length(instance.radius, angle, A[j][2]))
      while total_service_time + total_travel_time <= service_time:
        # pre-condition: j is a left neighbor of A[i].
        left_neighbors.append(j)
        j = j - 1 if j - 1 >= 0 else j - 1 + remaining
        total_service_time += A[j][3]
        total_travel_time = 2 * (VRPWHCircleInstance.get_arc_length(instance.radius, angle, A[j][2]))

      # Get the right neighbors of A[i]
      j = i + 1 if i + 1 < remaining else i + 1 - remaining
      total_service_time = A[j][3]
      total_travel_time = 2 * (VRPWHCircleInstance.get_arc_length(instance.radius, angle, A[j][2]))
      print("Total time to start is " + str(total_service_time + total_travel_time))
      while total_service_time + total_travel_time <= service_time:
        # pre-condition: j is a left neighbor of A[i].
        right_neighbors.append(j)
        j = j + 1 if j + 1 < remaining else j + 1 - remaining
        total_service_time += A[j][3]
        total_travel_time = 2 * (VRPWHCircleInstance.get_arc_length(instance.radius, angle, A[j][2]))

      neighbors = left_neighbors + right_neighbors
      print("Neighbors of " + str(A[i]) + " is " + str(neighbors))
      best_subset, mini = knapsack(instance, instance.points, i, neighbors)
      print("Best subset is " + str(best_subset) + " with a minimum of " + str(mini))
      cost += A[i][3]
      max_idx = max(max_idx, i)
      done.add(i)
      remaining -= 1
      for x in best_subset:
        print("POPPING " + str(x))
        max_idx = max(max_idx, x)
        remaining -= A[x][4]
        done.add(x)
    i += 1

  for i in range(len(A)):
    if A[i] not in done and i <= max_idx:
      cost += A[i][3]
    elif A[i] not in done and i > max_idx:
      cost += VRPWHCircleInstance.get_arc_length(instance.radius, A[i][2], A[max_idx][2])
      max_idx = i
  return cost

instance = VRPWHCircleInstance(num_points=10, radius=1, mu=1, sigma=1, alpha=0.50, p=1)
