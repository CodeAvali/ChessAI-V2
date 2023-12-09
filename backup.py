#Live document for current work - Code Avali - Chessbot NEA

import numpy as np
import Moves_Inital
global board 
global White_Playing
global White_moves
global Black_moves 
global Moves_Tuple
global Blocked_Tuple
global Time_Stamp
space = ' '

# (3) ----------- Functions ------------------

def turn(Time_Stamp):
  if Time_Stamp % 2 == 1: 
    print(" Black Playing...") 
    Moves_Tuple = Black_moves
    return False, Moves_Tuple
  else:
    print(" White Playing...")
    Moves_Tuple = White_moves
    return True, Moves_Tuple

  #----

def action(move_to, move_from):

  #Normalise y to what is expected
  move_fromx, move_fromy = move_from.split(",")
  move_fromy = (int(move_fromy) - 9) * -1
  move_from = move_fromx + "," + str(move_fromy)

  move_tox, move_toy = move_to.split(",")
  move_toy = (int(move_toy) - 9) * -1
  move_to = move_tox + "," + str(move_toy)

  #Create into a tuple
  move_from = tuple((int(x)-1) for x in move_from.split(","))
  move_to = tuple((int(x)-1) for x in move_to.split(","))

  return move_to, move_from 

  #----

  #----

def absurd(move_to, move_from):
  Exception = ''
  if board[move_from[1]][move_from[0]] == Empty_:
    Exception += 'MOVE VALIDATION: There is no peice at inital'

  if White_Playing:
    if board[move_from[1]][move_from[0]] in BLACK:
      Exception += 'MOVE VALIDATION: You cannot move a black peice as White'
    elif board[move_to[1]][move_to[0]] in WHITE:
      Exception += 'MOVE VALIDATION: You can not move to a white peice as White'

  else:
    if board[move_from[1]][move_from[0]] in WHITE:
      Exception += 'MOVE VALDIATION: You cannot move a white peice as Black'
    elif board[move_to[1]][move_to[0]] in BLACK:
      Exception += 'MOVE VALDIATION: You cannot move to a black peice as White'

  if Exception != '':
    print(Exception, board[move_from[1]][move_from[0]])
    return False
  else: 
    return True 

  #----

def perform(move_to, move_from, board):

  global White_moves
  global Black_moves

  Moves_Tuple = []

  #Performing moves
  #print("TEST:", move_to, move_from)

  print("testing", move_from)

  peice = board[move_from[1]][move_from[0]]  #Collect moving peice into temp variable 
  board[(move_from[1])][(move_from[0])] = Empty_  #Remove moving peice
  board[(move_to[1])][(move_to[0])] = peice #Hence, write the peice into the location 

  #Hence; store new to respective holder
  if White_Playing:                       #TO DO Reverse order
    White_moves = clean(move_from, White_moves)
    #Black_moves = clean(move_to, Black_moves)        #Perform generation func 
  else:
    Black_moves = clean(move_from, Black_moves)
    #White_moves = clean(move_to, White_moves)        #Perform generation func     

  #Check for peice to generate new moves

  Moves_Tuple += property(move_to, peice, Moves_Tuple)

  if White_Playing:
    White_moves += Moves_Tuple    
  else:
    Black_moves += Moves_Tuple

  generate(move_from)

  return board 

  #----

def property(move_to, peice, Moves_Tuple):
  global White_moves
  global Black_moves

  print(peice)

  if peice in (W_Pawn, B_Pawn):
    print("PAWN move structure")
    Moves_Tuple += pawn((move_to[0], move_to[1]), White_Playing)
  elif peice in (W_Knig, B_Knig):
    print("KNIGHT move structure")
    Moves_Tuple += knight((move_to[0], move_to[1]))
  elif peice in (W_Rook, B_Rook):
    print("ROOK move structure")
    Moves_Tuple += straight((move_to[0], move_to[1]))
  elif peice in (W_Bish, B_Bish):
    print("BISHOP move structure")
    Moves_Tuple += diagonal((move_to[0], move_to[1]))
  elif peice in (W_Quee, B_Quee):
    print("QUEEN move strucuture")
    Moves_Tuple += diagonal((move_to[0], move_to[1]))
    Moves_Tuple += straight((move_to[0], move_to[1]))
  elif peice in (W_King, B_King): 
    print("KING move sructure")
    Moves_Tuple += adjecent((move_to[0], move_to[1]))

  return Moves_Tuple

  #----

def legal(move_to, move_from, move_space): 

  #print(move_space)

  for i in range(len(move_space)):
    #print(move_to, move_space[i][0])
    if move_from == move_space[i][0]:
      #print("TEST - 1")
      if move_to == move_space[i][1]:
        #print("TEST - 2")
        return True

  return False

  #----

def clean(delete, moves_structure):

  kept = []

  cleaned = tuple(delete)
  for i in range(len(moves_structure)):
    if moves_structure[i][0] != cleaned:
      kept.append(moves_structure[i])
    #else:
      #print(moves_structure[i][0], cleaned)

  return kept

  #----

def pawn(create, White_Playing):
  #from inital, collect the x and y components 

  create_x, create_y = create[0], create[1]

  #Hence, create a tuple containing new moves 

  new = []
  temp = ''

  create_y -= 1
  if (White_Playing) and not(blocked(create, create_x, create_y)): 
    temp = (create_x, create_y)  

    #For black
  create_y += 2
  if (not White_Playing) and not(blocked(create, create_x, create_y)):
    temp = (create_x, create_y)   
    #Add any additional conditions - Caputre; enpassant 

  if temp != '':
    temp = (create, tuple(temp)) #Need to sync for other player
    new.append(temp)

  #print(new)

  return new

  #---- 

def blocked(create, move_from_x, move_from_y):
  create_x, create_y = create[0], create[1]
  global Blocked_Tuple
  #print(move_from_x, move_from_y)

  if move_from_x < 0 or move_from_x > 7 or move_from_y < 0 or move_from_y > 7:
    return True  # Out of range


  if board[move_from_y][move_from_x] != Empty_:    #need to check that a range check is applied 
    print("YAY", board[create_y][create_x])    #will replace with an appropriate load 
    temp = (move_from_x, move_from_y)
    temp = (temp, tuple(create))
    Blocked_Tuple.append(temp)
    if (board[move_from_y][move_from_x] in (W_Pawn, B_Pawn)) and (board[create_y][create_x] in (W_Pawn, B_Pawn)):
      temp = (move_from_x, move_from_y)
      temp = (tuple(create), temp)
      #TO DO: remove pawn move from moves tuple - so that direct pawn captures are NOT possible 
      Blocked_Tuple.append(temp)

      #need to grab Moves_Tuple for opposing plater 
      delete(temp, Time_Stamp, True) 

    #TO DO: Check for own peices - reasonably to enforce rules; esp for horses and so on 
    return True 
  else:
    #print("AWW")
    return False 


  #---- 

def generate(move_from): 
  global Blocked_Tuple
  global White_moves
  global Black_moves 
  global KeyboardInterrupt
  global Blocked_Tuple
  #check to locate item being moved/deleted 

  for i in range(len(Blocked_Tuple)):
    #entry ticket
    #print("TEST:", Blocked_Tuple[i][0], move_from)
    #print("TEST2:", Blocked_Tuple[i][1], move_from)
    if Blocked_Tuple[i][0] == move_from: 
      #print("FIRE 1")

      #release blocked moves 

      moving_from = Blocked_Tuple[i][0]
      moving_to = Blocked_Tuple[i][1]

      peice = board[moving_from[1]][moving_from[0]]
      if peice in WHITE:
        #print("yo crazy1")
        White_moves += property(moving_from, peice, White_moves)   
      elif peice in BLACK: 
        #print("yo crazy 2")
        Black_moves += property(moving_from, peice, Black_moves)

    if Blocked_Tuple[i][1] == move_from:
      #print("FIRE 2")

      #release blocked moves

      moving_from = Blocked_Tuple[i][0]
      moving_to = Blocked_Tuple[i][1]

      peice = board[moving_from[1]][moving_from[0]]
      #print(moving_from[1], move_from[0])
      #print("PEICE:", peice)
      if peice in WHITE:
        #TO DO: need to rewrite into property func 
        #print("yo crazy 3")
        White_moves += property(moving_from, peice, White_moves)   
      elif peice in BLACK: 
        #print("yo crazy 4")
        Black_moves += property(moving_from, peice, Black_moves)  

  #----

def load(x_value, y_value, create, data_holder):
  temp = (x_value, y_value)
  temp = (create, tuple(temp))
  data_holder.append(temp)
  return data_holder

  #----

def delete(selection, timestamp, opposing):
  #grab opposinng moves_tuple
  global White_moves
  global Black_moves

  temp_moves = []
  #print("Time to delete!")

  White_Playing, test = turn(timestamp)
  #print(White_Playing)
  if (White_Playing is False) and (opposing is True):
    for i in range(len(White_moves)-1):
      #print("running")
      if White_moves[i] != selection:
        temp_moves.append(White_moves[i])
      #else:
        #print("Pawn blocked")
    White_moves = temp_moves

  if (White_Playing is True) and (opposing is True): 
    for i in range(len(Black_moves)-1):
      #print("running for black")
      if Black_moves[i] != selection:
        temp_moves.append(Black_moves[i])
      #else:
        #print("Pawn blocked")
    Black_moves = temp_moves


  #-----

def straight(create):
  #from inital, collect the x and y components

  create_x, create_y = create[0], create[1]

  #Hence, create a tuple of new moves

  new = []

  x_pointer = create_x
  while x_pointer < 7 and not(blocked(create, x_pointer + 1, create_y)):
    x_pointer += 1
    new += load(x_pointer, create_y, create, new)
  x_pointer = create_x
  while x_pointer > 0 and not(blocked(create, x_pointer - 1, create_y)):
    x_pointer -= 1 
    new += load(x_pointer, create_y, create, new)
  y_pointer = create_y 
  while y_pointer < 7 and not(blocked(create, create_x, y_pointer + 1)):
    y_pointer += 1
    new += load(create_x, y_pointer, create, new)
  y_pointer = create_y
  while y_pointer > 0 and not(blocked(create, create_x, y_pointer - 1)): 
    y_pointer -= 1 
    new += load(create_x, y_pointer, create, new)

  return new

  #----

def diagonal(create):

  #Hence, create a tuple of new moves
  new = []
  blocke
  create_x, create_y = create[0], create[1]

  x_pointer, y_pointer = create_x, create_y
  while (x_pointer, y_pointer < 7) and not blocked(create, x_pointer + 1, y_pointer + 1): 
    x_pointer += 1
    y_pointer += 1 
    new += load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer > 0 and y_pointer < 7) and not blocked(create, x_pointer - 1, y_pointer + 1):
    x_pointer -= 1
    y_pointer += 1 
    new += load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer > 0) and not blocked(create, x_pointer + 1, y_pointer - 1):
    x_pointer += 1
    y_pointer -= 1
    new += load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y 
  while (x_pointer, y_pointer > 0) and not blocked(create, x_pointer - 1, y_pointer - 1):
    x_pointer -= 1
    y_pointer -= 1
    new += load(x_pointer, y_pointer, create, new)

  return new 

  #----

def knight(create):

  print("Horsing around!")

  pivot = []
  new = []
  create_x, create_y = create[0], create[1]

  #hence, create tuple of new moves
  pivot.append((create_x + 2, create_y + 1))       #Will format later to a bland tuple 
  pivot.append((create_x - 2, create_y + 1))
  pivot.append((create_x + 2, create_y - 1))
  pivot.append((create_x - 2, create_y - 1))
  pivot.append((create_x + 1, create_y + 2))
  pivot.append((create_x - 1, create_y + 2))
  pivot.append((create_x + 1, create_y - 2))
  pivot.append((create_x - 1, create_y - 2))

  for i in range(len(pivot)-1):          #Range check; will likely format into indep function for consistency 
    if pivot[i][0] <= 8 and pivot[i][0] >= 0:
      if pivot[i][1] <= 8 and pivot[i][1] >= 0:
        temp = (create, tuple(pivot[i]))
        new.append(temp)

  #print(new)

  return new

  #----

def adjecent(create):

  print("kinging")

  pivot = []
  new = []
  create_x, create_y = create[0], create[1]

  #hence, create tuple of new moves
  pivot.append((create_x + 1, create_y + 1))        #Will format into a bland tuple later 
  pivot.append((create_x, create_y + 1))
  pivot.append((create_x - 1, create_y + 1))
  pivot.append((create_x + 1, create_y))
  pivot.append((create_x - 1, create_y))
  pivot.append((create_x + 1, create_y - 1))
  pivot.append((create_x, create_y - 1))
  pivot.append((create_x - 1, create_y - 1))

  for i in range(len(pivot)-1):                        #Range check implemented later
    if pivot[i][0] < 8 and pivot[i][0] >= 0 :
      if pivot[i][1] < 8 and pivot[i][1] >= 0:
        temp = (create, tuple(pivot[i]))
        new.append(temp)

  #print(new)

  return new


  #----

def belonging(move_from, Moves_Tuple):
  kept = []
  print(move_from, Moves_Tuple)
  for i in range(len(Moves_Tuple)-1):
    if move_from == Moves_Tuple[i][0]:
      kept.append(Moves_Tuple[i])


  print("Possible moves", kept)



#1. ----------- Board creation -------------------

W_Pawn = "♟︎"
B_Pawn = "♙"
W_Bish = '♝'
B_Bish = '♗' 
W_Knig = '♞'
B_Knig = '♘'
W_Rook = '♜'
B_Rook = '♖'
W_Quee = '♛' 
B_Quee = '♕'
W_King = '♚'  
B_King = '♔'
Empty_ = '_'

WHITE = [W_Pawn, W_Bish, W_Knig, W_Rook, W_Quee, W_King]
BLACK = [B_Pawn, B_Bish, B_Knig, B_Rook, B_Quee, B_King]

board = [[B_Rook, B_Knig, B_Bish, B_Quee, B_King, B_Bish, B_Knig, B_Rook],
        [B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn], 
        [W_Rook, W_Knig, W_Bish, W_Quee, W_King, W_Bish, W_Knig, W_Rook]]

Moves_Tuple = []
Blocked_Tuple = Moves_Inital.Blocked_moves
White_moves = Moves_Inital.White_moves
Black_moves = Moves_Inital.Black_moves


#2. ----------- Performing a move/MAIN GAMEPLAY LOOP --------------------

Playing = True
White_Playing = True 
print(np.matrix(board))
Time_Stamp = -1
while Playing:
  #Pass the turn to the next player 
  Time_Stamp += 1 
  White_Playing, Moves_Tuple = turn(Time_Stamp)

  #TESTS:
  #print("TEST, White moves:", White_moves)
  #print("TEST, Black moves:", Black_moves)

  # Asking the user for a move
  Valid = False
  print("OUTER LOOP")
  while not Valid:
    print("INNER LOOP")
    #Get inputs from users - using string literals to produce visual spacing
    #print("DEBUG: Move-Tuple", Moves_Tuple)
    move_from = input(f"location to move from, (x,y) {space*10}")
    move_to = input(f"location to move to, (x,y) {space*12}")     

    #Process accordingly and normalise
    move_to, move_from = action(move_to, move_from)
    belonging(move_from, Moves_Tuple)

    #print("TEST", move_to, move_from)

    #Perform exceptions; 
    Valid = legal(move_to, move_from, Moves_Tuple)
    #absurd(move_to, move_from)


  #Printing inputs
  board = perform(move_to, move_from, board)
  #print("Blocked moves", Blocked_Tuple)
  #print("White moves", White_moves)

  print(np.matrix(board))