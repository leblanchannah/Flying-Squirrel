import copy
from tkinter import *

class Conway:
    def __init__(self,generations,graph):
        self.gen = generations
        self.game = graph
        self.rows = len(graph) -1
        self.cols = len(graph[0]) -1 
        # game runs gen times, 1 = alive, 0 = dead
        # Calculate N, the N of live cells in C's eight-location neighborhood. 
        # need to change cell from (0,0).
        self.printGen(0)
        for i in range(self.gen):
            self.tempG = copy.deepcopy(self.game)
            for j in range(self.rows):
                for k in range(self.cols):
                    cell = (j,k)
                    self.n = self.nearby(self.tempG,cell)
                    self.game[cell[0]][cell[1]] = self.deadOrAlive(self.n,cell) #determine if cell is dead or alive
            self.printGen(i+1)
            
        
    def printGen(self,gen):
        print("Generation:" +str(gen))
        for i in range(self.rows):
            print("".join(str(self.game[i])))



    def deadOrAlive(self, N, cell):
        if self.tempG[cell[0]][cell[1]] == 0: # cell of interest is dead
            if N == 3:
                return 1 # a new cell is born 
            else:
                return 0
        else: #cell of interest is alive 
            if N < 2: # underpopulated
                return 0
            elif N == 2 or N == 3:
                return 1 # it lives
            else:
                return 0 # overcrowding


    #cell will be a tuple - (row,col)
    def nearby(self, graph, cell):
        row = cell[0]
        col = cell[1]
        N = 0
        if row != 0:
            N += graph[row-1][col]
            if col != 0:
                N += graph[row-1][col-1]
                N += graph[row][col-1]
            if col != self.cols:
                N += graph[row-1][col+1]
                N += graph[row][col+1]
        if row != self.rows:
            N += graph[row+1][col]
            if col != 0:
                N += graph[row+1][col-1]
            if col != self.cols:
                N += graph[row+1][col+1]
        return N

    # def build_graph(self):
    #     global graph
    #     global m
    #     WIDTH = m*len(grid[0])
    #     HEIGHT = m*len(grid)
    #     root = Tk()
    #     root.overrride

        


def IOGame(inFile, outFile):
    # number at start of file is number of generations to simulate followed by a graph
    # will there be more than one graph in a file?
    #read graph and parse into a 2d array
    f = open(inFile,"r")
    #out = open(outFile,"w") 
    graph = []
    generations = int(f.readline()) #number of generations won't be read twice
    for line in f:
        temp = list(line)[:-1]
        graph.append([int(x) for x in temp]) #removing \n char from line

    # need to print each thing to the file, open file and pass "out" to object??
    Conway(generations, graph)


def main():
    IOGame("inLife.txt","outLife.txt")


main()