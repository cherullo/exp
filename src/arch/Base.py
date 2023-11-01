
class Base():
    """ 
    Base class for all architectural classes.
    Allows for easier hashing and reporting.
    """
    def __init__(self):
        pass

    def _raise_not_implemented(self, method):
        """
        Triggers a Exception indicating that a method was not implemented.

        Args:
            method (Function): A method.

        Raises:
            Exception: Always.
        """
        raise Exception(f'Method {self.__class__.__name}.{method} not implemented.')

    def __str__(self):
        """ 
        Returns this instance's constructor call.
        Eg. FilterColumn("Country", ["Brazil, Canada, Madagascar"])
        """
        self._raise_not_implemented(self.__str__)

    def __lt__(self, other):
        return str(self) < str(other)

    def description(self) -> str:
        """ 
        Returns a human-readable description of this class instance.

        Returns:
            str: This instance's description.
        """
        self._raise_not_implemented(self.description)

    def add_hash(self, hasher): # Don't import Hasher or we'll have a loop
        """ 
        Feeds the provided hasher with this instance's constructor data.

        Args:
            hasher (Hasher): A Hasher instance.
        """
        self._raise_not_implemented(self.add_hash)



