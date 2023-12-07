from abc import abstractmethod

class Base():
    """ 
    Base class for all architectural classes.
    Allows for easier hashing and reporting.
    """
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        """ 
        Returns this instance's constructor call.
        Eg. FilterColumn("Country", ["Brazil, Canada, Madagascar"])
        """
        pass

    def __lt__(self, other):
        return str(self) < str(other)

    @abstractmethod
    def description(self) -> str:
        """ 
        Returns a human-readable description of this class instance.

        Returns:
            str: This instance's description.
        """
        pass

    @abstractmethod
    def add_hash(self, hasher): # Don't import Hasher or we'll have a loop
        """ 
        Feeds the provided hasher with this instance's constructor data.

        Args:
            hasher (Hasher): A Hasher instance.
        """
        pass



