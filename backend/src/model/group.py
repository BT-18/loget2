class Group:
    def __init__(self, name: str):
        """
        Constructor for the group
        Args:
            name (str): the name of the group
        """
        if name is None or id is None:
            raise TypeError("Name and ID must be provided")
        self.name = name
        
    def get_name(self) -> str:
        """
        getter for the name of the group
        Returns: The name of the group
        """
        return self.name
    
    def set_name(self, name: str) -> None:
        """
        Change the name of the group

        Args:
            name: the new name of the group

        Returns: Nothing
        """
        if name is None:
            raise TypeError("Name must be provided")
        self.name = name
        
