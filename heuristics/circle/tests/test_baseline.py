import math
import numpy as np
from circle.utilities import *
from circle.baseline import *

# Simple tests of the baseline heuristic. Note that the baseline heuristic should spend exactly (circumference + \sum_i service_times_i) total time

def test_baseline_one():
    service_stops = [ServiceStop(x = 1, y = 0, service_time = 5, flag = False)]
    instance = VRPWHCircleInstance(num_points = 1, radius = 1, service_stops = service_stops, alpha = 1)
    assert np.isclose(baseline(instance), 2 * math.pi + 5)

def test_baseline_two():
    service_stops = [ServiceStop(x = 1, y = 0, service_time = 5, flag = False), ServiceStop(x = 0, y = 1, service_time = 5, flag = False)]
    instance = VRPWHCircleInstance(num_points = len(service_stops), radius = 1, service_stops = service_stops, alpha = 1)
    assert np.isclose(baseline(instance), 2 * math.pi + 10)

def test_baseline_three():
    service_stops = [ServiceStop(x = 2, y = 0, service_time = 5, flag = False), ServiceStop(x = 0, y = 2, service_time = 5, flag = False)]
    instance = VRPWHCircleInstance(num_points = len(service_stops), radius = 2, service_stops = service_stops, alpha = 1)
    assert np.isclose(baseline(instance), 4 * math.pi + 10)

def test_baseline_four():
    instance = VRPWHCircleInstance(
                                num_points = 4,
                                radius = 1,
                                service_stops =
                                [
                                   ServiceStop(x = 1, y = 0, service_time = 2, flag = False),
                                   ServiceStop(x = -math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 5, flag = False),
                                   ServiceStop(x = math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 1, flag = False),
                                   ServiceStop(x = 0, y = -1, service_time = 20, flag = False)
                                ],
                                alpha = 1,
                             )
    assert np.isclose(baseline(instance), 28 + 2 * np.pi)
