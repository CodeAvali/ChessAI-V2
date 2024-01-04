#Test for an ai implementation

import random 


def lazy_pick(Moves_Tuple):
  choices = len(Moves_Tuple)
  pick = random.randint(0, choices - 1)

  return Moves_Tuple[pick]

##########

