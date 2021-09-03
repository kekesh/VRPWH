from utilities import *
import numpy as np
import logging
import math

def baseline(instance: VRPWHCircleInstance):
  ''' 
  The baseline heuristic always traverses the circle exactly one time (and it spends 2 * pi * r time doing so). 
  Finally, we must add the (sum_{i} service_time_i) to the answer as no optimizations are used.
  ''' 
  cost = 2 * math.pi * instance.radius
  for service_stop in instance.service_stops:
    cost += service_stop.service_time
  return cost
