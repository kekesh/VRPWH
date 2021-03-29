import numpy as np
import functools

class VRPWHCircleInstance:
  def __init__(self, radius, num_points, mu, sigma):
    self.radius = radius
    self.circumference = 2 * np.pi * self.radius
    self.num_points = num_points
    self.points = []

    # Generate num_points uniformly on x^2 + y^2 = r^2.
    for i in range(0, self.num_points):
      Z = np.random.uniform(0, 1)
      theta = 2 * np.pi * Z

      service_time = 2 * mu + 1
      while service_time > 2 * mu or service_time < 0:
        service_time = np.random.normal(mu, sigma)

      (x, y, angle, service_time) = (self.radius * np.cos(theta), self.radius * np.sin(theta), np.degrees(theta), service_time)
      if angle > 180:
        angle -= 360
      self.points.append((x, y, angle, service_time))

  def __str__(self):
    rep = "Radius: {}".format(self.radius) + "\n"
    rep += "Number of points: {}".format(self.num_points) + "\n"
    for i in range(0, len(self.points)):
      rep += "[" + str(i + 1) + "]: " + "(x = " + str(self.points[i][0]) + ", y = " + str(self.points[i][1]) + ", angle = " + str(self.points[i][2]) + ", service_time = " + str(self.points[i][3]) + ")\n"

    return rep

  # Input assumes a1, a2 are in degrees
  @staticmethod
  def get_arc_length(r, a1, a2):
    if a1 > 0 and a2 < 0:
      return VRPWHCircleInstance.get_arc_length(r, a1, 0) + VRPWHCircleInstance.get_arc_length(r, 0, a2)
    return r * abs(np.radians(a1) - np.radians(a2))

  # Sort points in clockwise order (i.e., from (-r, 0) to (0, r) to (r, 0) to (0, -r)).
  def sort_clockwise(self):
    def clockwise_comparator(point1, point2):
      a1, a2 = point1[2], point2[2]
      if a1 * a2 >= 0:
        return -1 if a1 >= a2 else 1
      return 1 if (a1 <= 0 and a2 >= 0) else -1
    self.points = sorted(self.points, key=functools.cmp_to_key(clockwise_comparator))
