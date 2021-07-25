import math
import numpy as np
from circle.utilities import *

# Tests basic instantiation of a ServiceStop object.
def test_servicestop_constructor():
    s = ServiceStop(x=2, y=3, service_time=5, flag=False)
    assert s.x == 2
    assert s.y == 3
    assert s.service_time == 5
    assert not s.flag

# Tests basic usage of the distance() function.
def test_servicestop_distance_one():
    s1 = ServiceStop(x=0, y=1, service_time=5, flag=False)
    s2 = ServiceStop(x=1, y=0, service_time=5, flag=False)
    assert np.isclose(ServiceStop.distance(s1, s2, 1), math.pi/2) 

# Tests symmetry of the distance() function. 
def test_servicestop_distance_two():
    s1 = ServiceStop(x=0, y=1, service_time=5, flag=False)
    s2 = ServiceStop(x=1, y=0, service_time=5, flag=False)
    assert np.isclose(ServiceStop.distance(s2, s1, 1), math.pi/2) 

# Tests distance function with non-unity radius. 
def test_servicestop_distance_three():
    s1 = ServiceStop(x=0, y=2, service_time=5, flag=False)
    s2 = ServiceStop(x=2, y=0, service_time=5, flag=False)
    assert np.isclose(ServiceStop.distance(s1, s2, 2), math.pi) 
    assert np.isclose(ServiceStop.distance(s2, s1, 2), math.pi) 

# Less trivial example on a circle with radius one.
def test_servicestop_distance_four():
    s1 = ServiceStop(x=-1/2, y=math.sqrt(3)/2, service_time=5, flag=False)
    s2 = ServiceStop(x=1/2, y=math.sqrt(3)/2, service_time=5, flag=False)
    assert np.isclose(ServiceStop.distance(s1, s2, 1), math.pi / 3) 
    assert np.isclose(ServiceStop.distance(s2, s1, 1), math.pi / 3) 

# Less trivial example on a circle with non-one radius.
def test_servicestop_distance_five():
    s1 = ServiceStop(x=-math.sqrt(2)/2, y=math.sqrt(6)/2, service_time=5, flag=False)
    s2 = ServiceStop(x=math.sqrt(2)/2, y=math.sqrt(6)/2, service_time=5, flag=False)
    assert np.isclose(ServiceStop.distance(s1, s2, 2), 2 * math.pi / 3) 
    assert np.isclose(ServiceStop.distance(s2, s1, 2), 2 * math.pi / 3) 

# Less trivial example on a circle with non-integer radius.
def test_servicestop_distance_five():
    s1 = ServiceStop(x=-math.sqrt(2)/2, y=math.sqrt(6)/2, service_time=5, flag=False)
    s2 = ServiceStop(x=math.sqrt(2)/2, y=math.sqrt(6)/2, service_time=5, flag=False)
    assert np.isclose(ServiceStop.distance(s1, s2, math.sqrt(2)), math.pi * math.sqrt(2) / 3) 
    assert np.isclose(ServiceStop.distance(s2, s1, math.sqrt(2)), math.pi * math.sqrt(2) / 3) 

# Verify that randomly-generated VRPWH instances actually have their service stops on the circle.
def test_instance_servicestops_one():
    vrpwh = generate_random_vrpwh_instance(num_points=100, radius=1, mu=5, sigma=1, alpha=1, p=1)
    assert all([np.isclose(service_stop.x ** 2 + service_stop.y ** 2, vrpwh.radius ** 2) for service_stop in vrpwh.service_stops]) 

# Verify that randomly-generated VRPWH instances actually have their service stops on the circle.
def test_instance_servicestops_two():
    vrpwh = generate_random_vrpwh_instance(num_points=1000, radius=10, mu=5, sigma=1, alpha=1, p=1)
    assert all([np.isclose(service_stop.x ** 2 + service_stop.y ** 2, vrpwh.radius ** 2) for service_stop in vrpwh.service_stops]) 

# Verify that randomly-generated VRPWH instances actually have their service stops on the circle.
def test_instance_servicestops_three():
    vrpwh = generate_random_vrpwh_instance(num_points=10000, radius=200, mu=5, sigma=1, alpha=1, p=1)
    assert all([np.isclose(service_stop.x ** 2 + service_stop.y ** 2, vrpwh.radius ** 2) for service_stop in vrpwh.service_stops]) 

def test_instance_servicestops_sort_one():
    service_stops = [ServiceStop(x = 2, y = 0, service_time = 5, flag = False), ServiceStop(x = 0, y = 2, service_time = 5, flag = False)]
    service_stops = sorted(service_stops)
    assert service_stops[0].x == 0 and service_stops[0].y == 2 and service_stops[1].x == 2 and service_stops[1].y == 0

def test_instance_servicestops_sort_two():
    ss1 = ServiceStop(x = 0, y = 2, service_time = 5, flag = False)
    ss2 = ServiceStop(x = 2, y = 0, service_time = 5, flag = False)
    service_stops = sorted([ss1, ss2])
    assert service_stops[0] == ss1 and service_stops[1] == ss2

def test_instance_servicestops_sort_three():
    ss1, ss2 = ServiceStop(x = -2, y = 0, service_time = 5, flag = False), ServiceStop(x = 2, y = 0, service_time = 5, flag = False)
    service_stops = sorted([ss1, ss2])
    assert np.array_equal(service_stops, [ss1, ss2])
    service_stops = sorted([ss2, ss1])
    assert np.array_equal(service_stops, [ss1, ss2])

def test_instance_servicestops_sort_four():
    ss1, ss2 = ServiceStop(x = -2, y = 0, service_time = 5, flag = False), ServiceStop(x = 2, y = 0, service_time = 5, flag = False)
    service_stops = sorted([ss1, ss2])
    assert np.array_equal(service_stops, [ss1, ss2])
    service_stops = sorted([ss2, ss1])
    assert np.array_equal(service_stops, [ss1, ss2])

def test_instance_servicestops_sort_four():
    ss1, ss2, ss3, ss4 = ServiceStop(x = 1, y = 0, service_time = 5, flag = False), ServiceStop(x = 0, y = -1, service_time = 5, flag = False), ServiceStop(x = 0, y = 1, service_time = 5, flag = False), ServiceStop(x = -1, y = 0, service_time = 5, flag = False),
    service_stops = sorted([ss1, ss2, ss3, ss4])
    assert np.array_equal(service_stops, [ss4, ss3, ss1, ss2])

# Verify that adding a new service stop increments the total number of service stops.
def test_add_service_stop():
    service_stops = [ServiceStop(x = 1, y = 0, service_time = 5, flag = False), ServiceStop(x = 0, y = -1, service_time = 5, flag = False), ServiceStop(x = 0, y = 1, service_time = 5, flag = False), ServiceStop(x = -1, y = 0, service_time = 5, flag = False)]
    instance = VRPWHCircleInstance(len(service_stops), 1, service_stops, 1)
    assert instance.num_points == 4
    instance.add_service_stop(ServiceStop(x = 1, y = 0, service_time = 5, flag = True))
    assert instance.num_points == 5

def test_remove_service_stop():
    service_stops = [ServiceStop(x = 1, y = 0, service_time = 5, flag = False), ServiceStop(x = 0, y = -1, service_time = 5, flag = False), ServiceStop(x = 0, y = 1, service_time = 5, flag = False), ServiceStop(x = -1, y = 0, service_time = 5, flag = False)]
    instance = VRPWHCircleInstance(len(service_stops), 1, service_stops, 1)

    # This service stop doesn't exist.
    instance.remove_service_stop(ServiceStop(x = 0, y = -2, service_time = 5, flag = False))
    assert instance.num_points == 4

    # This service stop exists.
    instance.remove_service_stop(ServiceStop(x = 0, y = -1, service_time = 5, flag = False))
    assert instance.num_points == 3

def test_service_stop_equality():
    ss1 = ServiceStop(x = -2, y = 0, service_time = 5, flag = False) 
    assert ss1 == ServiceStop(x = -2, y = 0, service_time = 5, flag = False) 
    assert ss1 != ServiceStop(x = -2, y = 0, service_time = 5, flag = True)
    assert ss1 != ServiceStop(x = -2, y = 0, service_time = 4, flag = False)
    assert ss1 != ServiceStop(x = -2, y = 1, service_time = 5, flag = False)
    assert ss1 != ServiceStop(x = -1, y = 0, service_time = 5, flag = False) 




