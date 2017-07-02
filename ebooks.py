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

def rules(x, y):
    return board[x][y]+7

def getStringFromBoard(b):
    bs = ""
    for j in range(8):
        for i in range(8):
            if b[i][j] == 1:
                bs += '⚫️'
            elif b[i][j] == 0:
                bs += '⚪️'
            else:
                bs += '🔴'
        bs += '\n'
    return bs

def getNextGenFromBoard(b):
    nextboard = board
    for j in range(8):
        for i in range(8):
            nextboard[i][j] = rules(i, j)
            print(str(nextboard[i][j]))
    return nextboard

if __name__=='__main__':
    api = connect()

    board = [[0 for i in range(8)] for j in range(8)]
    board = getBoardFromFile('state.txt')
    boardstr = ''
    boardstr = getStringFromBoard(board)

    nextboard = board
    nextboard = getNextGenFromBoard()
    nextboardstr = getStringFromBoard(nextboard)

    print (boardstr)
    print (nextboardstr)
    #status = api.PostUpdate(tweet)
