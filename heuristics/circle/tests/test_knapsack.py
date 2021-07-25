import math
import numpy as np
from circle.utilities import *
from circle.knapsack import *

def test_knapsack_one():
    # The knapsack heuristic should lookahead and service stop number 3, whereas the standard lookahead heuristic would service stop number 2.
    instance = VRPWHCircleInstance(
                                    num_points = 3,
                                    radius = 1,
                                    service_stops =
                                    [
    
                                       ServiceStop(x = -math.sqrt(3) / 2, y = 1 / 2, service_time = 20, flag = True),
                                       ServiceStop(x = -math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 9, flag = True),
                                       ServiceStop(x = 0, y = 1, service_time = 10, flag = True)
                                    ],
                                    alpha = 1,
                                 )

    assert knapsack(instance) == 29 + 2 * math.pi

def test_knapsack_two():
    # We can't use the helping agent at Service Stop 3, so we'll have to go with Service Stop 2.
    instance = VRPWHCircleInstance(
                                    num_points = 3,
                                    radius = 1,
                                    service_stops =
                                    [
    
                                       ServiceStop(x = -math.sqrt(3) / 2, y = 1 / 2, service_time = 20, flag = True),
                                       ServiceStop(x = -math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 9, flag = True),
                                       ServiceStop(x = 0, y = 1, service_time = 10, flag = False)
                                    ],
                                    alpha = 1,
                                 )
    assert knapsack(instance) == 30 + 2 * math.pi

def test_knapsack_three():
    # We can't use the helping agent anywhere: knapsack heuristic should reduce to baseline heuristic.
    instance = VRPWHCircleInstance(
                                    num_points = 3,
                                    radius = 1,
                                    service_stops =
                                    [
    
                                       ServiceStop(x = -math.sqrt(3) / 2, y = 1 / 2, service_time = 20, flag = False),
                                       ServiceStop(x = -math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 9, flag = False),
                                       ServiceStop(x = 0, y = 1, service_time = 10, flag = False)
                                    ],
                                    alpha = 1,
                                 )
    assert knapsack(instance) == 39 + 2 * math.pi

def test_knapsack_four():
    # Minimal optimal solution
    instance = VRPWHCircleInstance(
                                    num_points = 3,
                                    radius = 1,
                                    service_stops =
                                    [
    
                                       ServiceStop(x = -math.sqrt(3) / 2, y = 1 / 2, service_time = 20, flag = False),
                                       ServiceStop(x = -math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 9, flag = False),
                                       ServiceStop(x = 0, y = 1, service_time = 10, flag = True)
                                    ],
                                    alpha = 1,
                                 )
    assert knapsack(instance) == 29 + 2 * math.pi
