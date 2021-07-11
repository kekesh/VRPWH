import numpy as np
import functools
import itertools
import math
from random import random


class ServiceStop:
    ''' 
    Provides a representation of a service stop at a point (x, y) with a user-defined service time.  
    A Boolean flag is used to represent whether or not the service stop can be serviced by our helping agent.
    The distance method provides us with an easy way to compute the distance between two service stations on the circle (i.e., arc length).
    '''
    def __init__(self, x, y, service_time, flag):
        self.x = x
        self.y = y
        self.service_time = service_time
        self.flag = flag

    @staticmethod
    def distance(s1, s2, r):
        ''' 
        Construct a triangle with vertices at the radius and the two points. 
        By the Law of Cosines, the angle between the two points is arccos(1 - d^2/2r^2).
        '''
        d = (s1.x - s2.x) ** 2 + (s1.y - s2.y) ** 2
        theta = np.arccos(1 - d/(2 * r * r))
        return r * theta

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class VRPWHCircleInstance:
  def __init__(self, num_points, radius, service_stops, alpha, p):
    self.num_points = num_points
    self.radius = radius
    self.service_stops = service_stops
    self.alpha = alpha
    self.p = p

  def __str__(self):
    rep = "Radius: {}, Alpha: {}, p: {}, N: {}".format(self.radius, self.alpha, self.p, self.num_points)
    for service_stop in self.service_stops:
        rep += "\n" + str(service_stop)
    return rep

def generate_random_service_stop(r, mu, sigma, p) -> ServiceStop:
    ''' 
    Generate a random service stop located uniformly at random on the circle x^2 + y^2 = r^2. 
    The service time of the service stop is drawn from a truncated N(mu, sigma^2) distribution (i.e., we redraw until X >= 0 and X >= 2 * mu)
    '''
    def generate_random_coordinate(r):
        theta = random() * 2 * math.pi
        return r * np.cos(theta), r * np.sin(theta)

    def get_service_time(mu, sigma):
        service_time = -1
        while service_time < 0 or service_time > 2 * mu:
            service_time = np.random.normal(mu, sigma)
        return service_time

    coords = generate_random_coordinate(r)
    service_time = get_service_time(mu, sigma)
    flag = p >= random()

    return ServiceStop(x=coords[0], y=coords[1], service_time=service_time, flag=flag)

def generate_random_vrpwh_instance(num_points, radius, mu, sigma, alpha, p) -> VRPWHCircleInstance:
    ''' 
    Generate a random instance of the VRPWH problem.
    The service time of the service stop is drawn from a truncated N(mu, sigma^2) distribution (i.e., we redraw until X >= 0 and X >= 2 * mu)
    '''
    service_stops = []
    for _ in itertools.repeat(None, num_points):
        service_stops.append(generate_random_service_stop(radius, mu, alpha, p))
    return VRPWHCircleInstance(num_points, radius, service_stops, alpha, p)
