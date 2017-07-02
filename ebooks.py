import random
import re
import sys
import twitter
from local_settings import *

def connect():
    api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                          consumer_secret=MY_CONSUMER_SECRET,
                          access_token_key=MY_ACCESS_TOKEN_KEY,
                          access_token_secret=MY_ACCESS_TOKEN_SECRET)
    return api

def getBoardFromFile(statefilename):
    f = open(statefilename, 'r+')
    f.readline()
    i = 0
    board = [[0 for i in range(8)] for j in range(8)]
    for line in f:
        if int(line) == 1:
            board[i%8][i//8] = 1
        elif int(line) == 0:
            board[i%8][i//8] = 0
        else:
            board[i%8][i//8] = 5 #for error handling
        i+=1
    f.close()
    return board

def countNeighbors(x, y):
    count = 0
    if (board[x][(y-1)%8]==1):
        count +=1
    if (board[x][(y+1)%8]==1):
        count +=1
    if (board[(x-1)%8][y]==1):
        count +=1
    if (board[(x-1)%8][(y-1)%8]==1):
        count +=1
    if (board[(x-1)%8][(y+1)%8]==1):
        count +=1
    if (board[(x+1)%8][y]==1):
        count +=1
    if (board[(x+1)%8][(y-1)%8]==1):
        count +=1
    if (board[(x+1)%8][(y+1)%8]==1):
        count +=1
    return count

# Any live cell with fewer than two live neighbors dies, as if caused by under-population.
# Any live cell with two or three live neighbors lives on to the next generation.
# Any live cell with more than three live neighbors dies, as if by over-population.
# Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
def rules(x, y):
    if(board[x][y]==1):
        if (countNeighbors(x, y) < 2):
            return 0
        elif (1 < countNeighbors(x, y) < 4):
            return 1
        elif (countNeighbors(x, y) > 3):
            return 0
    elif(board[x][y]==0):
        if (countNeighbors(x, y) == 3):
            return 1
        else:
            return 0
    else:
        return 5


def getStringFromBoard(b):
    bs = ""
    for j in range(8):
        for i in range(8):
            if b[i][j] == 1:
                bs += '⚫️ '
            elif b[i][j] == 0:
                bs += '⚪️ '
            else:
                bs += '🔴 '
        bs += '\n'
    return bs

def getNextGenFromBoard():
    nextboard = [[0 for i in range(8)] for j in range(8)]
    for j in range(8):
        for i in range(8):
            nextboard[i][j] = rules(i, j)
    return nextboard

def writeNewGenToFile(statefilename):
    f = open(statefilename, 'w')
    for j in range(8):
        for i in range(8):
            f.write(str(nextboard[i][j]) + '\n')
    f.close()

if __name__=='__main__':
    api = connect()

    board = [[0 for i in range(8)] for j in range(8)]
    board = getBoardFromFile('state.txt')
    boardstr = ''
    boardstr = getStringFromBoard(board)

    nextboard = board
    nextboard = getNextGenFromBoard()
    nextboardstr = getStringFromBoard(nextboard)

    writeNewGenToFile('state.txt')

    print(api.GetUserTimeline(screen_name=gameoflife_bot, count=1, max_id=None, include_rts=False, trim_user=True, exclude_replies=True))
    print('Read from file:')
    print (boardstr)
    print('New gen to be tweeted and written:')
    print (nextboardstr)
    #status = api.PostUpdate(tweet)
