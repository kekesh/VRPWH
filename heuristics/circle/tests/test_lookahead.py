import math
import numpy as np
from circle.utilities import *
from circle.lookahead import *

def test_lookahead_one():
    instance = VRPWHCircleInstance(
                                num_points = 4,
                                radius = 1,
                                service_stops =
                                [
                                   ServiceStop(x = 1, y = 0, service_time = 2, flag = True),
                                   ServiceStop(x = -math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 5, flag = True),
                                   ServiceStop(x = math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 1, flag = True),
                                   ServiceStop(x = 0, y = -1, service_time = 20, flag = True)
                                ],
                                alpha = 1,
                             )
    assert np.isclose(lookahead(instance), 27 + 2 * np.pi)

def test_lookahead_two():
    # The truck driver must service everything themselves, so lookahead reduces to baseline.
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
    assert np.isclose(lookahead(instance), 28 + 2 * np.pi)

def test_lookahead_three():
    # The truck driver must service everything themselves, so lookahead reduces to baseline.
    instance = VRPWHCircleInstance(
                                num_points = 4,
                                radius = 1,
                                service_stops =
                                [
                                   ServiceStop(x = 1, y = 0, service_time = 2, flag = False),
                                   ServiceStop(x = -math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 5, flag = False),
                                   ServiceStop(x = math.sqrt(2) / 2, y = math.sqrt(2) / 2, service_time = 1, flag = True),
                                   ServiceStop(x = 0, y = -1, service_time = 20, flag = False)
                                ],
                                alpha = 1,
                             )
    assert np.isclose(lookahead(instance), 27 + 2 * np.pi)
