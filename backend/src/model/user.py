class User:
    def __init__(self, email: str, password: str, totp:str=None):
        """
        Constructor for the User
        Args:
            email (str): the email of the user:
            password (str): the hashed password of the user:
            totp (str): the totp key of the user:
        """
        self.email = email
        self.password = password
        self.totp = totp

    def get_email(self) -> str:
        """
        getter for the email of the user
        Returns: The email of the user
        """
        return self.email

    def get_password(self) -> str:
        """
        getter for the password of the user
        Returns: the hashed password of the user

        """
        return self.password

    def get_totp(self) -> str:
        """
        getter for the totp of the user
        Returns: The totp key of the user
        """
        return self.totp

    def set_totp(self, totp: str) -> None:
        """
        Change or set the totp of the user

        Args:
            totp (str): the new totp of the user

        Returns: Nothing
        """
        if totp is not None:
            self.totp = totp
        else:
            raise TypeError("No totp provided")

    def set_email(self, email: str) -> None:
        """
        Change the email of the user

        Args:
            email: the new email of the user

        Returns: Nothing

        """
        if email is not None:
            self.email = email
        else:
            raise TypeError("No email provided")

    def set_password(self, password: str) -> None:
        """
        Change password of the user

        Args:
            password: the new password of the user

        Returns: Nothing
        """
        if password is not None:
            self.password = password
        else:
            raise TypeError("No password provided")

