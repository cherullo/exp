import struct
import zlib

from arch import Base

_ORDER = 'little'

def _int_to_bytearray(i: int):
    l = 8 + (i + (i < 0)).bit_length() // 8
    return i.to_bytes(length=l, byteorder=_ORDER, signed=True)

def _float_to_bytearray(f: float):
    return bytearray(struct.pack("d", f))

def _str_to_bytearray(s: str):
    return bytearray(s, 'utf-8')

def _to_bytearray(v):
    if (isinstance(v, int)):
        return _int_to_bytearray(v)
    
    if (isinstance(v, float)):
        return _float_to_bytearray(v)

    if (isinstance(v, str)):
        return _str_to_bytearray(v)

    if (isinstance(v, bool)):
        return _str_to_bytearray('True' if v == True else 'False')

    if (isinstance(v, Hasher)):
        return _int_to_bytearray(v.value)
    
    raise Exception(f'Cannot hash {type(v)}')

class Hasher():
    def __init__(self, *args):
        self.value = 1
        self.ordered(*args)

    def ordered(self, *args):
        for v in args:
            if (v is None):
                continue

            if (isinstance(v, Base)):
                v.add_hash(self)
            else:
                self.value = zlib.adler32(_to_bytearray(v), self.value)
            
        return self

    def unordered(self, *args):
        temp = 0

        for v in args:
            if (v is None):
                continue

            if (isinstance(v, Base)):
                temp ^= v.add_hash(Hasher()).value
            else:
                temp ^= zlib.adler32(_to_bytearray(v))

        self.value ^= temp

        return self

    def __str__(self):
        return "%x"%(self.value&0xffffffff)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other

        if isinstance(other, Hasher):
            return self.value == other.value

        return False;



    