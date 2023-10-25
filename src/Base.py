
class Base():
    def __init__(self):
        pass

    def _raise_not_implemented(self, method):
        raise Exception(f'Method {self.__class__.__name}.{method} not implemented.')

    def ToString(self) -> str:
        self._raise_not_implemented(self.ToString)

    def __str__(self):
        return self.ToString()

    def __lt__(self, other):
        return self.ToString() < other.ToString()

    def Description(self) -> str:
        self._raise_not_implemented(self.Description)

    def AddHash(self, h):
        self._raise_not_implemented(self.AddHash)



