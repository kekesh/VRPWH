import math
import numpy as np
from circle.utilities import *
from circle.baseline import *

def test_baseline_one():
    service_stops = [ServiceStop(x = 1, y = 0, service_time = 5, flag = False)]
    instance = VRPWHCircleInstance(num_points = 1, radius = 1, service_stops = service_stops, alpha = 1, p = 1)
    assert np.isclose(baseline(instance), 2 * math.pi + 5)

def test_baseline_two():
    service_stops = [ServiceStop(x = 1, y = 0, service_time = 5, flag = False), ServiceStop(x = 0, y = 1, service_time = 5, flag = False)]
    instance = VRPWHCircleInstance(num_points = 1, radius = 1, service_stops = service_stops, alpha = 1, p = 1)
    assert np.isclose(baseline(instance), 2 * math.pi + 10)

def test_baseline_three():
    service_stops = [ServiceStop(x = 2, y = 0, service_time = 5, flag = False), ServiceStop(x = 0, y = 2, service_time = 5, flag = False)]
    instance = VRPWHCircleInstance(num_points = 1, radius = 2, service_stops = service_stops, alpha = 1, p = 1)
    assert np.isclose(baseline(instance), 4 * math.pi + 10)
