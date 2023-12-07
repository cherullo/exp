import sys
from os import path

def get_main_filename():
    return sys.modules['__main__'].__file__

def get_absolute_main_filename():
    return path.abspath(get_main_filename())

def get_main_basename():
    return path.basename(get_main_filename()) 

def get_main_basename_extless():
    return path.splitext(get_main_basename())[0]