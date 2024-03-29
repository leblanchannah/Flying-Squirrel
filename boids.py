# Spencer Edwards 
# Hannah LeBlanc 

import time
import math
import random
from tkinter import *

class Boids:

    def __init__(self, n, interval):
        self.n = n     # number of boids
        self.interval = interval
        self.boids = [[0,0] for i in range(n)]      # boids[i] = (x, y)   ie. position of boid i
        self.width = 800
        self.height = 600
        self.centreX = self.width // 2
        self.centreY = self.height // 2
        self.velocities = [[0, 0] for i in range(n)] # positions[i] = (vx, vy) ie. velocity in each direction of boid i
        self.wall = 10
        self.wallForce = 5
        self.boidSize = 6
        self.startTime = 0
        self.timeElapsed = 0
        self.offsetStart = 20
        
        root = Tk()
        root.title("Hello")
        root.overrideredirect(True)
        root.geometry('%dx%d+%d+%d' % (self.width, self.height, (root.winfo_screenwidth() - self.width) / 2,
                                       (root.winfo_screenheight() - self.height) / 2))
        root.bind_all('<Escape>', lambda event: event.widget.quit())
        self.wn = Canvas(root, width=self.width, height=self.height, background='white')
        #self.random_start()
        self.initializeBoids()
        self.wn.after(interval, self.runBoids)
        self.wn.pack()
        mainloop()


    def random_start(self):
        for i in range(self.n):
            if random.randint(0,1):
                #along left and right
                y = random.randint(1,self.height)
                if random.randint(0,1):
                    #along left
                    x = -self.offsetStart
                else:
                    x = self.width + self.offsetStart
            else:
                #along top and bottom
                x = random.randint(1,self.width)
                if random.randint(0,1):
                    #along top
                    y = -self.offsetStart
                else:
                    y = self.height + self.offsetStart
            self.boids[i][0] = x
            self.boids[i][1] = y
            self.velocities[i] = [0,0]
            self.startTime = time.time()

        
    def initializeBoids(self):
        quarter = self.n / 4
        #Place boids on screen with equal distribution
        for i in range(self.n):
            if i < quarter:
                left = self.width // 2
                right = self.width
                top = 0
                bottom = self.height // 2
            elif i < (quarter * 2):
                left = 0
                right = self.width // 2
                top = 0
                bottom = self.height // 2
            elif i < (quarter * 3):
                left = 0
                right = self.width // 2
                top = self.height // 2
                bottom = self.height
            else:
                left = self.width // 2
                right = self.width
                top = self.height // 2
                bottom = self.height
            self.boids[i][0] = random.randrange(left, right)
            self.boids[i][1] = random.randrange(top, bottom)
            self.velocities[i] = [(self.centreX - self.boids[i][0]) / 100,
                                  (self.centreY - self.boids[i][1]) / 100]
        self.startTime = time.time()
        self.moveAllBoids()

    def runBoids(self):
        self.timeElapsed = time.time() - self.startTime
        self.drawBoids()
        self.moveAllBoids()
        self.wn.after(self.interval, self.runBoids)

    def drawBoids(self):
        self.wn.delete(ALL)
        for i in range(self.n):
            self.drawABoid(self.boids[i])

    def drawABoid(self, boid):
        centreX = boid[0]
        centreY = boid[1]

        leftX = centreX - self.boidSize
        leftY = centreY - (self.boidSize)
        rightX = centreX + self.boidSize
        rightY = centreY + (self.boidSize)

        self.wn.create_oval(leftX, leftY, rightX, rightY)
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
            v1 = self.cohesion(b, i)
            #print("x v1 = " + str(v1[0]) + " y v1 = " + str(v1[1]))
            v2 = self.separation(b, i)
            #print("x v2 = " + str(v2[0]) + " y v2 = " + str(v2[1]))
            v3 = self.alignment(b, i)
            #print("x v3 = " + str(v3[0]) + " y v3 = " + str(v3[1]))
            sum = vectorAdd(v1, vectorAdd(v2, v3))
            #print("sum x v1+v2+v3 = " + str(sum[0]) + " sum y v1+v2+v3 = " +str(sum[1]))
            if (self.timeElapsed > 15) and (self.timeElapsed < 25):
                v4 = self.wind()
                sum = vectorAdd(sum, v4)

            self.velocities[i] = vectorAdd(self.velocities[i], sum)
            
        for i in range(len(self.boids)):
            self.velocities[i][0] /= 5
            self.velocities[i][1] /= 5
            self.boids[i] = vectorAdd(self.boids[i], self.velocities[i])

    def cohesion(self, bj, ix):
        pcj = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                pcj = vectorAdd(pcj, self.boids[i])
        pcj = [pcj[0] / (self.n - 1), pcj[1] / (self.n - 1)]
        #print("x pcj = " + str(pcj[0]) + " y pcj = " + str(pcj[1]))
        return [(pcj[0] - self.boids[ix][0]) / 8, (pcj[1] - self.boids[ix][1]) / 8]

    def separation(self, bj, ix):
        c = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                if euclideanDistance(self.boids[i], self.boids[ix]) < 35:
                    c = vectorSubtract(c, vectorSubtract(self.boids[i],  self.boids[ix]))
        return c

    def alignment(self, bj, ix):
        pvj = [0, 0]
        for i in range(len(self.boids)):
            b = self.boids[i]
            if b != bj:
                pvj = vectorAdd(pvj, self.velocities[i])
        pvj = [pvj[0] / (self.n - 1), pvj[1] / (self.n - 1)]
        #print("x pvj = " + str(pvj[0]) + " y pvj = " + str(pvj[1]))
        return [(pvj[0] - self.velocities[ix][0]) / 16, (pvj[1] - self.velocities[ix][1]) / 16]

    def wind(self):
        v = [0, 25]
        return v

    def checkWalls(self, boid, ix):
        x = boid[0]
        y = boid[1]
        if x < self.wall:
            self.velocities[ix][0] += self.wallForce
        elif x > (self.width - self.wall):
            self.velocities[ix][0] -= self.wallForce
        if y < self.wall:
            self.velocities[ix][1] += self.wallForce
        elif y > (self.height - self.wall):
            self.velocities[ix][1] -= self.wallForce

    def angleBetween(self, v):
        u = [self.centreX, self.centreY]
        lengthU = math.sqrt(math.pow(u[0], 2) + math.pow(u[1], 2))
        lengthV = math.sqrt(math.pow(v[0], 2) + math.pow(v[1], 2))
        dotUV = (u[0] * v[0]) + (u[1] * v[1])
        result = dotUV / (lengthU * lengthV)
        if result > 1:
            result = 1
        elif result < (-1):
            result = -1
        return math.degrees(math.acos(result))

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

def main():
    n = 24         # number of boids
    interval = 40  # move boids every interval (in milliseconds)
    b = Boids(n, interval)

main()
