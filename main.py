#Main.py - Chess AI educational demonstration
#This is the shell of the chess AI program; which GUI.py calls from. 

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
  global White_moves, Black_moves, White_Playing, flag_map
  #INDEPENDENT: Shorthand for creating an action when needed

  temp = (x_value, y_value)
  temp = (create, tuple(temp))
  data_holder.append(temp)

  #For flagging system; add value as required       #Adaptive flagging system - needs to be refactored in to save O(2n)- legal moves
  #if flagging:
    #if White_Playing:
      #data = flag_map[y_value][x_value]
      #data = (int(data[0]) + 1, data[1])
      #flag_map[y_value][x_value] = data
    #else: 
      #data = flag_map[y_value][x_value] 
      #data = (data[0], int(data[1]) + 1)
      #flag_map[y_value][x_value] = data
  return data_holder

#----

def flag_the_map(White_moves, Black_moves):

  flag_map = [[(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],                #Basic flagging - likely inefficent. 
             [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],                 #Leads to inconsitences as has to be applied end of turn 
             [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],                 #NEEDS TO BE ADAPTIVE. AAAAAAAAAAAAA
             [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
             [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
             [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
             [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)],
             [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]]

  for i in range(len(White_moves)):
    x_value = White_moves[i][1][0]
    y_value = White_moves[i][1][1]
    data = flag_map[y_value][x_value]
    data = (int(data[0]) + 1, data[1])
    flag_map[y_value][x_value] = data

  for j in range(len(Black_moves)):
    x_value = Black_moves[j][1][0]
    y_value = Black_moves[j][1][1]
    data = flag_map[y_value][x_value]
    data = (data[0], int(data[1]) + 1)
    flag_map[y_value][x_value] = data

  return flag_map

  #----

def perform(move_to, move_from, board):
  global White_moves, Black_moves
  #Perform the required action - Clean and call forth explosion system

  Moves_Tuple = []

  #Performing moves
  get(move_to, move_from)
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

def get(move_to, move_from):
  global board, White_moves, Black_moves

  captured = board[move_to[1]][move_to[0]] #get captured peice
  capturing = board[move_from[1]][move_from[0]]

  if captured == W_En_Passant_Token:
    if capturing == B_Pawn:
      board[4][move_to[0]] = Empty_
      White_moves = clean((move_to[0], 4), White_moves)
  elif captured == B_En_Passant_Token:
    if capturing == W_Pawn:
      board[3][move_to[0]] = Empty_
      Black_moves = clean((move_to[0], 3), Black_moves)


  #then need to generate new moves from location;


  #----

def promotion(move_to, move_from):
  global board, White_moves, Black_moves

  #assuming pawn peice has allready been checked

  if move_to[1] == 0:   #Then, white pawn promotion
    board[1][move_from[0]] = W_Quee
  elif move_to[1] == 7:  #Black, pawn promotion 
    board[6][move_from[0]] = B_Quee   

  #Will implement peice choice later - just assuming queen for completeness. 

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

  #Directly forward moves; only 1 square
  if (White_Playing) and (board[create_y - 1][create_x] not in PEICE):
    new = load(create_x, create_y - 1, create, new)
  elif (not White_Playing) and (board[create_y + 1][create_x] not in PEICE):
    new = load(create_x, create_y + 1, create, new)

  #Handle starting space 2 move rule 

  create_x, create_y = create[0], create[1]

  if (White_Playing and create_y == 6) and (board[4][create_x] not in PEICE): 
    new = load(create_x, 4, create, new)
  if (not White_Playing) and (create_y == 1) and (board[3][create_x] not in PEICE):
    new = load(create_x, 3, create, new)

  #Handle diagional captures
  if (create_x - 1) >= 0:  #Index check 
    if (White_Playing) and board[create_y - 1][create_x - 1] in BLACK: 
      new = load(create_x - 1, create_y - 1, create, new)
    elif not(White_Playing) and board[create_y + 1][create_x - 1] in WHITE:
      new = load(create_x - 1, create_y + 1, create, new)

  if (create_x + 1) < 8: 
    if (White_Playing) and board[create_y - 1][create_x + 1] in BLACK:
      new = load(create_x + 1, create_y - 1, create, new)
    elif not(White_Playing) and board[create_y + 1][create_x + 1] in WHITE:
      new = load(create_x + 1, create_y + 1, create, new)
    
  return new

  #----

def straight(create, gen):
  global Blocked_Tuple, Attack_Tuple, Protected_Tuple
  Blocked_Tuple = []
  Attack_Tuple = []
  Protected_Tuple = []
  #from inital, collect the x and y components

  create_x, create_y = create[0], create[1]

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

  create_y, create_x = create[0], create[1]
  pivot = [(create_y + 2, create_x + 1),
           (create_y + 2, create_x - 1),
           (create_y - 2, create_x + 1),
           (create_y - 2, create_x - 1),
           (create_y + 1, create_x + 2),
           (create_y + 1, create_x - 2),
           (create_y - 1, create_x + 2),
           (create_y - 1, create_x - 2)]
  
  new = []
  Blocked_Tuple = []

  for i in range(len(pivot)):         
    if (pivot[i][0] < 8 and pivot[i][0] >= 0) and (pivot[i][1] < 8 and pivot[i][1] >= 0):  #Range check
      if not gen:
        if not own(create, pivot[i]):  #ensure no friendly captures      
          new = load(pivot[i][0], pivot[i][1], create, new)
      elif gen:
        if board[pivot[i][1]][pivot[i][0]] in KNIGHT:
          Blocked_Tuple = load(pivot[i][0], pivot[i][1], create, Blocked_Tuple)  #Handle edge case for moves
        
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

  create_x, create_y = create[0], create[1]
  pivot = [(create_x + 1, create_y + 1), 
           (create_x    , create_y + 1),
           (create_x - 1, create_y + 1), 
           (create_x + 1, create_y    ), 
           (create_x - 1, create_y    ), 
           (create_x + 1, create_y - 1), 
           (create_x, create_y - 1    ), 
           (create_x - 1, create_y - 1)]
  
  new = []

  for i in range(len(pivot)):         
    if (pivot[i][0] < 8 and pivot[i][0] >= 0) and (pivot[i][1] < 8 and pivot[i][1] >= 0):
      if not own(create, pivot[i]) and not attacked(pivot[i]):  #Check for friendly peices
        new = load(pivot[i][0], pivot[i][1], create, new)

  return new

  #----

def direct(create):
  new = []
  temp = (move_to, move_to)
  new.append(temp)
  return new

  #----

def attacked(create):
  global flag_map, White_Playing 

  pointer = 1
  if not White_Playing: 
    pointer = 0

  if flag_map[create[1]][create[0]][pointer] >= 1:
    return True
  else: 
    return False

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

  checked = []

  cleaned = tuple(delete)
  for i in range(len(moves_structure)):
    if (moves_structure[i][0] != cleaned):
      checked.append(moves_structure[i])
    
    #else:                                        #Adaptive flagging attempt - need to refactor later! to be more efficent rather than a 

     # x_value = moves_structure[i][1][1]
     # y_value = moves_structure[i][1][0]
      #print(board[y_value][x_value])
      #if White_Playing:
        #data = flag_map[x_value][y_value]
        #data = (int(data[0]) - 1, data[1])
        #flag_map[x_value][y_value] = data
      #else:
        #data = flag_map[x_value][y_value]
        #data = (data[0], int(data[1]) - 1)
        #flag_map[x_value][y_value] = data
  
  return checked

  #----

def blocked(create, move_from_x, move_from_y):
  global Blocked_Tuple, Attack_Tuple, Protected_Tuple

  if (move_from_x < 0 or move_from_x > 7) or (move_from_y < 0 or move_from_y > 7):
    return True #Range check 

  starting = board[create[1]][create[0]]
  destination = board[move_from_y][move_from_x]

  if (destination in EMPTY):
    return False #location is empty; not blocked

  Blocked_Tuple = load(move_from_x, move_from_y, create, Blocked_Tuple)
  if own(create, (move_from_x, move_from_y)):
    Protected_Tuple = load(move_from_x, move_from_y, create, Protected_Tuple)
  else:
    Attack_Tuple = load(move_from_x, move_from_y, create, Attack_Tuple)
  return True
    
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

  #for handling knight edge case
  locations += knight(move_from, True)
  locations += knight(move_to, True)

  #Otherwise; ensure that the opponents king is included
  print(King_location)
  if White_Playing:
    locations = load(King_location[1][0], King_location[1][1], King_location[0], locations)
    print("WhitePlaying")
  else:
    locations += load(King_location[0][0], King_location[0][1], King_location[1], locations)
    print("BlackPlaying")

  print(locations)

  return locations 

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

#----

def passant_check(move_from, move_to, en_location):
  global board

  en_flag = False  #Use a boolean flag

  inital_y = move_from[1]
  final_y = move_to[1]
  
  #Check to see if pawn move is elegible for en_passant
  if (inital_y == 1 and final_y == 3) or (inital_y == 6 and final_y == 4): 
    if (move_from[0] - 1) >= 0:   #Do a range check 
      if board[final_y][move_from[0] - 1] in PAWN:
        en_flag = True
    if (move_from[0] + 1) <= 7:   #Opposite range check - prevent error.
      if board[final_y][move_from[0] + 1] in PAWN:
        en_flag = True     

  #If move is elegible for en_passant response, create respective token for player
  if en_flag:
    offset = int((move_from[1] - move_to[1]) / 2) + move_to[1]
    if White_Playing:
      board[offset][move_from[0]] = W_En_Passant_Token     
      en_location[0][0] = offset
      en_location[0][1] = move_from[0]
    else:
      board[offset][move_from[0]] = B_En_Passant_Token
      en_location[1][0] = offset
      en_location[1][1] = move_from[0]

  return en_location  #point to token location 

  #----

def flag_map_check(flag_map):
  print("Flag map - print error check")
  for i in range(len(flag_map)):
    print(flag_map[i])
  
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
W_En_Passant_Token = '!'
B_En_Passant_Token = '?'

WHITE = [W_Pawn, W_Bish, W_Knig, W_Rook, W_Quee, W_King, W_En_Passant_Token]
BLACK = [B_Pawn, B_Bish, B_Knig, B_Rook, B_Quee, B_King, B_En_Passant_Token]
PEICE = [W_Pawn, W_Bish, W_Knig, W_Rook, W_Quee, W_King, B_Pawn, B_Bish, B_Knig, B_Rook, B_Quee, B_King]
KNIGHT = [W_Knig, B_Knig]
PAWN = [W_Pawn, B_Pawn]
EMPTY = [Empty_, W_En_Passant_Token, B_En_Passant_Token]
KING = [W_King, B_King]
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

flag_map = Moves_Inital.flag_map
flag_map_check(flag_map)

Moves_Tuple = []
Blocked_Tuple = []
Attack_Tuple = []
Protected_Tuple = []
White_moves = Moves_Inital.White_moves
Black_moves = Moves_Inital.Black_moves
en_location = [[-1, -1], [-1, -1]]    #first index array is used for White; 2nd index array is used for Black 
en_flag = -1
King_location = [[7, 4], [0, 4]]

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

  #Check to see if the move is elegible for enpassant 
  if board[move_from[1]][move_from[0]] in PAWN:
    en_location = passant_check(move_from, move_to, en_location)
    #Likewise, if pawn check for promotion
    promotion(move_to, move_from)

  #Printing inputs
  board = perform(move_to, move_from, board)
  map += generate(move_to, move_from)

  if (White_Playing) and board[en_location[1][0]][en_location[1][1]] == B_En_Passant_Token:
    board[en_location[1][0]][en_location[1][1]] = Empty_
  if (not White_Playing) and board[en_location[0][0]][en_location[0][1]] == W_En_Passant_Token:
    board[en_location[0][0]][en_location[0][1]] = Empty_

  #print(move_from[0], move_from[1], King_location)
  print("DIRECT", move_from, board[move_to[1]][move_to[0]])
  if board[move_to[1]][move_to[0]] in KING: 
    print("CHANGED")
    if White_Playing:
      King_location[0][0] = move_to[0]
      King_location[0][1] = move_to[1]
    else:
      King_location[1][0] = move_to[0]
      King_location[1][1] = move_to[1]
  print(move_from[0], move_from[1], King_location)

  
  #mark(map)
  map = unique(map)
  mark(map)

  #mark(map)

  White_moves, Black_moves = explode(map)

  #White_moves = unique(White_moves)
  #Black_moves = unique(Black_moves)

  print(np.matrix(board))
  flag_map = flag_the_map(White_moves, Black_moves)
  flag_map_check(flag_map)

  print("----- PERFORMANCE CHECKS ------")            #Remove after stage 1
  print("Complexity, white moves", len(White_moves))
  print("Complexity, black moves", len(Black_moves))

