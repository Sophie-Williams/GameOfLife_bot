import random
import re
import sys
import twitter
#Get tokens and keys to connect to the right account
from local_settings import *

#Connect to twitter API
def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api

#Parses previous board tweet into string of Xs and _s, then 2D array of 1s and 0s
def getBoardFromText(boardtext):
    board = [[0 for i in range(8)] for j in range(8)] #create new blank board
    boardtext = re.sub(r'\n','', boardtext) #take out new lines.
    boardtext = re.sub(r'\"|\(|\)', '', boardtext) #take out quotes.
    boardtext = boardtext.replace("🔵", "X")    #live
    boardtext = boardtext.replace("⚪️", "_")    #dead
    boardtextlist = list(boardtext)
    for j in range(8):
        for i in range(8):
            #live cell
            if (boardtextlist[i+(j*8)] == 'X'):
                board[i][j] = 1
            #dead cell
            elif (boardtextlist[i+(j*8)] == '_'):
                board[i][j] = 0
            #for debugging
            else:
                board[i][j] = 5
    return board

#Returns a count of how many of a cell's 8 neighbors are alive
#Modular, so that board wraps
def countNeighbors(x, y):
    count = 0
    if (board[x][(y-1)%8]==1): #W
        count +=1
    if (board[x][(y+1)%8]==1): #E
        count +=1
    if (board[(x-1)%8][y]==1): #N
        count +=1
    if (board[(x+1)%8][y]==1): #S
        count +=1
    if (board[(x-1)%8][(y-1)%8]==1): #NW
        count +=1
    if (board[(x-1)%8][(y+1)%8]==1): #SW
        count +=1
    if (board[(x+1)%8][(y-1)%8]==1): #NE
        count +=1
    if (board[(x+1)%8][(y+1)%8]==1): #SE
        count +=1
    return count

# Any live cell with fewer than two live neighbors dies, as if caused by under-population.
# Any live cell with two or three live neighbors lives on to the next generation.
# Any live cell with more than three live neighbors dies, as if by over-population.
# Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
# Returns live or dead cell
def rules(x, y):
    #If alive...
    if(board[x][y]==1):
        if (countNeighbors(x, y) < 2):
            return 0
        elif (1 < countNeighbors(x, y) < 4):
            return 1
        elif (countNeighbors(x, y) > 3):
            return 0
    #If dead...
    elif(board[x][y]==0):
        if (countNeighbors(x, y) == 3):
            return 1
        else:
            return 0
    #For debugging
    else:
        return 5

#Generates board string from 2D array of 1s and 0s
def getStringFromBoard(b):
    bs = ""
    for j in range(8):
        for i in range(8):
            if b[i][j] == 1:
                bs += '🔵'
            elif b[i][j] == 0:
                bs += '⚪️'
            #For debugging
            else:
                bs += '🔴'
        bs += '\n'
    return bs

#Generate next board according to the rules at each cell
def getNextGenFromBoard():
    nextboard = [[0 for i in range(8)] for j in range(8)]
    for j in range(8):
        for i in range(8):
            nextboard[i][j] = rules(i, j)
    return nextboard

#For when a board becomes blank or locked
def generateRandomBoard():
    randboard = [[0 for i in range(8)] for j in range(8)]
    for j in range(8):
        for i in range(8):
            randboard[i][j] = random.randint(0, 1)
    return randboard

if __name__=='__main__':
    api = connect()

    #Retrieve last board genenration.
    boardtext = api.GetUserTimeline(screen_name='gameoflife_bot', count=1, max_id=None, include_rts=False, trim_user=True, exclude_replies=True)[0].text
    if '⚪️' not in boardtext:
        #Last board was a text message. Generate random board.
        nextboardstr = getStringFromBoard(generateRandomBoard())
        print(nextboardstr)
        status = api.PostUpdate(nextboardstr)
        sys.exit()
    board = [[0 for i in range(8)] for j in range(8)]
    board = getBoardFromText(boardtext)
    boardstr = ''
    boardstr = getStringFromBoard(board)

    nextboard = board
    nextboard = getNextGenFromBoard()
    nextboardstr = getStringFromBoard(nextboard)

    #No live cells in last board
    if '🔵' not in boardtext:
        nextboardstr = 'This population is extinct, so I\'ll generate a new board randomly.'
    #Generation next generation produced an identical board, meaning the configuration is stable.
    if nextboardstr == boardstr:
        nextboardstr = 'Population is locked, so I\'ll generate a new board randomly.'

    print(nextboardstr)
    #Tweet board
    status = api.PostUpdate(nextboardstr)
