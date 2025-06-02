from C4Logic import Board 

b = Board(6, 7, 4)  # Example for a 6x7 board with 4 in a row to win
print("Initial Board:")

b.reset()
b[0][0] = 1
b[1][0] = 1
b[2][0] = 1
b[3][0] = 1  
assert b.get_game_ended() == 1

b.reset()
b[0][0] = 1
b[0][1] = 1
b[0][2] = -1
b[0][3] = -1
b[0][4] = -1
b[0][5] = -1  
assert b.get_game_ended() == -1

b.reset()
b[0][0] = 1
b[1][1] = 1
b[2][2] = 1
b[3][3] = 1
assert b.get_game_ended() == 1

b.reset()
b[0][3] = 1
b[2][1] = 1
b[1][2] = 1
b[3][0] = 1
assert b.get_game_ended() == 1

b.reset()
assert b.get_game_ended() == 0
