def straight(create, gen):
  #from inital, collect the x and y components
  create_x, create_y = create[0], create[1]
  blocked_trait = True 

  #Hence, create a tuple of new moves
  new = []

  #For the right direction
  x_pointer = create_x
  while x_pointer < 7 and not(blocked(create, x_pointer + 1, create_y)):
    x_pointer += 1
    new = load(x_pointer, create_y, create, new)







temp = (create_x, create_y - 1)  #Some offset to apply with blocked check
temp = (create, tuple(temp)) 
new.append(temp)








def load(x_value, y_value, create, data_holder):
  temp = (x_value, y_value)
  temp = (create, tuple(temp))
  data_holder.append(temp)
  return data_holder #Back into main program



#####

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

  new += Attack_Tuple
  return new



#-----

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

  return locations 









def straight(move_from, gen):
  raise NotImplementedError

def diagonal(move_from, gen):
  raise NotImplementedError

def perform(move_to, move_from, board):
  raise NotImplementedError

def generate(move_to, move_from):
  raise NotImplementedError

def explode(mapping):
  raise NotImplementedError

new = []
Blocked_Tuple = []
Attack_Tuple = []
gen = True 



def test(new, gen):
  if gen:
    return Blocked_Tuple
  else:
    new += Attack_Tuple
    return new 


#Do the action 
board = perform(move_to, move_from, board)

#Find 'affected' peices using heurisitc method 
map += generate(move_to, move_from)

#Regenerate moves for the 'affected' peices
White_moves, Black_moves = explode(map)