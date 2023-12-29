#Live document for current work - Code Avali - Chessbot NEA

import numpy as np
import Moves_Inital
global board, White_Playing, White_moves, Black_moves, Moves_Tuple, Blocked_Tuple, Time_Stamp
space = ' '

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
  global White_moves, Black_moves
  #Perform the required action - Clean and call forth explosion system

  Moves_Tuple = []

  #Performing moves
  peice = board[move_from[1]][move_from[0]]  #Collect moving peice into temp variable 
  board[(move_from[1])][(move_from[0])] = Empty_  #Remove moving peice
  board[(move_to[1])][(move_to[0])] = peice #Hence, write the peice into the location 

  #Hence; store new to respective holder
  if White_Playing:                       
    White_moves = clean(move_from, White_moves)
    Black_moves = clean(move_to, Black_moves)        
  else:  #Otherwise; black player
    Black_moves = clean(move_from, Black_moves)
    White_moves = clean(move_to, White_moves)           

  if White_Playing:
    White_moves += Moves_Tuple    
  else:
    Black_moves += Moves_Tuple

  return board 

  #----

# (3) --------- Movement properties -----------

def property(move_to, peice, Moves_Tuple):
  global White_Playing
  #MAIN: Calls forth movement properties; to return legal moves etc

  if peice in (W_Pawn, B_Pawn):
    Moves_Tuple += pawn((move_to[0], move_to[1]), White_Playing)
  elif peice in (W_Knig, B_Knig):
    Moves_Tuple += knight((move_to[0], move_to[1]), False)
  elif peice in (W_Rook, B_Rook):
    Moves_Tuple += straight((move_to[0], move_to[1]), False)
  elif peice in (W_Bish, B_Bish):
    Moves_Tuple += diagonal((move_to[0], move_to[1]), False)
  elif peice in (W_Quee, B_Quee):
    Moves_Tuple += diagonal((move_to[0], move_to[1]), False)
    Moves_Tuple += straight((move_to[0], move_to[1]), False)
  elif peice in (W_King, B_King): 
    Moves_Tuple += adjecent((move_to[0], move_to[1]))

  return Moves_Tuple

  #----

def pawn(create, White_Playing):
  global blocked_trait, board
  #from inital, collect the x and y components 

  create_x, create_y = create[0], create[1]

  #Hence, create a tuple containing new moves 

  new = []
  temp = ''

  if (White_Playing) and not(board[create_y - 1][create_x] in PEICE):
    temp = (create_x, create_y - 1)  

    #For black
  if (not White_Playing) and not(board[create_y + 1][create_x] in PEICE):
    temp = (create_x, create_y + 1)   
    #Add any additional conditions - Caputre; enpassant

  if temp != '':
    temp = (create, tuple(temp)) #Need to sync for other player
    new.append(temp)

  #Handle starting space 2 nove rule 

  temp = ''

  create_x, create_y = create[0], create[1]

  blocked_trait = True
  if (White_Playing and create_y == 6) and (board[4][create_x] not in PEICE): 
    temp = (create_x, 4)
  refresh()
  if (not White_Playing) and (create_y == 1) and (board[3][create_x] not in PEICE):
    temp = (create_x, 3)

  if temp != '':
    temp = (create, tuple(temp)) #Need to sync for other player
    new.append(temp)

  #Handle diagional captures
  if (create_x - 1) >= 0:
    if (White_Playing) and board[create_y - 1][create_x - 1] in BLACK: 
      temp = (create_x - 1, create_y - 1)
      temp = (create, tuple(temp))
      new.append(temp)
    elif not(White_Playing) and board[create_y + 1][create_x - 1] in WHITE:
      temp = (create_x - 1, create_y + 1)
      temp = (create, tuple(temp))
      new.append(temp)

  if (create_x + 1) < 8: 
    if (White_Playing) and board[create_y - 1][create_x + 1] in BLACK:
      temp = (create_x + 1, create_y - 1)
      temp = (create, tuple(temp))
      new.append(temp)
    elif not(White_Playing) and board[create_y + 1][create_x + 1] in WHITE:
      temp = (create_x + 1, create_y + 1)
      temp = (create, tuple(temp))
      new.append(temp)
    
  return new

  #----

def straight(create, gen):
  global Blocked_Tuple, Attack_Tuple, Protected_Tuple
  Blocked_Tuple = []
  Attack_Tuple = []
  Protected_Tuple = []
  #from inital, collect the x and y components

  create_x, create_y = create[0], create[1]
  blocked_trait = True 

  #Hence, create a tuple of new moves

  new = []

  x_pointer = create_x
  while x_pointer < 7 and not(blocked(create, x_pointer + 1, create_y)):
    x_pointer += 1
    new = load(x_pointer, create_y, create, new)
  x_pointer = create_x
  while x_pointer > 0 and not(blocked(create, x_pointer - 1, create_y)):
    x_pointer -= 1 
    new = load(x_pointer, create_y, create, new)
  y_pointer = create_y 
  while y_pointer < 7 and not(blocked(create, create_x, y_pointer + 1)):
    y_pointer += 1
    new = load(create_x, y_pointer, create, new)
  y_pointer = create_y
  while y_pointer > 0 and not(blocked(create, create_x, y_pointer - 1)): 
    y_pointer -= 1 
    new = load(create_x, y_pointer, create, new)

  if gen:
    #Can cleanout bishop/knight peices for optimisation - CHECK TO SEE IF APPROVED 
    new = []
    for i in range(len(Blocked_Tuple)):
      if board[Blocked_Tuple[i][1][1]][Blocked_Tuple[i][1][0]] not in straight_optimised:
        temp = (move_from, tuple(Blocked_Tuple[i][1]))
        new.append(temp)
      #else: 
        #print("straight movement redundancy check successful", board[Blocked_Tuple[i][1][1]][Blocked_Tuple[i][1][0]])
    return new
  else:
    new += Attack_Tuple
    return new

  #----

def diagonal(create, gen):
  global Blocked_Tuple, Attack_Tuple, Protected_Tuple
  Blocked_Tuple = []
  Attack_Tuple = []
  Protected_Tuple = []

  #Hence, create a tuple of new moves
  new = []
  create_x, create_y = create[0], create[1]


  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer < 7) and not blocked(create, x_pointer + 1, y_pointer + 1): 
    x_pointer += 1
    y_pointer += 1 
    new = load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer > 0 and y_pointer < 7) and not blocked(create, x_pointer - 1, y_pointer + 1):
    x_pointer -= 1
    y_pointer += 1 
    new = load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer > 0) and not blocked(create, x_pointer + 1, y_pointer - 1):
    x_pointer += 1
    y_pointer -= 1
    new = load(x_pointer, y_pointer, create, new)
  x_pointer, y_pointer = create_x, create_y 
  while (x_pointer > 0 and y_pointer > 0) and not blocked(create, x_pointer - 1, y_pointer - 1):
    x_pointer -= 1
    y_pointer -= 1
    new = load(x_pointer, y_pointer, create, new)

  if gen:
    #Can cleanout bishop/knight peices for optimisation - CHECK TO SEE IF APPROVED 
    new = []
    for i in range(len(Blocked_Tuple)):
      if board[Blocked_Tuple[i][1][1]][Blocked_Tuple[i][1][0]] not in diagonal_optimised:
        temp = (move_from, tuple(Blocked_Tuple[i][1]))
        new.append(temp)
      #else: 
        #print("Diagonal movement redundancy check successful", board[Blocked_Tuple[i][1][1]][Blocked_Tuple[i][1][0]])
    return new
  else:
    new += Attack_Tuple
    return new 

  #----

def knight(create, gen):
  #Create move_tuple for horse actions
  
  pivot = []
  new = []
  Blocked_Tuple = []
  create_y, create_x = create[0], create[1]

  #hence, create tuple of new moves
  pivot.append((create_y + 2, create_x + 1))       #Will format later to a bland tuple 
  pivot.append((create_y + 2, create_x - 1))
  pivot.append((create_y - 2, create_x + 1))
  pivot.append((create_y - 2, create_x - 1))
  pivot.append((create_y + 1, create_x + 2))
  pivot.append((create_y + 1, create_x - 2))
  pivot.append((create_y - 1, create_x + 2))
  pivot.append((create_y - 1, create_x - 2))

  for i in range(len(pivot)):         
    if (pivot[i][0] < 8 and pivot[i][0] >= 0) and (pivot[i][1] < 8 and pivot[i][1] >= 0):  #Range check
      if not own(create, pivot[i]):  #ensure no friendly captures      
        #Then append to check  
        temp = (create, tuple(pivot[i]))
        new.append(temp)
      else:
        temp = (create, tuple(pivot[i]))
        Blocked_Tuple.append(temp)
        

  if not gen:
    return new
  else: 
    return Blocked_Tuple 
    
  #----

def own(move_from, move_to):
  create_move = board[move_from[1]][move_from[0]]
  create_location = board[move_to[1]][move_to[0]]

  if (create_move in WHITE) and (create_location in WHITE):
    return True
  elif (create_move in BLACK) and (create_location in BLACK):
    return True
  else:  #otherwise;
    return False 
    
#----
  

def adjecent(create):

  pivot = []
  new = []
  create_x, create_y = create[0], create[1]

  #hence, create tuple of new moves
  pivot.append((create_x + 1, create_y + 1))        #Will format into a bland tuple later 
  pivot.append((create_x    , create_y + 1))
  pivot.append((create_x - 1, create_y + 1))
  pivot.append((create_x + 1, create_y))
  pivot.append((create_x - 1, create_y))
  pivot.append((create_x + 1, create_y - 1))
  pivot.append((create_x, create_y - 1))
  pivot.append((create_x - 1, create_y - 1))

  for i in range(len(pivot)):         
    if (pivot[i][0] < 8 and pivot[i][0] >= 0) and (pivot[i][1] < 8 and pivot[i][1] >= 0):
      if not own(create, pivot[i]):
        temp = (create, tuple(pivot[i]))
        new.append(temp)

  #print(new)

  return new

  #----

def direct(create):
  new = []
  temp = (move_to, move_to)
  new.append(temp)
  #print("returned from direct", new)
  return new

# (4) --------- Legal moves; expansions and validation

def legal(move_to, move_from, move_space): 
  # Validate that move is in moves_tuple

  for i in range(len(move_space)):
    if move_from == move_space[i][0]:
      if move_to == move_space[i][1]:
        return True #is present in 

  #otherwise;
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
  checked = []

  cleaned = tuple(delete)
  for i in range(len(moves_structure)):
    if (moves_structure[i][0] != cleaned):
      checked.append(moves_structure[i])

  return checked

  #----

def blocked(create, move_from_x, move_from_y):
  global Blocked_Tuple, Attack_Tuple, Protected_Tuple

  if (move_from_x < 0 or move_from_x > 7) or (move_from_y < 0 or move_from_y > 7):
    return True #Range check 

  starting = board[create[1]][create[0]]
  destination = board[move_from_y][move_from_x]

  if destination == Empty_:
    return False #location is empty; not blocked

  Blocked_Tuple = load(move_from_x, move_from_y, create, Blocked_Tuple)
  if own(create, (move_from_x, move_from_y)):
    Protected_Tuple = load(move_from_x, move_from_y, create, Protected_Tuple)
  else:
    Attack_Tuple = load(move_from_x, move_from_y, create, Attack_Tuple)
  return True
    
  #----

  #----

def generate(move_from, move_to):
  #Create a list of affected peices 
  global White_moves, Black_moves, Blocked_Tuple
  #From the location; get all peices that have been affected

  print(move_from, move_to)  #testing

  locations = []
  Blocked_Tuple = []

  #for moving_from
  locations += straight(move_from, True)
  locations += diagonal(move_from, True)       
  
  #for moving_to
  locations += straight(move_to, True)
  locations += diagonal(move_to, True)

  #for direct locations 
  #locations += direct(move_to)
  #locations += direct(move_from)
  locations += blind(move_from, move_to)

  return locations 

  #----

def blind(move_from, move_to):
  global board, KNIGHT

  pivot = []
  new = []

  create_y, create_x = move_from[0], move_from[1]
  pivot.append((create_y + 2, create_x + 1))       #Will format later to a bland tuple 
  pivot.append((create_y + 2, create_x - 1))
  pivot.append((create_y - 2, create_x + 1))
  pivot.append((create_y - 2, create_x - 1))
  pivot.append((create_y + 1, create_x + 2))
  pivot.append((create_y + 1, create_x - 2))
  pivot.append((create_y - 1, create_x + 2))
  pivot.append((create_y - 1, create_x - 2))

  create_y, create_x = move_to[0], move_to[1]
  pivot.append((create_y + 2, create_x + 1))       #Will format later to a bland tuple 
  pivot.append((create_y + 2, create_x - 1))
  pivot.append((create_y - 2, create_x + 1))
  pivot.append((create_y - 2, create_x - 1))
  pivot.append((create_y + 1, create_x + 2))  #Could realistically just handle this better. 
  pivot.append((create_y + 1, create_x - 2))
  pivot.append((create_y - 1, create_x + 2))
  pivot.append((create_y - 1, create_x - 2))


  for i in range(len(pivot)):         
    if (pivot[i][0] < 8 and pivot[i][0] >= 0) and (pivot[i][1] < 8 and pivot[i][1] >= 0):  #Range check
      #print(pivot[i], board[pivot[i][1]][pivot[i][0]])
      if board[pivot[i][1]][pivot[i][0]] in KNIGHT:
        temp = (move_from, tuple(pivot[i]))
        new.append(temp)

  #print("generated from blind", new)

  return new 

  #Need to make more efficent - Refactor incoming!

  #----

def explode(mapping):
  global White_moves, Black_moves, White_Playing
  #Hence, after generating a map of affected peices

  #print("complexity explosion", len(mapping))
  for i in range(len(mapping)):
    peice = board[mapping[i][1][1]][mapping[i][1][0]]
    if peice in WHITE:
      White_Playing = True
      White_moves = clean(mapping[i][1], White_moves)
      White_moves = property(mapping[i][1], peice, White_moves)
    elif peice in BLACK:
      White_Playing = False
      Black_moves = clean(mapping[i][1], Black_moves)
      Black_moves = property(mapping[i][1], peice, Black_moves)

  #Then, return new legal moves. 
  return White_moves, Black_moves

  #White_moves = unique(White_moves)      #testing for duplicates
  #Black_moves = unique(Black_moves)
  
  #====

def mark(locations):
  test = [[0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0]]

  for i in range(len(locations)):
    test[locations[i][1][1]][locations[i][1][0]] += 1

  print(np.matrix(test))

#----

def refresh():
  global blocked_trait 
  blocked_trait = False

#----

def unique(duplicates):

  # intilize a null list
  unique_list = []
  print("TESTING", len(duplicates))

  # traverse for all elements
  for i in duplicates:
      # check if exists in unique_list or not
      if i not in unique_list:
          unique_list.append(i)

  print("TESTING", len(unique_list))

  return unique_list

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
KNIGHT = [W_Knig, B_Knig]
straight_optimised = [W_Knig, B_Knig, W_Bish, B_Bish, Empty_]
diagonal_optimised = [W_Knig, B_Knig, W_Rook, B_Rook, Empty_]


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
Attack_Tuple = []
Protected_Tuple = []
White_moves = Moves_Inital.White_moves
Black_moves = Moves_Inital.Black_moves

# (5) --------- Main gameplay loop

Playing = True
White_Playing = True 
print(np.matrix(board))
Time_Stamp = - 1
while Playing:
  #Pass the turn to the next player 
  Time_Stamp += 1
  White_Playing, Moves_Tuple = turn(Time_Stamp)

  # Asking the user for a move
  Valid = False
  map = []
  
  while not Valid:
    
    #Get inputs from users - using string literals to produce visual spacing
    move_from = input(f"location to move from, (x,y) {space*10}")
    move_to = input(f"location to move to, (x,y) {space*12}")     

    #Process accordingly and normalise
    move_to, move_from = action(move_to, move_from)

    #Perform exceptions; 
    Valid = legal(move_to, move_from, Moves_Tuple)
    belonging(move_from, Moves_Tuple)
    #absurd(move_to, move_from)


  #Printing inputs
  board = perform(move_to, move_from, board)
  map += generate(move_to, move_from)

  #mark(map)
  #print(len(map))
  #map = unique(map)
  #print(len(map))
  #mark(map)

  #mark(map)

  White_moves, Black_moves = explode(map)

  #White_moves = unique(White_moves)
  #Black_moves = unique(Black_moves)

  print(np.matrix(board))

  print("----- PERFORMANCE CHECKS ------")
  print("Complexity, white moves", len(White_moves))
  print("Complexity, black moves", len(Black_moves))

