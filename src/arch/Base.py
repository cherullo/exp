
class Base():
    def __init__(self):
        pass

    def _raise_not_implemented(self, method):
        raise Exception(f'Method {self.__class__.__name}.{method} not implemented.')

    #def ToString(self) -> str:
    #    self._raise_not_implemented(self.ToString)

    def __str__(self):
        self._raise_not_implemented(self.__str__)

    def __lt__(self, other):
        return str(self) < str(other)

    def description(self) -> str:
        self._raise_not_implemented(self.description)

    def add_hash(self, hasher): # Don't import Hasher or we'll have a loop
        self._raise_not_implemented(self.add_hash)



