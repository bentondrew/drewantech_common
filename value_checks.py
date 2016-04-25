#  Copyright 2016
#  Drewan Tech, LLC
#  ALL RIGHTS RESERVED


def is_number_type_not_complex(value_to_check):
  if type(value_to_check) is not int:
    if type(value_to_check) is not float:
      return False
  return True
