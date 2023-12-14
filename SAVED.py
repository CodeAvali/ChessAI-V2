def diagonal(create, gen):
  global blocked_trait
  global Blocked_Tuple

  print("running diagonal", gen)

  #Hence, create a tuple of new moves
  new = []
  create_x, create_y = create[0], create[1]
  #print("Funny movement")

  #refresh()
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer < 7) and not blocked(create, x_pointer + 1, y_pointer + 1): 
    print("running 1")
    #print(blocked(create, x_pointer + 1, y_pointer + 1))
    x_pointer += 1
    y_pointer += 1 
    new = load(x_pointer, y_pointer, create, new)
  refresh()
  #new = load(x_pointer + 1, y_pointer + 1, create, new)
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer > 0 and y_pointer < 7) and not blocked(create, x_pointer - 1, y_pointer + 1):
    print("running 2")
    #print(blocked(create, x_pointer - 1, y_pointer + 1))
    x_pointer -= 1
    y_pointer += 1 
    new = load(x_pointer, y_pointer, create, new)
  refresh()
  #new =
  x_pointer, y_pointer = create_x, create_y
  while (x_pointer < 7 and y_pointer > 0) and not blocked(create, x_pointer + 1, y_pointer - 1):
    print("running 3")
    #print(blocked(create, x_pointer + 1, y_pointer - 1))
    x_pointer += 1
    y_pointer -= 1
    new = load(x_pointer, y_pointer, create, new)
  refresh()
  #new = load(x_pointer + 1, y_pointer - 1, create, new)
  x_pointer, y_pointer = create_x, create_y 
  while (x_pointer > 0 and y_pointer > 0) and not blocked(create, x_pointer - 1, y_pointer - 1):
    print("running 4")
    #print(blocked(create, x_pointer - 1, y_pointer - 1))
    x_pointer -= 1  
    y_pointer -= 1
    new = load(x_pointer, y_pointer, create, new)
  #refresh()
  #new = load(x_pointer - 1, y_pointer - 1, create, new)    

  if gen:
    return Blocked_Tuple 
  else:
    print("Generated moves, Diagonal", new)
    return new 