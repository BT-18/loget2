class Entity:
    def __init__(self, name: str):
        """
        Constructor for the entity
        Args:
            name (str): the name of the entity
        """
        if name is None:
            raise TypeError("Name must be provided")
        self.name = name
        
    def get_name(self) -> str:
        """
        getter for the name of the entity
        Returns: The name of the entity
        """
        return self.name
    
    def set_name(self, name: str) -> None:
        """
        Change the name of the entity

        Args:
            name: the new name of the entity

        Returns: Nothing
        """
        if name is None:
            raise TypeError("Name must be provided")
        self.name = name