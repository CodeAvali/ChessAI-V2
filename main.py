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
blocked_trait = False

# (2) --------- Essential Functions ------------

def turn(Time_Stamp):
  #INDEPENDENT: Determines the current players turn, depending on time_stamp; and loads Moves_Tuple
  
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
  #INDEPENDENT: Normalises the actions into an board addressable form 

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

def load(x_value, y_value, create, data_holder):
  global White_moves
  global Black_moves
  #INDEPENDENT: Shorthand for creating an action when needed

  temp = (x_value, y_value)
  temp = (create, tuple(temp))
  data_holder.append(temp)
  return data_holder

  #----

def perform(move_to, move_from, board):
  global White_moves
  global Black_moves
  #Perform the required action - Clean and call forth explosion system

  Moves_Tuple = []

  #Performing moves
  #print("TEST:", move_to, move_from)

  #print("testing", move_from)

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

  #generate(move_from)

  return board 

  #----

# (3) --------- Movement properties -----------

def property(move_to, peice, Moves_Tuple):
  #MAIN: Calls forth movement properties; to return legal moves etc

  #print(peice)

  if peice in (W_Pawn, B_Pawn):
    #print("PAWN move structure")
    Moves_Tuple += pawn((move_to[0], move_to[1]), White_Playing)
  elif peice in (W_Knig, B_Knig):
    #print("KNIGHT move structure")
    Moves_Tuple += knight((move_to[0], move_to[1]))
  elif peice in (W_Rook, B_Rook):
    #print("ROOK move structure")
    Moves_Tuple += straight((move_to[0], move_to[1]), False)
  elif peice in (W_Bish, B_Bish):
    #print("BISHOP move structure")
    Moves_Tuple += diagonal((move_to[0], move_to[1]), False)
  elif peice in (W_Quee, B_Quee):
    #print("QUEEN move strucuture")
    Moves_Tuple += diagonal((move_to[0], move_to[1]), False)
    Moves_Tuple += straight((move_to[0], move_to[1]), False)
  elif peice in (W_King, B_King): 
    #print("KING move sructure")
    Moves_Tuple += adjecent((move_to[0], move_to[1]))

  return Moves_Tuple

  #----

def pawn(create, White_Playing):
  global blocked_trait 
  #from inital, collect the x and y components 

  create_x, create_y = create[0], create[1]

  #Hence, create a tuple containing new moves 

  new = []
  temp = ''

  create_y -= 1
  #print(blocked(create, create_x, create_y))
  #print(board[create_y][create_x])

  blocked_trait = False
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

  #print(temp)
  #print(new)

  return new

  #----

def straight(create, gen):
  #from inital, collect the x and y components

  create_x, create_y = create[0], create[1]
  #print("Straight movement")

  #Hence, create a tuple of new moves

  new = []

  x_pointer = create_x
  while x_pointer < 7 and not(blocked(create, x_pointer + 1, create_y)):
    x_pointer += 1
    new = load(x_pointer, create_y, create, new)
  refresh()
  #new = load(x_pointer + 1 ,create_y, create, new)
  #print(new, "first bach")
  x_pointer = create_x
  while x_pointer > 0 and not(blocked(create, x_pointer - 1, create_y)):
    x_pointer -= 1 
    new = load(x_pointer, create_y, create, new)
  refresh()
  #new = load(x_pointer - 1, create_y, create, new)
  y_pointer = create_y 
  while y_pointer < 7 and not(blocked(create, create_x, y_pointer + 1)):
    #print("Running1")
    y_pointer += 1
    new = load(create_x, y_pointer, create, new)
  refresh()
  #new = load(create_x, y_pointer + 1, create, new)
  y_pointer = create_y
  while y_pointer > 0 and not(blocked(create, create_x, y_pointer - 1)): 
    #print("Running2")
    y_pointer -= 1 
    new = load(create_x, y_pointer, create, new)
  refresh()
  #new = load(create_x, y_pointer - 1, create, new)

  #print("Straight moves", new)

  if gen:
    return Blocked_Tuple 
  else:
    return new

  #----

def diagonal(create, gen):
  global blocked_holder

  #Hence, create a tuple of new moves
  new = []
  blocked_holder = []
  create_x, create_y = create[0], create[1]
  #print("Funny movement")

  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer < 7) and not blocked(create, x_pointer + 1, y_pointer + 1): 
    x_pointer += 1
    y_pointer += 1 
    new = load(x_pointer, y_pointer, create, new)
  refresh()
  #new = load(x_pointer + 1, y_pointer + 1, create, new)
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer > 0 and y_pointer < 7) and not blocked(create, x_pointer - 1, y_pointer + 1):
    x_pointer -= 1
    y_pointer += 1 
    new = load(x_pointer, y_pointer, create, new)
  refresh()
  #new = 
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer > 0) and not blocked(create, x_pointer + 1, y_pointer - 1):
    x_pointer += 1
    y_pointer -= 1
    new = load(x_pointer, y_pointer, create, new)
  refresh()
  #new = load(x_pointer + 1, y_pointer - 1, create, new)
  x_pointer, y_pointer = create_x, create_y 
  while (x_pointer > 0 and y_pointer > 0) and not blocked(create, x_pointer - 1, y_pointer - 1):
    x_pointer -= 1
    y_pointer -= 1
    new = load(x_pointer, y_pointer, create, new)
  refresh()
  #new = load(x_pointer - 1, y_pointer - 1, create, new)    

  if gen:
    return Blocked_Tuple 
  else:
    return new 

  #----

def knight(create):
  #Create move_tuple for horse actions
  
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

# (4) --------- Legal moves; expansions and validation

def legal(move_to, move_from, move_space): 
  #INDEPENDENT HELPER: Validate that move is in moves_tuple

  #print(move_space)

  for i in range(len(move_space)):
    if move_from == move_space[i][0]:
      if move_to == move_space[i][1]:
        return True

  return False

  #----

def belonging(move_from, Moves_Tuple):
  #INDEPENDENT HELPER: Output legal moves 
  
  kept = []
  for i in range(len(Moves_Tuple)-1):
    if move_from == Moves_Tuple[i][0]:
      kept.append(Moves_Tuple[i])

  print("Possible moves", kept)

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

def blocked(create, move_from_x, move_from_y):
  global board
  global blocked_trait 
  global Blocked_Tuple

  if move_from_x < 0 or move_from_x > 7 or move_from_y < 0 or move_from_y > 7:
    return True  # Out of range


  if board[move_from_y][move_from_x] not in PEICE:
    #blocked_holder = load(move_from_x, move_from_y, create, blocked_holder)
    #print(blocked_holder)
    #print(board[move_from_y][move_from_x])
    return False
  else:
    if blocked_trait:
      Blocked_Tuple = load(move_from_x, move_from_y, create, Blocked_Tuple)
      blocked_trait = False
      return False
    else:
      return True 

  #----

def generate(move_from, move_to):
  #Create a list of affected peices 
  global White_moves
  global Black_moves
  #From the location; get all peices that have been affected
  #print("generating!")

  locations = []
  Blocked_Tuple = []
  locations += straight(move_from, True)
  Blocked_Tuple = []
  locations += diagonal(move_from, True)       
  Blocked_Tuple = []        
  locations += straight(move_to, True)
  Blocked_Tuple = []
  locations += diagonal(move_to, True)
  Blocked_Tuple = []

  #Possibly create a unique func to clean 

  return locations 

  #----

def explode(mapping):
  global White_moves
  global Black_moves
  #Hence, after generating a map of affected peices

  for i in range(len(mapping)-1):
    peice = board[mapping[i][1][1]][mapping[i][1][0]]
    #print(peice)
    if peice in WHITE:
      White_Playing = True
      #print("EXPLODE Complexity: ", len(White_moves))
      White_moves = clean(mapping[i][1], White_moves)
      #print("EXPLODE Complexity: ", len(White_moves))
      White_moves = property(mapping[i][1], peice, White_moves)
      #print(White_moves)
    elif peice in BLACK:
      White_Playing = False
      Black_moves = clean(mapping[i][1], Black_moves)
      Black_moves = property(mapping[i][1], peice, Black_moves)

  #Should do reasonablity checks here

  return White_moves, Black_moves
  
  #====

def mark(locations):
  global board 
  for i in range(len(locations)-5):
     try:
       board[locations[i][1][1]][locations[i][1][0]] = "X"
     except IndexError:
       print(locations[i])

  print(np.matrix(board))

#----

def refresh():
  global blocked_trait 
  blocked_trait = True

# (1) ---------- Loaded values

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
PEICE = [W_Pawn, W_Bish, W_Knig, W_Rook, W_Quee, W_King, B_Pawn, B_Bish, B_Knig, B_Rook, B_Quee, B_King]

board = [[B_Rook, B_Knig, B_Bish, B_Quee, B_King, B_Bish, B_Knig, B_Rook],
        [B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn, B_Pawn],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_, Empty_],
        [W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn, W_Pawn], 
        [W_Rook, W_Knig, W_Bish, W_Quee, W_King, W_Bish, W_Knig, W_Rook]]

Moves_Tuple = []
Blocked_Tuple = []
White_moves = Moves_Inital.White_moves
Black_moves = Moves_Inital.Black_moves

#print(White_moves, Black_moves)

# (5) --------- Main gameplay loop

Playing = True
White_Playing = True 
print(np.matrix(board))
Time_Stamp = - 1
while Playing:
  #Pass the turn to the next player 
  Time_Stamp += 1 
  White_Playing, Moves_Tuple = turn(Time_Stamp)

  #TESTS:
  #print("TEST, White moves:", White_moves)
  #print("TEST, Black moves:", Black_moves)

  # Asking the user for a move
  Valid = False
  map = []
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
  map += generate(move_to, move_from)
  White_moves, Black_moves = explode(map)

  #print("Blocked moves", Blocked_Tuple)
  #print("White moves", White_moves)
  #print("Black moves", Black_moves)

  print(np.matrix(board))

  print("----- PERFORMANCE CHECKS ------")
  print(len(White_moves))
  print(len(Black_moves))

  #alt = White_moves
  #mark(alt)