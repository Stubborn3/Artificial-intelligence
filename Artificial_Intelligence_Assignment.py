import numpy as np
import time
import copy

class node:
    def __init__(self):
        self.matrix = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None

class puzzle:
    def __init__(self):
        self.root = None
        self.temp = None
        #self.start = np.array([[1,2,0,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], dtype = int)
        #self.start = np.array([[4,1,3],[0,2,6],[7,5,8]], dtype = int)
        self.start = np.array([[0,9,8,1],[4,5,6,7],[2,3,10,11],[12,13,14,15]], dtype = int)
#        self.start = np.array([[0,1,2,3],[5,6,7,4],[9,10,11,8],[13,14,15,12]], dtype = int)
        #self.start = np.array([[4,1,2,3],[5,6,10,7],[8,13,9,11],[12,0,14,15]], dtype = int)
        #self.goal = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], dtype = int)
        #start = 1,4,2,6,5,8,7,3,0
        #self.start = np.array([[1,2,3],[0,4,6],[7,5,8]], dtype = int)
        self.current = None
        self.ptr = None
        self.flg = False
        self.goalFound = False
        self.grid = None
    

    def userInterface(self):
        self.grid = int(input("Enter the Grid size: "))
        self.start = np.zeros((self.grid,self.grid),dtype = int)
        for i in range(self.grid):
            for j in range(self.grid):
                self.start[i][j] = int(input("Enter the num: "))

    def puzzleTree(self,temp ,flag):
        if self.root == None:
            temp = node()
            temp.matrix = self.start
            temp.left = None
            temp.right = None
            temp.up = None
            temp.down = None
            self.root = temp
            if self.validSolvability(temp.matrix):
                return True
            return False
        elif temp.left == None and flag == 'left':
            temp.left = node()
            temp.left.matrix = self.current
            temp.left.left = None
            temp.left.right = None
            temp.left.up = None
            temp.left.down = None
        elif temp.right == None and flag == 'right':
            temp.right = node()
            temp.right.matrix = self.current
            temp.right.left = None
            temp.right.right = None
            temp.right.up = None
            temp.right.down = None
        elif temp.up == None and flag == 'up':
            temp.up = node()
            temp.up.matrix = self.current
            temp.up.left = None
            temp.up.right = None
            temp.up.up = None
            temp.up.down = None
        elif temp.down == None and flag == 'down':
            temp.down = node()
            temp.down.matrix = self.current
            temp.down.left = None
            temp.down.right = None
            temp.down.up = None
            temp.down.down = None



    def blankUp(self,temp,tuple):
        row = tuple[0] -  1
        if row > -1 and row < self.grid:
            self.current = copy.deepcopy(temp)
            var = self.current[row][tuple[1]]
            self.current[row][tuple[1]] = 0
            self.current[row+1][tuple[1]] = var
            if self.ptr != None and np.array_equal(self.ptr.matrix,self.current):
                #print("check")
                return False
            return True
        return False
    
    def blankDown(self,temp,tuple):
        row = tuple[0] +  1
        if row > -1 and row < self.grid:
            self.current = copy.deepcopy(temp)
            var = self.current[row][tuple[1]]
            self.current[row][tuple[1]] = 0
            self.current[row-1][tuple[1]] = var
            if self.ptr != None and np.array_equal(self.ptr.matrix,self.current):
                return False
            return True
        return False
    
    def blankLeft(self,temp, tuple):
        col = tuple[1] - 1
        if col > -1 and col < self.grid:
            self.current = copy.deepcopy(temp)
            var = self.current[tuple[0]][col]
            self.current[tuple[0]][col] = 0
            self.current[tuple[0]][col+1] = var
            if self.ptr != None and np.array_equal(self.ptr.matrix,self.current):
                #print("check")
                return False
            return True
        return False

    def blankRight(self,temp,tuple):
        col = tuple[1] +  1
        if col > -1 and col < self.grid:
            self.current = copy.deepcopy(temp)
            var = self.current[tuple[0]][col]
            self.current[tuple[0]][col] = 0
            self.current[tuple[0]][col-1] = var
            if self.ptr != None and np.array_equal(self.ptr.matrix,self.current):
                #print("check")
                return False
            return True
        return False

    def mainFunction(self):
        if self.grid % 2 == 1:
            if self.puzzleTree('',''):
                self.goal = np.array([[1,2,3],[4,5,6],[7,8,0]], dtype = int)
                self.goal = np.array([[0,1,2],[3,4,5],[6,7,8]], dtype = int)
                print("It's reachable for:")
                print(self.goal)
            else:
                # self.goal = np.array([[0,1,2],[3,4,5],[6,7,8]], dtype = int)
                # self.goal = np.array([[1,2,3],[4,5,6],[7,8,0]], dtype = int)
                print("It's not solveable")
                return
        else:
            if self.puzzleTree('',''):
                self.goal = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]], dtype = int)
                print("It's reachable for:")
                print(self.goal)
            else:
                self.goal = np.array([[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]], dtype = int)
                print("It's reachable for:")
                print(self.goal)
        print(" - - - - - - - - - - - -")
        limit = 1
        while True:
            start = 1
            i = 0
            while i < limit:
                self.traverseInsert(self.root,start,limit)
                i +=1
            self.flg = True
            self.traverseDeletion(self.root)
            if self.goalFound:
                break
            limit += 1
        self.flg = True
        self.cost = -1
        self.movesMatrix(self.root)
        print("Total Cost: ", self.cost)

    def movesMatrix(self,temp):
        if self.flg:
            self.cost += 1
            print(temp.matrix)
        if np.array_equal(temp.matrix,self.goal):
            self.flg = False
        if temp.left != None and self.flg:
            print("Move Left")
            self.movesMatrix(temp.left)
        if temp.down != None and self.flg:
            print("Move Down")
            self.movesMatrix(temp.down)
        if temp.right != None and self.flg:
            print("Move Right")
            self.movesMatrix(temp.right)
        if temp.up != None and self.flg:
            print("Move Up")
            self.movesMatrix(temp.up)

    def traverseInsert(self,temp, start,reach):
        if temp.left != None:
            start += 1
            self.ptr = temp
            self.traverseInsert(temp.left,start,reach)
            start -= 1
        if temp.down != None:
            start += 1
            self.ptr = temp
            self.traverseInsert(temp.down,start,reach)
            start -= 1
        if temp.right != None:
            start += 1
            self.ptr = temp
            self.traverseInsert(temp.right,start,reach)
            start -= 1
        if temp.up != None:
            start += 1
            self.ptr = temp
            self.traverseInsert(temp.up,start,reach)
            start -= 1
        if start <= reach:
            if self.blankLeft(temp.matrix,self.checkRow(temp.matrix)):
                self.puzzleTree(temp,'left')
            if self.blankDown(temp.matrix,self.checkRow(temp.matrix)):
                self.puzzleTree(temp,'down')
            if self.blankRight(temp.matrix,self.checkRow(temp.matrix)):
                self.puzzleTree(temp,'right')
            if self.blankUp(temp.matrix,self.checkRow(temp.matrix)):
                self.puzzleTree(temp,'up')

    def traverseDeletion(self,temp):
        if temp.left != None and self.flg:
            self.ptr = temp
            self.traverseDeletion(temp.left)
            self.ptr = temp
        if temp.down != None and self.flg:
            self.ptr = temp
            self.traverseDeletion(temp.down)
            self.ptr = temp
        if temp.right != None and self.flg:
            self.ptr = temp
            self.traverseDeletion(temp.right)
            self.ptr = temp
        if temp.up != None and self.flg:
            self.ptr = temp
            self.traverseDeletion(temp.up)
            self.ptr = temp

        if self.deleteNode():
            self.flg = False
            self.goalFound = True
        

    def deleteNode(self):
        if self.ptr.left != None and self.ptr.left.left == None and self.ptr.left.right == None and self.ptr.left.down == None and self.ptr.left.up == None:
            if np.array_equal(self.ptr.left.matrix,self.goal):
                #print("goal is found")
                return True
            del self.ptr.left
            self.ptr.left = None
        if self.ptr.down != None and self.ptr.down.left == None and self.ptr.down.right == None and self.ptr.down.down == None and self.ptr.down.up == None:
             if np.array_equal(self.ptr.down.matrix,self.goal):
                #print("goal is found")
                return True
             del self.ptr.down
             self.ptr.down = None
        if self.ptr.right != None and self.ptr.right.left == None and self.ptr.right.right == None and self.ptr.right.down == None and self.ptr.right.up == None:
             if np.array_equal(self.ptr.right.matrix,self.goal):
                #print("goal is found")
                return True
             del self.ptr.right
             self.ptr.right = None
        if self.ptr.up != None and self.ptr.up.left == None and self.ptr.up.right == None and self.ptr.up.down == None and self.ptr.up.up == None:
             if np.array_equal(self.ptr.up.matrix,self.goal):
                #print("goal is found")
                return True
             del self.ptr.up
             self.ptr.up = None

    def countInversions(self,matrix):
        matrix = copy.deepcopy(matrix.reshape(-1))
        inversion = 0
        count = 0
        for i in range(self.grid*self.grid-1):
            count = 0
            for j in range(i+1,self.grid*self.grid):
                if matrix[i] > matrix[j] and matrix[j] > 0:
                    count += 1
            inversion += count
        return inversion
    
    def checkRow(self,matrix):
        for i in range(self.grid):
            for j in range(self.grid):
                if matrix[i][j] == 0:
                    return i,j

    def validSolvability(self,matrix):
        if self.grid % 2 == 1:
            if self.countInversions(matrix) % 2 == 0:
                return True
            return False
        else:
            if self.countInversions(matrix) % 2 == 0 and self.checkRow(matrix)[0] % 2 == 1:
                print("A")
                return True
            elif self.countInversions(matrix) % 2 == 1 and self.checkRow(matrix)[0] % 2 == 0:
                print("B")
                return True
            return False

obj = puzzle()
obj.userInterface()
obj.mainFunction()
