# Assignment 3 - Artificial Life - CISC 352
# Spencer Edwards - 13srte
# Hannah LeBlanc - 12hml4

#
# “I confirm that this submission is my own work and is consistent with
# the Queen's regulations on Academic Integrity.”
#

import time
import math
import random
import turtle

class Boids:

    def __init__(self, n, interval):
        self.n = n     # number of boids
        self.interval = interval
        self.boids = [[0, 0]] * n      # boids[i] = (x, y)   ie. position of boid i
        self.velocities = [[0, 0]] * n # positions[i] = (vx, vy) ie. velocity in each direction of boid i
        self.turtles = []
        self.wn = turtle.Screen()
        self.initializeBoids()
        self.runBoids(interval)

    def initializeBoids(self):
        width = 400
        height = 300
        self.wn.bgcolor("lightgreen")
        self.wn.screensize(width, height)
        for i in range(self.n):
            self.boids[i][0] = random.randrange(0, width)
            self.boids[i][1] = random.randrange(0, height)
            self.turtles.append(turtle.Turtle())
            self.turtles[i].shape("turtle")
            self.turtles[i].speed("fastest")
            self.turtles[i].penup()
            self.turtles[i].setx(self.boids[i][0])
            self.turtles[i].sety(self.boids[i][1])
            self.turtles[i].pendown()

    def runBoids(self, interval):
        while True:
            start = time.time()

            self.moveAllBoids()
            self.drawBoids()

            end = time.time()
            timeElapsed = end - start
            time.sleep(interval - timeElapsed)

    def drawBoids(self):
        self.wn.clear()
        self.wn.bgcolor("lightgreen")
        for i in range(len(self.turtles)):
            self.turtles[i].stamp()
            self.turtles[i].penup()
            self.turtles[i].setx(self.boids[i][0])
            self.turtles[i].sety(self.boids[i][1])
            self.turtles[i].setheading(angleBetween(self.boids[i], self.velocities[i]))
            self.turtles[i].pendown()

    def moveAllBoids(self):
        v1 = None
        v2 = None
        v3 = None
        b = None
        for i in range(len(self.boids)):
            b = self.boids[i]
            print("b: [" + str(b[0]) + ", " + str(b[1]) + "]")
            v1 = self.cohesion(b, i)
            v2 = self.separation(b, i)
            v3 = self.alignment(b, i)
            sum = self.vectorAdd(v1, self.vectorAdd(v2, v3))

            self.velocities[i] = self.vectorAdd(self.velocities[i], sum)
            self.boids[i] = self.vectorAdd(self.boids[i], self.velocities[i])

    def cohesion(self, bj, ix):
        pcj = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                pcj = self.vectorAdd(pcj, self.boids[i])
        pcj = [pcj[0] / (self.n - 1), pcj[1] / (self.n - 1)]
        return [(pcj[0] - self.boids[ix][0]) / 100, (pcj[1] - self.boids[ix][1]) / 100]

    def separation(self, bj, ix):
        c = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                if self.euclideanDistance(self.boids[i], self.boids[ix]) < 10:
                    c = self.vectorSubtract(c, self.vectorSubtract(self.boids[i],  self.boids[ix]))
        return c

    def alignment(self, bj, ix):
        pvj = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                pvj = self.vectorAdd(pvj, self.velocities[i])
        pvj = [pvj[0] / (self.n - 1), pvj[1] / (self.n - 1)]
        return [(pvj[0] - self.velocities[ix][0]) / 8, (pvj[1] - self.velocities[ix][1]) / 8]

    def euclideanDistance(self, v1, v2):
        return math.sqrt(math.pow(v2[0] - v1[0], 2) + math.pow(v2[1] - v1[1], 2))

    def vectorAdd(self, v1, v2):
        i = 0
        vlen = len(v1)
        v3 = [0] * vlen
        for i in range(vlen):
            v3[i] = v1[i] + v2[i]
        return v3

    def vectorSubtract(self, v1, v2):
        i = 0
        vlen = len(v1)
        v3 = [0] * vlen
        for i in range(vlen):
            v3[i] = v1[i] - v2[i]
        return v3

def angleBetween(u, v):
    lengthU = math.sqrt(math.pow(u[0], 2) + math.pow(u[1], 2))
    lengthV = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))
    dotUV = (u[0] * v[0]) + (u[1] * v[1])
    result = dotUV / (lengthU * lengthV)
    if result > 1:
        result = 1
    elif result < (-1):
        result = -1
    return math.acos(result)

def main():
    n = 10         # number of boids
    interval = 2    # move boids every interval (in seconds)
    b = Boids(n, interval)

main()