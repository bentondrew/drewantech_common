#  Copyright 2016
#  Drewan Tech, LLC
#  ALL RIGHTS RESERVED


ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

digits = '0123456789'


def generate_32_character_random_string():
  import random
  return (''.join(random.choice(ascii_uppercase + digits)
                  for x in range(32)))
