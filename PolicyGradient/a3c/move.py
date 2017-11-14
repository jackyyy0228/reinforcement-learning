#define pieces and movement

ipieces=[[[0,0,1,0],[0,0,1,0],[0,0,1,0],[0,0,1,0]],
         [[0,0,0,0],[0,0,0,0],[1,1,1,1],[0,0,0,0]],
         [[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]],
         [[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]]]
opieces=[[[0,0,0,0],[0,2,2,0],[0,2,2,0],[0,0,0,0]],
         [[0,0,0,0],[0,2,2,0],[0,2,2,0],[0,0,0,0]],
         [[0,0,0,0],[0,2,2,0],[0,2,2,0],[0,0,0,0]],
         [[0,0,0,0],[0,2,2,0],[0,2,2,0],[0,0,0,0]]]
jpieces=[[[0,3,3,0],[0,0,3,0],[0,0,3,0],[0,0,0,0]],
         [[0,0,0,0],[0,3,3,3],[0,3,0,0],[0,0,0,0]],
         [[0,0,3,0],[0,0,3,0],[0,0,3,3],[0,0,0,0]],
         [[0,0,0,3],[0,3,3,3],[0,0,0,0],[0,0,0,0]]]
lpieces=[[[0,0,4,0],[0,0,4,0],[0,4,4,0],[0,0,0,0]],
         [[0,0,0,0],[0,4,4,4],[0,0,0,4],[0,0,0,0]],
         [[0,0,4,4],[0,0,4,0],[0,0,4,0],[0,0,0,0]],
         [[0,4,0,0],[0,4,4,4],[0,0,0,0],[0,0,0,0]]]
zpieces=[[[0,5,0,0],[0,5,5,0],[0,0,5,0],[0,0,0,0]],
         [[0,0,0,0],[0,5,5,0],[5,5,0,0],[0,0,0,0]],
         [[0,5,0,0],[0,5,5,0],[0,0,5,0],[0,0,0,0]],
         [[0,0,5,5],[0,5,5,0],[0,0,0,0],[0,0,0,0]]]
spieces=[[[0,0,6,0],[0,6,6,0],[0,6,0,0],[0,0,0,0]],
         [[0,0,0,0],[0,6,6,0],[0,0,6,6],[0,0,0,0]],
         [[0,0,6,0],[0,6,6,0],[0,6,0,0],[0,0,0,0]],
         [[6,6,0,0],[0,6,6,0],[0,0,0,0],[0,0,0,0]]]
tpieces=[[[0,0,7,0],[0,7,7,0],[0,0,7,0],[0,0,0,0]],
         [[0,0,0,0],[0,7,7,7],[0,0,7,0],[0,0,0,0]],
         [[0,0,7,0],[0,0,7,7],[0,0,7,0],[0,0,0,0]],
         [[0,0,7,0],[0,7,7,7],[0,0,0,0],[0,0,0,0]]]
lspieces=[8,8,8,8,8,8,8,8,8,8]#this is the lines sent piece aka garbage lines
zeropieces=[[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
         [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
         [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],
         [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]]
allpieces=[ipieces,opieces,jpieces,lpieces,zpieces,spieces,tpieces]
def checkCombo(combo,sent):
    if combo>0:
        if combo<=8:
            sent+=(combo+1)//2
        else: sent+=4
    return sent
    
def blockmoving(grid, block, px,py):
    if collideDown(grid, block,px,py)==True:
        for x in range(4):
            for y in range (4):
                if block[x][y]>0:
                    num=block[x][y]
                    if -1<px+x<10 and -1<py+y<20:
                        grid[px+x][py+y]=num
        return False
    else:
        return True
#the ghost block piece

#move right function
#when respective right buttons are pressed
#x pos of the block moves over 1unit right
def moveRight(px,py,px2,py2):
    if keys[K_h]:
        if collideRight(grid1,block1,px,py)==False:    
            px+=1
    if keys[K_RIGHT]:
        if collideRight(grid2,block2,px2,py2)==False:
            px2+=1
    return [px,py,px2,py2]

#move left function
#when respective left buttons are pressed
#x pos of the block moves over 1unit left
def moveLeft(px,py,px2,py2):
    if keys[K_f]:
        if collideLeft(grid1,block1,px,py)==False:
            px-=1
    if keys[K_LEFT]:
        if collideLeft(grid2,block2,px2,py2)==False:
            px2-=1
    return [px,py,px2,py2]


#move down function
#when respective down buttons are pressed
#y pos of the block moves down 1unit
#as long as there is nothing underneath
def moveDown(px,py,px2,py2):

    if keys[K_g]:
        if collideDown(grid1,block1,px,py)==False:
            py+=1
    if keys[K_DOWN]:
        if collideDown(grid2,block2,px2,py2)==False:
            py2+=1
    return [px,py,px2,py2]


#collidedown function
#for i in range 4(y position)
#if px+y=20 then collidedown =true
#used for move down and rotation collision
def collideDown(grid,block,px,py):
    for x in range(4):
        for y in range(4):
            if block[x][y]>0:
                if -1<px+x<10 and -1<py+y<20:
                    n=block[x][y]
                    if py+y+1==20:
                        return True
                    if grid[px+x][py+y+1]>0:
                        if y<3 and block[x][y+1]==0:
                            return True
                        if y==3:
                            return True

    return False


#collideleft function
#for i in range 4(x positions)
#if blockx +x =0 then collide left = True
#used for moving block and rotation collision
def collideLeft(grid,block,px,py):
    for x in range (4):
        for y in range (4):
            if block[x][y]>0:
                if px+x-1==-1:
                    return True
                if py+y >=0 and grid[px+x-1][py+y]>0:
                    if x>0 and block[x-1][y]==0:
                        return True
                    if x==0:
                        return True
    return False

#collideright function
#for i in range 4(x positions)
#if blockx +x +1>9 then collide left = True
#plus 1 is there cuz pxis on left of the piece
#used for moving block and rotation collision
def collideRight(grid,block,px,py):
    for x in range (4):
        for y in range (4):
            if block[x][y]>0:
                if px+x+1>9:
                    return True
                if py+y >= 0 and grid[px+x+1][py+y]>0:
                    if x<3 and block[x+1][y]==0:
                        return True
                    if x==3:
                        return True
    return False
#send function
#sending number of lines
def send(grid,gridb,sent,tempsend):
    x=0
    #tempsend = send then send increases
    #lines sent is the difference between these two
    #lines p1 sends affects p2grid and vice versa
    garbage=sent-tempsend
    for y in range (1,garbage+1):
        if grid[0][-y]==8:
            x+=1
    for i in range (1,x+1):
        for x in range (10):
            del grid[x][-i]
            grid[x]=[0]+grid[x]
    for y in range (garbage-x):    
        for i in range(10):
            del(gridb[i][y])#deletes top of grid
            gridb[i]=gridb[i]+[8]#adds garbage lines at the bottom
    return grid,gridb

#ko Function
def KO(grid,block,px,py,time):
    ko=False
    #if your grid hits the top ko =true
    for x in range (4):
        for y in range (4):
            if block[x][y]>0:
                if py+y<0:
                    ko=True
    #if ko = true then all the garbage lines
    #are deleted. If there are no garbage lines then you lose
    if ko==True:
        garbage=0
        for y in range (20):
            for x in range (10):
                if grid[x][y]==8:
                    garbage+=1
                    grid[x].remove(grid[x][y])
                    grid[x]=[0]+grid[x]
        if garbage==0:
            time=0     
    return [grid,ko,time]

#def win(grid,gridb,kO,sent):
    
#clear lines function
#when you send lines the grid clears the line
def clear(grid,gridb,block,b,sent,tempsend,combo):
    global tempsend1
    global tempsend2
    cleared=0
    tempsend=sent
    add=3
    for y in range (20):
        row=0#starts checking from row zero
        for x in range (10):
            if grid[x][y]>0 and grid[x][y]<8:
                row+=1
        if row==10:
            add-=1
            #print tspinCheck(grid,block,px,py,b)
            if tspinCheck(grid,block,px,py,b)==True:#for tspin sends more lines than actually cleared
                sent+=add
            cleared+=1
            for i in range (10):
                del(grid[i][y])#deletes cleared lines
                grid[i]=[0]+grid[i]#adds a row of zeros to the grid
                    
    if cleared>=1:#for sending lines
        combo+=1
        if cleared==4:#a tetris
            #screen.blit(tetris,(330,465))
            sent+=4 
        for i in range (1,4):#single, double, triple
            if cleared==i:
                sent+=(i-1)
    if cleared==0:#no lines cleared= no combo
        #screen.blit(back,(315,440))
        combo=-1
    sent=checkCombo(combo,sent)#linessent increases with amount of combos
    return (combo,sent,tempsend,cleared)


#getPositon function
#gets the position of the block falling
#position is sorted and returned to be used
#for the falling blocks
def getPositions(block,px,py):  
    positions=[]
    for x in range(4):
        for y in range (4):
            if block[x][y]>0:
                positions.append((px+x,py+y))
                sorted(positions, key=lambda pos: pos[1])
    return positions

#rotatecollision function
#when respective rotate buttons are pressed
#this function checks if collide(left right or down has occured)
#if it hasnt then rotation occurs
def rotateCollide(grid,block,px,py):
    for x in range (4):
        for y in range (4):
            if block[x][y]>0:
                if -1<px+x<10 and -1<py+y<20:
                    if grid[px+x][py+y]>0: 
                        return ["both",0]
                if px+x<0:
                    return ["left",x]
                if px+x>9:
                    return ["right",x]
                if py+y>19:
                    return ["down",0]
           
    return [False,0]

#this function allows you to slide in a piece at the last minute
#allows you to move over 1 unit to the left or right
def moveOver(grid,block,px,py):
    for x in range (4):
        for y in range (4):
            if block[x][y]>0:
                if px+x>9:
                    px=moveOver(grid,block,px-1,py)[0]
                    py=moveOver(grid,block,px-1,py)[1]
                if px+x<0:
                    px=moveOver(grid,block,px+1,py)[0]
                    py=moveOver(grid,block,px+1,py)[1]
                    
    return (px,py)            

#this function checks if a tspin has occured
#checks all possible tspin positions
#then spins the t piece into the spot
def tspinCheck(grid,block,px,py,b):
    if collideDown(grid,block,px,py)==True:
        if b==tpieces:
            pos=getPositions(block,px,py)
            if px+2<10 and py+3<20:
                if grid[px][py+1]>0 and grid[px][py+3]>0 and grid[px+2][py+3]>0:

                    return True
                elif grid[px][py+3]>0 and grid[px+2][py+3]>0 and grid[px+2][py+1]>0:

                    return True
    return False
#this function rotates the piece
#when rotation button is hit the next grid in the piece list becomes the piece
def rotate(grid,block,px,py,b,tspin):
    c=b.index(block)
    y=(c+1)%4
    block=b[y]
    collision=rotateCollide(grid,block,px,py)#checks for collisions
    x=collision[0]
    d=collision[1]
    if x=="both":
        if rotateCollide(grid,b[y],px,py+1)==False:
            py+=1
        else:
            a=1
            for i in range (2):                
                if rotateCollide(grid,b[y],px,py-i)[0]=="both":
                    #print "yes"
                    py-=a
                    if i==1:
                        block=b[c]
                        py+=2
                if rotateCollide(grid,b[y],px,py-i)[0]==False:
                    break
    if x=="left":
        px=moveOver(grid,block,px,py)[0]#px becomes moveover move left
    if x=="right":
        px=moveOver(grid,block,px,py)[0]#px becomes moveover move right
    if x=="down":
        py-=1
    if tspinCheck(grid,block,px,py,b)==True:
        tspin=1
    return [block,px,py,tspin]

#this function drops the piece as far as it can go until
#it collides with a piece below it
def hardDrop(grid,block,px,py):
    y=0
    x=0
    if collideDown(grid,block,px,py)==False:
        x=1
    if x==1:
        while True:
            py+=1
            y+=1
            if collideDown(grid,block,px,py)==True:
                break
        
    return y

#this function enables you to hold a piece
def hold(grid,b,held,nextlist,piecelist):
    #when piece is held the block at pos[0]
    #in the nextlist becomes the newpiece
    if held==[]:
        held=b
        b=nextlist[0]
        nextlist.remove(nextlist[0])
        if len(piecelist)==0:
            piecelist=[ipieces,opieces,jpieces,lpieces,zpieces,spieces,tpieces]
        nextlist.append(choice(piecelist))
        piecelist.remove(nextlist[-1])
    #the piece switches with the held piece     
    else:
        b,held=held,b
        
    return [b,held,nextlist,piecelist] 

#this function creates a newblock to be appended to the nextlist
def newBlock(grid,block,b,nextlist,piecelist):
    if len(piecelist)>0:
        n=randint(0,len(piecelist)-1) #makes chooosing random
        nextlist.append(piecelist[n]) #appends at the nth piece to the nextlist
        piecelist.remove(piecelist[n])#takes that piece out so there are no repeats

    else:
        piecelist=[ipieces,opieces,jpieces,lpieces,zpieces,spieces,tpieces]#rests piecelist
        nextlist.append(choice(piecelist))#add to nextlist
        piecelist.remove(nextlist[-1])#removes the last item in the next list
    b=nextlist[0]#firt grid of four 
    nextlist.remove(nextlist[0])
    return [b,nextlist,piecelist]


    #counters for various reasons               
    #improve timing of the game
    counter=0
    movecounter=0
    downcounter=0
    stopcounter1=0
    stopcounter2=0
    #piecelist p1
    piecelist1=[ipieces,opieces,jpieces,lpieces,zpieces,spieces,tpieces]
    #piecelist p2
    piecelist2=[ipieces,opieces,jpieces,lpieces,zpieces,spieces,tpieces]
    #choices of the list
    b1=choice(piecelist1)
    b2=choice(piecelist2)
    #removes the choices
    piecelist1.remove(b1)
    piecelist2.remove(b2)
    nextlist1=[]#list of 5 pieces that are going to come next
    nextlist2=[]
    block1=b1[0]#first piece in list
    block2=b2[0]#first piece in list
    tspin1=0 #for t spin
    tspin2=0 #for t spin
    #for "KO"
    KO1=0 
    KO2=0
    #DEFINING VARIABLES
    cleared1=0
    cleared2=0
    kocounter1=0
    kocounter2=0
    for i in range (5):
        nextlist1.append(choice(piecelist1))#gets five random pieces from the piecelist
        nextlist2.append(choice(piecelist2))    
        piecelist1.remove(nextlist1[-1])    #removes from piecelist.
        piecelist2.remove(nextlist2[-1])

    #main loop
    while running:
        #battlemusic.play()#plays music
        keys=key.get_pressed()#gets pressed keys
        counter+=1
        movecounter+=1
        downcounter+=1
        
        if counter==65:#timing
            if collideDown(grid1,block1,px,py)==False:
                py+=1
            # must check if the piece CAN move down, if not copy to grid
            if collideDown(grid2,block2,px2,py2)==False:
                py2+=1
            counter=0#reset counter

        for evt in event.get():
            if evt.type==QUIT:
                running=False
            if evt.type==KEYDOWN:
                if evt.key==K_s:#rotating p1
                    thing=rotate(grid1,block1,px,py,b1,tspin1)#stuff you need when rotating
                    #rotate returs 4 items 
                    block1=thing[0]
                    px=thing[1]
                    py=thing[2]
                    tspin1=thing[3]
                    print(tspin1)
                if evt.key==K_UP:#rotating p2
                    thing=rotate(grid2,block2,px2,py2,b2,tspin2)#parameters
                    #rotate returs 4 items 
                    block2=thing[0]
                    px2=thing[1]
                    py2=thing[2]
                    tspin2=thing[3]
                if evt.key==K_t:#harddrop p1
                    y=hardDrop(grid1,block1,px,py)#parameters
                    py+=y
                    stopcounter1=50
                if evt.key==K_SPACE:#harddrop p2
                    y=hardDrop(grid2,block2,px2,py2)#parameters
                    py2+=y
                    stopcounter2=50
                if evt.key==K_RSHIFT:#holding p1
                    x=hold(grid1,b1,held1,nextlist1,piecelist1)#parameters
                    px=4 #rests x and y coords
                    py=-2
                    #hold returns 4 items
                    #assignning variables to each item
                    b1=x[0]
                    block1=b1[0]
                    held1=x[1]
                    nextlist1=x[2]
                    piecelist1=x[3]
                if evt.key==K_LSHIFT:#holding p2
                    x=hold(grid2,b2,held2,nextlist2,piecelist2)#parameters
                    #hold return 4 items
                    #assignning variables to each item
                    px2=4
                    py2=-2
                    b2=x[0]
                    block2=b2[0]
                    held2=x[1]
                    nextlist2=x[2]
                    piecelist2=x[3]
       
        if collideDown(grid1,block1,px,py)==True:
            stopcounter1+=1#counter for collidedown 
        if collideDown(grid2,block2,px2,py2)==True:
            stopcounter2+=1#counter for collidedown
        if kocounter1>=1:
            kocounter1+=1
        if kocounter2>=1:
            kocounter2+=1
        if stopcounter1>=30:#adds adequate delay  
            if blockmoving(grid1,block1,px,py)==False:
                z=send(grid1,grid2,sent1,tempsend1)#parameters
                grid1=z[0]#1 item returned
                grid2=z[1]#2nd item returned
                tempsend1=sent1#needed for subtraction later
                newchie1=clear(grid1,grid2,block1,b1,sent1,tempsend1,combo1)#parameters for clear
                oldcombo1=combo1
                cleared1=newchie1[3]#4 item returned
                tempsend1=newchie1[2]#3rd
                sent1=newchie1[1]#2nd
                combo1=newchie1[0]#1st
                
                x=KO(grid1,block1,px,py,time)#parameters
                grid1=x[0]#1st item returned
                time=x[2]#3rd item returned
                if x[1]==True: #2nd item for KOing
                    delaytime=time
                    oldko2=KO2

                    screen.blit(kos[KO2],(426,235))#
                    KO2+=1
                    kocounter2+=1
                
                x=newBlock(grid1,block1,b1,nextlist1,piecelist1)#parameters
                b1=x[0]#item1
                block1=b1[0]#item1 in b1
                nextlist1=x[1]#item2
                piecelist1=x[2]#item3
                px=4#rests x and y
                py=-2
                stopcounter1=0#back to zero
        if stopcounter2>=30:#delay  
            if blockmoving(grid2,block2,px2,py2)==False:
                z=send(grid2,grid1,sent2,tempsend2)#parameters
                grid2=z[0]#1 item returned
                grid1=z[1]#2nd item returned
                tempsend2=sent2#needed for subtraction later              
                newchie2=clear(grid2,grid1,block2,b2,sent2,tempsend2,combo2)#parameters for clear
                oldcombo2=combo2
                cleared2=newchie2[3]#4th item returned
                tempsend2=newchie2[2]#3rd item returned
                sent2=newchie2[1]#2nd item returned
                combo2=newchie2[0]#1st item returned
                x=KO(grid2,block2,px2,py2,time)#parameters
                
                grid2=x[0]#1st item returned
                time=x[2]#3rd item returned 
                if x[1]==True:#2nd item, for kOing
                    delaytime=time 
                    oldko1=KO1

                    if x[1]==True:
                        delaytime=time

                        oldko1=KO1

                        screen.blit(kos[KO1],(44,235))
                        KO1+=1
                        kocounter1+=1


                x=newBlock(grid2,block2,b2,nextlist2,piecelist2)#parameters

                b2=x[0]#item1
                block2=b2[0]#item1 in b1
                nextlist2=x[1]#item2
                piecelist2=x[2]#item3
                px2=4#resets x and y
                py2=-2
                stopcounter2=0 #back to zero

        #parameters for getting position of
        #falling block
        positions1=getPositions(block1,px,py)
        positions2=getPositions(block2,px2,py2)     

        if movecounter==2:
             #done to eliminate the global aspect of px,py
             #yolo1 returns px,py,px2,py2
             yolo1 = moveLeft(px,py,px2,py2)
             px=yolo1[0]
             py=yolo1[1]
             px2=yolo1[2]
             py2=yolo1[3]
             #done to eliminate the global aspect of px,py
             #yolo1 returns px,py,px2,py2
             yolo2 = moveRight(px,py,px2,py2)
             px=yolo2[0]
             py=yolo2[1]
             px2=yolo2[2]
             py2=yolo2[3]
             movecounter=0
        if downcounter==2:
            #done to eliminate the global aspect of px,py
            #yolo1 returns px,py,px2,py2
            yolo3 = moveDown(px,py,px2,py2)
            px=yolo3[0]
            py=yolo3[1]
            px2=yolo3[2]
            py2=yolo3[3]
            downcounter=0
        
        
        if KO2-oldko2==1:
            b=screen.copy()
            screen.blit(ko,(140,233))
            display.flip()
            if kocounter2>=75:
                kocounter2=0
                oldko2=KO2
                time=delaytime
                screen.blit(b,(0,0))
                if KO2==3:
                    return [b,"endgame",2]
        #print KO1,oldko1

        if KO1-oldko1==1:
            
            a=screen.copy()
            screen.blit(ko,(527,233))
            
            display.flip()
            if kocounter1>=75:
                kocounter1=0
                oldko1=KO1
                time=delaytime
                screen.blit(a,(0,0))
                if KO1==3:
                    return [a,"endgame",1]
        else:
            drawScreen()
        dont_burn_my_cpu.tick(30)
        display.flip()
        

        
        if time>=0:
            time-=timer2p.tick()
        else:
            a=screen.copy()
            if KO2>KO1: #Checks who is the winner of the game
                return [a,"endgame",2]#a is screebn.copy,endgame ends the game,2 is player 2 wins
            if KO1>KO2:
                return [a,"endgame",1]#a is screebn.copy,endgame ends the game,1 is player 1 wins
            if KO1==KO2:
                if sent2>sent1:
                    return [a,"endgame",2]#a is screebn.copy,endgame ends the game,2 is player 2 wins
                if sent1>sent2:
                    return [a,"endgame",1]#a is screebn.copy,endgame ends the game,1 is player 1 wins

        drawTime2p(time)
        if combo1-oldcombo1==1: #draws the combo picture
            drawCombo(combo1,164,190)
        if combo2-oldcombo2==1:
            drawCombo(combo2,535,190)
       
        

        #time goes until it hits zero
        #when it hits zero return endgame screen
        
        display.flip()
    quit()

