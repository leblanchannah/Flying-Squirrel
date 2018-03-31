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
from tkinter import *

class Boids:

    def __init__(self, n, interval):
        self.n = n     # number of boids
        self.interval = interval
        self.boids = [[0,0] for i in range(n)]      # boids[i] = (x, y)   ie. position of boid i
        self.velocities = [[0,0] for i in range(n)] # positions[i] = (vx, vy) ie. velocity in each direction of boid i
        self.width = 800
        self.height = 600
        self.wall = 10
        self.wallForce = 10

        root = Tk()
        root.title("Hello")
        root.overrideredirect(True)
        root.geometry('%dx%d+%d+%d' % (self.width, self.height, (root.winfo_screenwidth() - self.width) / 2,
                                       (root.winfo_screenheight() - self.height) / 2))
        root.bind_all('<Escape>', lambda event: event.widget.quit())
        self.wn = Canvas(root, width=self.width, height=self.height, background='white')
        self.initializeBoids()
        self.wn.after(interval, self.runBoids)
        self.wn.pack()
        mainloop()

    def initializeBoids(self):
        quarter = self.n // 4
        #Place boids on screen with equal distribution
        for i in range(self.n):
            if i < quarter:
                left = self.width // 2
                right = self.width
                top = self.height
                bottom = self.height // 2
            elif i < (quarter * 2):
                left = 0
                right = self.width // 2
                top = self.height
                bottom = self.height // 2
            elif i < (quarter * 3):
                left = 0
                right = self.width // 2
                top = self.height // 2
                bottom = 0
            else:
                left = self.width // 2
                right = self.width
                top = self.height // 2
                bottom = 0
            self.boids[i][0] = random.randrange(left, right)
            self.boids[i][1] = random.randrange(bottom, top)
            #print("Boid: [" + str(self.boids[i][0]) + ", " + str(self.boids[i][1]) + "]")
        self.moveAllBoids()

    def runBoids(self):
        self.drawBoids()
        self.moveAllBoids()
        self.wn.after(self.interval, self.runBoids)

    def drawBoids(self):
        self.wn.delete(ALL)
        for i in range(self.n):
            self.drawABoid(self.boids[i], i)

    def drawABoid(self, boid, i):
        base = 10
        height = 15
        halfBase = base / 2
        halfHeight = height / 2
        centreX = boid[0]
        centreY = boid[1]
        centre = [centreX, centreY]
        #topX = centreX
        #topY = centreY + halfHeight
        #botLeftX = centreX - halfBase
        #botLeftY = centreY - halfHeight
        #botRightX = centreX + halfBase
        #botRightY = centreY - halfHeight
        theta = angleBetween([centreX, centreY])

        top = [centreX, centreY + halfHeight]
        botLeft = [centreX - halfBase, centreY + halfHeight]
        botRight = [centreX + halfBase, centreY - halfHeight]

        [topX, topY] = rotatePoint(top, centre, theta)
        [botLeftX, botLeftY] = rotatePoint(botLeft, centre, theta)
        [botRightX, botRightY] = rotatePoint(botRight, centre, theta)

        self.wn.create_line(topX, topY, botRightX, botRightY, botLeftX, botLeftY, topX, topY)
        self.wn.update()

    def moveAllBoids(self):
        v1 = None
        v2 = None
        v3 = None
        b = None
        for i in range(len(self.boids)):
            b = self.boids[i]
            self.checkWalls(b, i)

        for i in range(len(self.boids)):
            b = self.boids[i]
            #print("b: [" + str(b[0]) + ", " + str(b[1]) + "]")
            v1 = self.cohesion(b, i)
            v2 = self.separation(b, i)
            v3 = self.alignment(b, i)
            sum = vectorAdd(v1, vectorAdd(v2, v3))

            self.velocities[i] = vectorAdd(self.velocities[i], sum)
            self.boids[i] = vectorAdd(self.boids[i], self.velocities[i])

    def cohesion(self, bj, ix):
        pcj = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                pcj = vectorAdd(pcj, self.boids[i])
        pcj = [pcj[0] / (self.n - 1 / 2), pcj[1] / (self.n - 1 / 2)]
        return [(pcj[0] - self.boids[ix][0]) / 100, (pcj[1] - self.boids[ix][1]) / 100]

    def separation(self, bj, ix):
        c = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                if euclideanDistance(self.boids[i], self.boids[ix]) < 30:
                    c = vectorSubtract(c, vectorSubtract(self.boids[i],  self.boids[ix]))
        return c

    def alignment(self, bj, ix):
        pvj = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                pvj = vectorAdd(pvj, self.velocities[i])
        pvj = [pvj[0] / (self.n - 1), pvj[1] / (self.n - 1)]
        return [(pvj[0] - self.velocities[ix][0]) / 8, (pvj[1] - self.velocities[ix][1]) / 8]

    def checkWalls(self, boid, ix):
        x = boid[0]
        y = boid[1]
        if x < self.wall:
            self.velocities[ix][0] += self.wallForce
        elif x > (self.width - self.wall):
            self.velocities[ix][0] -= self.wallForce
        if y < self.wall:
            self.velocities[ix][1] += self.wallForce
        elif y < (self.height - self.wall):
            self.velocities[ix][1] -= self.wallForce

def euclideanDistance(v1, v2):
     return math.sqrt(math.pow(v2[0] - v1[0], 2) + math.pow(v2[1] - v1[1], 2))

def vectorAdd(v1, v2):
    i = 0
    vlen = len(v1)
    v3 = [0] * vlen
    for i in range(vlen):
        v3[i] = v1[i] + v2[i]
    return v3

def vectorSubtract(v1, v2):
    i = 0
    vlen = len(v1)
    v3 = [0] * vlen
    for i in range(vlen):
        v3[i] = v1[i] - v2[i]
    return v3

def angleBetween(v):
    u = [0, -10000]
    lengthU = math.sqrt(math.pow(u[0], 2) + math.pow(u[1], 2))
    lengthV = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))
    dotUV = (u[0] * v[0]) + (u[1] * v[1])
    result = dotUV / (lengthU * lengthV)
    if result > 1:
        result = 1
    elif result < (-1):
        result = -1
    #print("Angle between: " + str(math.degrees(math.acos(result))))
    return math.degrees(math.acos(result))

def rotatePoint(v, c, theta):
    x = v[0]
    y = v[1]
    cx = c[0]
    cy = c[1]
    #print("Before x: " + str(x) + ", before y: " + str(y))
    x -= cx
    y -= cy
    newX = (math.cos(theta) * x) - (math.sin(theta) * y)
    newY = (math.sin(theta) * x) + (math.cos(theta) * y)
    #print("After x: " + str(newX + cx) + ", after y: " + str(newY + cx))
    return [newX + cx, newY + cy]

def main():
    n = 24         # number of boids
    interval = 40  # move boids every interval (in milliseconds)
    b = Boids(n, interval)

main()