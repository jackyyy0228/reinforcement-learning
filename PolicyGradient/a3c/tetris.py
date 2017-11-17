
#basic modules needed for game to run
import numpy as np
import random
import pygame
from move import ipieces,opieces,jpieces,lpieces,zpieces,spieces,tpieces,zeropieces,allpieces
import move
from draw import *
#TODO
#Tspin check
GAME_OVER_REWARD = -0.2

class Tetris:
    def __init__(self,action_type = 'grouped',use_fitness = False,is_display = False,_screen = None):
        self.is_display = is_display
        self.action_type = action_type
        self.use_fitness = use_fitness
        if self.is_display:
            if _screen:
                self.screen = _screen
            else:
                self.screen = Screen()
    def reset(self):
        self.grid = [[0]*20 for i in range(10)]
        self.nextlist = []
        self.piecelist=[ipieces,opieces,jpieces,
                         lpieces,zpieces,spieces,tpieces]
        for i in range (5):
            self.nextlist.append(random.choice(self.piecelist))
            self.piecelist.remove(self.nextlist[-1])
        self.tspin = False
        self.b =  None ##piece
        self.newBlock()
        self.block = self.b[0] #0,1,2,3 denote different rotations
        self.tspin = 0
        self.px = 4
        self.py = -1  #modified
        self.combo = 0
        self.prev_clear_type = None # back to back tetris/tspin
        self.held = zeropieces
        self.change = False
        self.done = False
        self.singleCounter = 0
        self.positions=[] #block position, used for drawing screen
        self.totalSent = 0
        self.prev_fitness = 0
        if self.is_display:
            self.display()
        return self.get_state()
    def step(self,action):
        if self.check_collide(self.px,self.py):
            self.done = True
        if self.done:
            return self.get_state(),GAME_OVER_REWARD,self.done
        if self.action_type == 'grouped':
            return self.groupedAction(action)
        elif self.action_type == 'single': #haven't finished
            return self.singleAction(action)
    def groupedAction(self,actionID):
        #actionID = 0~4*13+1(hold) = 53
        #rotate 0~3 times, left 0~6 times right 0~6 times
        reward=0
        if actionID == 52:
            if not self.change:
                self.change = True
                self.hold()
                reward = 0
        else:
            self.change = False
            rotate_num = actionID % 4
            line = actionID // 4 - 6
            for i in range(rotate_num):
                self.rotate()
            if line < 0:
                leftTime = -line
                for i in range(leftTime):
                    self.moveLeft()
            elif line > 0:
                rightTime = line
                for i in range(rightTime):
                    self.moveRight()
            self.hardDrop()
            reward = self.check_end()
            if not self.done:
                self.newBlock()
                self.px = 4
                self.py = -1
        if self.is_display:
            self.display()
            
        return self.get_state(),reward,self.done
    def singleAction(self,actionID):
        #actionlist = ['Right','Left','Down','Rotate','HardDrop','Hold']
        self.single_end = False
        if actionID == 0:
            self.moveRight()
        elif actionID == 1:
            self.moveLeft()
        elif actionID == 2:
            self.single_end = self.moveDown()
        elif actionID == 3:
            self.rotate()
        elif actionID == 4:
            self.hardDrop()
            self.single_end = True
        elif actionID == 5:
            self.hold()
        self.singleCounter += 1
        reward = 0
        if self.singleCounter % 5 == 0:
            self.single_end = self.moveDown()
        if self.single_end:
            reward = self.check_end()
            if not self.done:
                self.newBlock()
                self.px = 4
                self.py = -1
        if self.is_display:
            self.display()
        return self.get_state(),reward,self.done
    def check_collide(self,new_px,new_py):
        for x in range(4):
            for y in range(4):
                if self.block[x][y] > 0:
                    if not 10 > new_px + x >= 0:
                        return True
                    if new_py + y >= 20:
                        return True
                    if new_py + y >= 0 and self.grid[new_px + x][new_py + y] > 0:
                        return True
        return False
    def moveRight(self):
        new_px = self.px + 1
        if not self.check_collide(new_px,self.py):
            self.px = new_px
    def moveLeft(self):
        new_px = self.px - 1
        if not self.check_collide(new_px,self.py):
            self.px = new_px
    def moveDown(self):
        new_py = self.py + 1
        if not self.check_collide(self.px,new_py):
            self.py = new_py
            return False
        return True
    def hardDrop(self):
        new_py = self.py + 1
        while not self.check_collide(self.px,new_py):
            self.py = new_py
            new_py += 1
    def hold(self):
        if self.held != zeropieces:
            self.held,self.b = self.b,self.held
            self.block = self.b[0]
        else:
            self.held = self.b
            self.newBlock()
    def rotate(self):
        self.block,self.px,self.py,self.tspin = move.rotate(self.grid,self.block,self.px,self.py,self.b,self.tspin)
        return
    def newBlock(self):
        if len(self.piecelist) == 0:
            self.piecelist = [ipieces,opieces,jpieces,lpieces,zpieces,spieces,tpieces]
        n=random.randint(0,len(self.piecelist)-1) 
        self.nextlist.append(self.piecelist[n])
        self.piecelist.remove(self.piecelist[n])
        self.b = self.nextlist[0]
        self.block = self.b[0]
        self.nextlist.remove(self.nextlist[0])
    def check_end(self):
        if self.check_collide(self.px,self.py):
            self.done = True
            return GAME_OVER_REWARD
        for x in range(4):
            for y in range(4):
                if self.block[x][y] > 0:
                    if 0 <= self.px + x < 10 and 0 <= self.py + y <20:
                        self.grid[self.px+x][self.py+y] = self.block[x][y]
        ## check line cleared
        total_clear = 0
        for y in range(20):
            is_clear = True
            for x in range(10):
                if not 8 > self.grid[x][y] > 0:
                    is_clear = False
            if is_clear:
                total_clear += 1
                for x in range(10):
                    for y2 in range(y,0,-1):
                        self.grid[x][y2] = self.grid[x][y2-1]
                    self.grid[x][0] = 0
        sent = 0
        if total_clear > 0:
            if self.combo > 8:
                sent = total_clear -1 + 4
            else:
                sent = total_clear -1 + (self.combo+1) // 2
            if total_clear == 4:
                if self.prev_clear_type == 'tetris':
                    sent += 2
                else:
                    sent += 1
                self.prev_clear_type = 'tetris'
            sent += 1
        if total_clear > 0:
            self.combo += 1
        else:
            self.combo = 0
        self.prev_clear_type = None
        self.totalSent += sent
        ## check end game
        for x in range (4):
            for y in range (4):
                if self.block[x][y] > 0:
                    if self.py+y < 0:
                        self.done = True
                        return GAME_OVER_REWARD
        if self.use_fitness :
            fitness = self.cal_fitness(total_clear)
            self.prev
        return sent
    def cal_fitness(self,lines):
        height = cal_height(self.grid)
        bumpiness = cal_bumpiness(self.grid)
        holes = cal_holes(self.grid)
        return -0.51 * height + 0.76 * lines - 0.36 * holes - 0.18 * bumpiness 
    def getPositions(self):  
        self.positions=[]
        for x in range(4):
            for y in range(4):
                if self.block[x][y] > 0:
                    self.positions.append((self.px+x,self.py+y))
                    sorted(self.positions, key=lambda pos: pos[1])
    def place_block(self):
        temp_grid = np.array(self.grid)
        for x in range(4):
            for y in range(4):
                if self.block[x][y] > 0:
                    if 10 > self.px + x >= 0 and 20 > self.py + y >=0:
                        temp_grid[self.px + x][self.py+y] = self.block[x][y]
        return temp_grid

    def get_state(self): #[grid,nextlist[0]....,held]
        statelist=[]
        temp_grid = self.place_block()
        grid = np.where( temp_grid>0 ,1,0)
        grid = np.reshape(grid.T,(20,10,1))
        templist = list(self.nextlist)
        templist.append(self.held)
        for idx,piece in enumerate(templist):
            if piece != zeropieces:
                num = allpieces.index(piece)
            else:
                num = len(allpieces)
            X = np.zeros(len(allpieces) + 1)
            X[num] = 1
            if idx > 0:
                Y = np.concatenate((Y,X))
            else:
                Y = np.array(X)
        return [grid,Y]
    def display(self):
        self.getPositions()
        self.screen.drawScreen(self.grid,self.px,self.py,self.block,
                               self.held,self.nextlist,
                               self.positions,self.totalSent)
    def draw(self):
        ## For testing
        temp_grid = self.place_block()
        for y in range(20):
            for x in range(10):
                print(temp_grid[x][y],end=' ')
            print()
        print('#'*20)
def cal_holes(grid):
    num_holes = 0
    for x in range(10):
        for y in range(1,20):
            if grid[x][y] == 0:
                check = True
                for (x2,y2) in [(-1,0),(0,-1),(1,0),(0,1)]:
                    if 0 <= x + x2 < 10 and 0 <= y + y2 <20 and grid[x+x2][y+y2] == 0 :
                        check = False
                if check:
                    num_holes += 1
    return num_holes
def cal_height(grid):
    sum_height = 0
    for x in range(10):
        height = 0
        for y in range(20):
            if grid[x][y] > 0:
                height = 20 - y
                break
        sum_height += height
    return sum_height
def cal_bumpiness(grid):
    height_list = []
    for x in range(10):
        height = 0
        for y in range(20):
            if grid[x][y] > 0:
                height = 20 - y
                break
        height_list.append(height)
    bumpiness = 0
    for x in range(len(height_list)-1):
        bumpiness += abs(height_list[x] - height_list[x+1])
    return bumpiness


class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,600))#screen is 800*600
        self.screen.blit(gamescreen,(0,0))#blitting the main background
        self.a = self.screen.copy()#used for image coverage
        pygame.display.flip()
    def drawScreen(self,grid,px,py,block,held,nextlist,positions,sent,is_p2 = False):
        bias = 0
        if is_p2:
            bias += 383
        self.drawHeld(grid,held,46+8+bias,161)#draws held piece for grid1
        self.drawNext(grid,nextlist,318+bias,161)#draws next piece for grid1
        self.drawNumbers(grid,sent,56+bias,377)#draws the linessent on the screen for grid1
        self.drawBackground(112+bias,138,grid,positions) # draw background
        self.drawPiece(112+bias,138,block,px,py) #drawing the pieces
        self.drawBoard(grid,112+bias,138) #drawing the grid
        pygame.display.flip()
    def drawHeld(self,grid,held,sx,sy):
        if held != zeropieces:
            num=allpieces.index(held)
            pos=[]
            for x in range (4):
                for y in range (4):
                    if held[0][x][y]>0:
                        pos.append((x,y))
            self.screen.blit(holdback,(sx-8,159))
            if num>1:
                for i in range(4):#if its an i piece different x and y position
                    self.screen.blit(resizepics[num],
                                     (sx+int(pos[i][0]*12),sy+int(pos[i][1]*12)))
            if num==0:
                for i in range(4):#if its an o piece different x and y position
                    self.screen.blit(resizepics[num],
                                     (sx-5+int(pos[i][0]*12),sy-6+int(pos[i][1]*12)))
            if num==1:
                for i in range(4):#any other piece id the same x and y position
                    self.screen.blit(resizepics[num],
                                     (sx-5+int(pos[i][0]*12),sy+int(pos[i][1]*12)))
    def drawNext(self,grid,nextpieces,sx,sy): 
        for i in range (5):#5 different pieces 
            pos=[]
            for x in range (4):
                for y in range (4): #same procedure as the drawhed function
                    if nextpieces[i][0][x][y]>0:
                        num=nextpieces[i][0][x][y]
                        pos.append((x,y))
            
            if i==0: #position 1
                self.screen.blit(holdback,(sx-1,159))            
                if num ==1:#i piece is different x and y pos
                    for i in range (4):
                        self.screen.blit(resizepics[num-1],
                                         (sx+1+int(pos[i][0]*12),156+int(pos[i][1]*12)))
                elif num==2: #o piece is different x and y pos
                    for i in range (4):
                        self.screen.blit(resizepics[num-1],
                                         (sx+1+int(pos[i][0]*12),158+int(pos[i][1]*12)))                
                else: #every other piece is the same x and y pos              
                    for i in range (4):
                        self.screen.blit(resizepics[num-1],
                                         (sx+7+int(pos[i][0]*12),159+int(pos[i][1]*12)))
            if i==1: #position2
                self.screen.blit(nextback2,(sx+2,230))
                if num==1:#i piece is differnet x and y pos
                    for i in range (4):
                        self.screen.blit(nextpics[num-1],
                                         (sx+9+int(pos[i][0]*8),235+int(pos[i][1]*8)))
                if num==2:#o piece is differnt x and y pos
                    for i in range (4):
                        self.screen.blit(nextpics[num-1],
                                         (sx+10+int(pos[i][0]*8),235+int(pos[i][1]*8)))
                if num>2:#every other piece same x and y pos
                    for i in range (4):
                        self.screen.blit(nextpics[num-1],
                                         (sx+13+int(pos[i][0]*8),235+int(pos[i][1]*8)))
            if i>=2:#position 3,4,5
                self.screen.blit(nextback3,(sx+4,288+52*(i-2)))
                if num==1: #same as above
                    for j in range (4):
                        self.screen.blit(nextpics[num-1],
                                         (sx+9+int(pos[j][0]*8),288+(i-2)*51+int(pos[j][1]*8)))
                if num==2: #same as above
                    for j in range (4):
                        self.screen.blit(nextpics[num-1],
                                         (sx+9+int(pos[j][0]*8),292+(i-2)*51+int(pos[j][1]*8)))
                if num>2: #same as above
                    for j in range (4):
                        self.screen.blit(nextpics[num-1],
                                         (sx+12+int(pos[j][0]*8),292+(i-2)*51+int(pos[j][1]*8)))
    def drawBlock(self,sx,sy,x,y,val):
        pics = [ipiece,opiece,jpiece,lpiece,zpiece,spiece,tpiece,lspiece]
        self.screen.blit(pics[val-1],(sx+(x)*18,sy+(y)*18))
    def drawPiece(self,sx,sy,block,px,py):
        for x in range(4):
            for y in range (4):
                if block[x][y]>0:
                    if -1<px+x<10 and -1<py+y<20:
                        self.drawBlock(sx,sy,px+x,py+y,block[x][y])

    def drawBoard(self,grid,sx,sy):
        for x in range (10):
            for y in range (20):
                if grid[x][y]>0:
                    self.drawBlock(sx,sy,x,y,grid[x][y])
    def drawBackground(self,sx,sy,grid,positions):
        for x in range(10):
            for y in range (20):
                if grid[x][y] == 0 and (x,y) not in positions:
                    if (x+y)%2 == 0:
                        self.screen.blit(dgrey,(sx+x*18,sy+y*18))
                    elif (x+y)%2 == 1:
                        self.screen.blit(lgrey,(sx+x*18,sy+y*18))
    def drawNumbers(self,grid,sent,sx,sy):
        tens=sent // 10#integer division tens digit
        ones=sent%10#remainder ones digit
        self.screen.blit(sentback,(sx-12,sy))
        if tens>0:
            if tens==1:
                #blitting the numbers at the poisition in numbers list
                self.screen.blit(numbers[tens],(sx-14,sy))
                self.screen.blit(numbers[ones],(sx+7,sy))
            else:
                self.screen.blit(numbers[tens],(sx-14,sy))
                self.screen.blit(numbers[ones],(sx+14,sy))
        else:
            self.screen.blit(numbers[ones],(sx,sy))


if __name__ == '__main__':
    test = 'single'
    T = Tetris(action_type = test,use_fitness = True,is_display = True)
    state = T.reset()
    for x in state:
        print(x)
        print('#######')
    if test == 'single':
        actionlist = ['Right','Left','Down','Rotate','HardDrop','Hold']
        print(actionlist)
        while True:
            actionID = input('key : ')
            if actionID not in ['0','1','2','3','4','5']:
                continue
            _,reward,done = T.step(int(actionID))
            #T.draw()
            print("Reward: " + str(reward))
            if done:
                print('Game Over.')
    else:
        valid = [ str(x) for x in range(53) ]
        while True:
            actionID = input('key : ')
            if actionID not in valid:
                continue
            state,_,done = T.step(int(actionID))
            for x in state:
                print(x.shape)
                print('#######')
            T.draw()
            if done:
                print('Game Over.')
