import itertools
import random


class Offline:
    
    def __init__(self):
        
        return 
    
    def printBoard(self,board, rounds):
    	# print the chessboard
    	print('\n0    ' + board['0,0'] + '|' + board['1,0'] + '|' + board['2,0'])
    	print('     -+-+-')
    	print('1    ' + board['0,1'] + '|' + board['1,1'] + '|' + board['2,1'])
    	print('     -+-+-')
    	print('2    ' + board['0,2'] + '|' + board['1,2'] + '|' + board['2,2'])
    	print('\n     0 1 2\n')
    	if (rounds % 2) == 0:
    		print('-' * 60)
    		print(f'ROUND {int(rounds/2)+1}\n')
    	if rounds == -1:
    		print('-' * 60)
   
    def choosePieces(self):
    	# choose X or O
    	player1 = input('\nEnter pieces you(player1) like (X or O):')
    	while player1 not in ['X', 'O']:
    		print('\nInvalid input. Do again.')
    		player1 = input('\nEnter pieces you(player1) like (X or O):')
    	player2 = 'O' if player1 == 'X' else 'X'
    	return player1, player2
           
    def chooseInitiaties(self):
    	# choose the first to start
    	turn = random.choice(['X', 'O'])
    	print('\n' + turn + ' goes first!')
    	return turn
     
    def playerMove(self, correctInput, turn):
    	# store positions
    	move = input('\nTurn for ' + turn + '. Move on which space?(e.g.1,0):')
    	while move not in correctInput: 
    		print('\nInvalid input. Do again.')
    		move = input('\nTurn for ' + turn + '. Move on which space?(e.g.1,0):')
    	correctInput.remove(move)
    	return move
    
    def board2magic(self, board):
    	# Third-order magic square
    	tempBoard = board.copy()
    	magic3 = [4, 9, 2, 3, 5, 7, 8, 1, 6] # sum is 15 for every line
    	j = 0
    	for i in list(tempBoard.keys()):
    		tempBoard[str(magic3[j])] = tempBoard.pop(i)
    		j += 1
    	return tempBoard
    	
    def checkWin_sub(self, pieces):
    	# check the results 
    	comb = list(itertools.combinations(pieces, 3))
    	isWin = True if 15 in [sum(i) for i in comb] else False
    	return isWin
    
    def checkWin(self, board):
    	# check if one wins
    	tempBoard = self.board2magic(board)
    	Xpieces = [int(x[0]) for x in tempBoard.items() if 'X' in x[1]]
    	Opieces = [int(x[0]) for x in tempBoard.items() if 'O' in x[1]]
    	Xwin = self.checkWin_sub(Xpieces)
    	Owin = self.checkWin_sub(Opieces)
    	winner = 'N'
    	if Xwin == True:
    		winner = 'X'
    	elif Owin == True:
    		winner = 'O'
    	return winner

    def abValuation(self, board, player1, player2, computerTurn, alpha, beta):
    	# alpha-beta
    	tempBoard = board.copy()
    	tempCorrectInput = [x for x in tempBoard.keys() if tempBoard[x] == ' ']
    	winner = self.checkWin(tempBoard)
    	if winner == computerTurn: # computer wins
    		return 1
    	elif winner == 'N':
    		if not tempCorrectInput: # no winner
    			return 0
    	else: # player wins
    		return -1
    	for move in tempCorrectInput:
    		tempBoard[move] = player1
    		tempVal = self.abValuation(tempBoard, player2, player1, computerTurn, alpha, beta)
    		tempBoard[move] = ' '
    		if player1 == computerTurn: # Max 
    			if tempVal > alpha:
    				alpha = tempVal
    			if alpha >= beta:
    				return beta
    		else: # Min
    			if tempVal < beta:
    				beta = tempVal
    			if beta <= alpha:
    				return alpha
    	if player1 == computerTurn:
    		value = alpha
    	else:
    		value = beta
    	return value
    
    def computerMove(self, board, turn, correctInput, computerTurn):
    	# computer plays
    	print("Computer's turn. Computer decides to move on: ", end = '')
    	best = -2
    	strategy = []
    	player1 = computerTurn
    	player2 = 'O' if player1 == 'X' else 'X'
    	for possibleMove in correctInput:
    		board[possibleMove] = player1
    		val = self.abValuation(board, player2, player1, computerTurn, -2, 2) #深度优先
    		board[possibleMove] = ' '
    		if val > best:
    			best = val
    			strategy = [possibleMove]
    		if val == best:
    			strategy.append(possibleMove)
    	move = random.choice(strategy)
    	correctInput.remove(move)
    	print(move)
    	return move
    
    def main(self,mode):
        game_run = True
        while game_run:
            theBoard = {'0,0': ' ', '1,0': ' ', '2,0': ' ',
                          '0,1': ' ', '1,1': ' ', '2,1': ' ',
                          '0,2':' ','1,2': ' ', '2,2': ' '}
            correctInput = list(theBoard.keys())
            #mode = chooseMode()
            player1, player2 = self.choosePieces()
            turn = self.chooseInitiaties()
            for rounds in range(9):
                self.printBoard(theBoard, rounds)
                if mode == 1:
                    move = self.playerMove(correctInput, turn)
                else:
                    if turn == player1:
                        move = self.playerMove(correctInput, turn)
                        if move == "quit":
                            game_run  = False
                    else: #turn == player2 
                        move = self.computerMove(theBoard, turn, correctInput, player2)
                if game_run:
                    theBoard[move] = turn
                    turn = 'O' if turn == 'X' else 'X'
                    winner = self.checkWin(theBoard)
                    if winner == 'N':
                        if rounds == 8:
                            print('\nDraw!')
                    else:
                        print("\n'" + winner + "'wins!")
                        break
            if game_run:
                self.printBoard(theBoard, -1)
                if input('Enter y to start a new game. Others to quit the game and go back to the menu.') != 'y':
                    break
 
if __name__ == '__main__':
    game = Offline()
    game.main(mode)


