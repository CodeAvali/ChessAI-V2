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



