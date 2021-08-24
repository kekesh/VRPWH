import math
import numpy as np
from circle.utilities import *
from circle.neighbor_expansion import *

def test_nexpansion_one():
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
    assert np.isclose(neighbor_expansion(instance), 29 + 2 * np.pi)
