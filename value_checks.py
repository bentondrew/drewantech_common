#  Copyright 2016
#  Drewan Tech, LLC
#  ALL RIGHTS RESERVED


def is_number_type_not_complex(value_to_check):
  if type(value_to_check) is not int:
    if type(value_to_check) is not float:
      return False
  return True


def valid_directory(directory):
  import os
  if type(directory) is not str:
    raise ValueError('The provided directory, {}, is not a str type.'
                     .format(directory))
  if not os.path.isdir(directory):
    raise OSError('The provided directory, {}, is not a valid directory '
                  'location.'.format(directory))
  return directory
