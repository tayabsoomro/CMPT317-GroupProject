
import random
from board import Board, Piece
from gamePlay import minimax, alphaBeta
from evaluate import Evaluate
from hashTable import HashTable
from gameController import Game, runGame

def main():
    runGame(3, alphaBeta)

if __name__ == '__main__':
    main()
