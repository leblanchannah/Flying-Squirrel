# Assignment 3 - Artificial Life - CISC 352
# Spencer Edwards - 13srte
# Hannah LeBlanc - 12hml4

#
# “I confirm that this submission is my own work and is consistent with
# the Queen's regulations on Academic Integrity.”
#

import time

class Boids:

    def __init__(self, n, interval):
        self.n = n     # number of boids
        self.interval = interval
        self.boids = [[0, 0]] * n      # boids[i] = (x, y)   ie. position of boid i
        self.velocities = [[0, 0]] * n # positions[i] = (vx, vy) ie. velocity in each direction of boid i
        runBoids(interval)

    def runBoids(self, interval):
        while True:
            start = time.time()

            # drawBoids()
            moveAllBoids()

            end = time.time()
            timeElapsed = end - start
            time.sleep(interval - timeElapsed)

    def moveAllBoids(self):
        v1 = None
        v2 = None
        v3 = None
        b = None
        for i in range(len(self.boids)):
            b = self.boids[i]
            v1 = self.separation(b)
            v2 = self.alignment(b)
            v3 = self.cohesion(b)
            sum = v1 + v2 + v3

            self.velocities[i] = self.velocities[i] + sum
            self.boids[i] = self.boids + self.velocities[i]

    def separation(self,b):
        # v = None
        v = b
        return b

    def alignment(self, b):
        # v = None
        v = b
        return b

    def cohesion(self, b):
        # v = None
        v = b
        return b

def main():
    n = 100         # number of boids
    interval = 1    # move boids every interval (in seconds)
    b = Boids(n, interval)

main()