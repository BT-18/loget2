class Log:
    def __init__(self, id: int, fromHost: str, receivedAt: str, message: str):
        """
        Constructor for the log
        Args:
            fromHost (str): the host from which the log was sent
            receivedAt (str): the time at which the log was received
            message (str): the content of the log
        """
        if id is None or fromHost is None or receivedAt is None or message is None:
            raise TypeError("ID, fromHost, receivedAt, and message must be provided")
        self.id = id
        self.fromHost = fromHost
        self.receivedAt = receivedAt
        self.message = message
        
    def get_id(self) -> int:
        """
        getter for the id of the log
        Returns: The id of the log
        """
        return self.id
        
    def get_fromHost(self) -> str:
        """
        getter for the host from which the log was sent
        Returns: The host from which the log was sent
        """
        return self.fromHost
    
    def get_receivedAt(self) -> str:
        """
        getter for the time at which the log was received
        Returns: The time at which the log was received
        """
        return self.receivedAt
    
    def get_message(self) -> str:
        """
        getter for the content of the log
        Returns: The content of the log
        """
        return self.message
    
    def set_id(self, id: int) -> None:
        """
        Change the id of the log

        Args:
            id: the new id of the log

        Returns: Nothing
        """
        if id is None:
            raise TypeError("ID must be provided")
        self.id = id
    
    def set_message(self, message: str) -> None:
        """
        Change the content of the log

        Args:
            message: the new content of the log

        Returns: Nothing
        """
        if message is None:
            raise TypeError("Message must be provided")
        self.message = message
        
    def set_fromHost(self, fromHost: str) -> None:
        """
        Change the host from which the log was sent

        Args:
            fromHost: the new host from which the log was sent

        Returns: Nothing
        """
        if fromHost is None:
            raise TypeError("fromHost must be provided")
        self.fromHost = fromHost
        
    def set_receivedAt(self, receivedAt: str) -> None:
        """
        Change the time at which the log was received

        Args:
            receivedAt: the new time at which the log was received

        Returns: Nothing
        """
        if receivedAt is None:
            raise TypeError("receivedAt must be provided")
        self.receivedAt = receivedAt
        
        