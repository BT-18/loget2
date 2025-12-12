from model.user import User
from util.connector import Pool
import mariadb

class UserRepo:
    def __init__(self, databasePool: Pool):
        self.db = databasePool.get_connection()
        
    def get_user_by_email(self, email: str):
        """
        Retrieve a user from the database by email
        Args:
            email (str): the email of the user to retrieve
        Returns: A User object if found, None otherwise
        """
        query = "SELECT email, hash, role, totp FROM Users WHERE email = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            return User(result[0], result[1], result[2], totp=result[3])
        else:
            return None
        
    def add_user(self, user: User) -> None:
        """
        Add a new user to the database
        Args:
            user (User): the user object to add
        Returns: Nothing
        """
        query = "INSERT INTO Users (email, hash, totp) VALUES (?, ?, ?)"
        cursor = self.db.cursor()
        cursor.execute(query, (user.get_email(), user.get_password(), user.get_totp()))
        self.db.commit()
        
    def update_totp(self, email: str, totp: str) -> None:
        """
        Update the TOTP key for a user
        Args:
            email (str): the email of the user to update
            totp (str): the new TOTP key
        Returns: Nothing
        """
        query = "UPDATE Users SET totp = ? WHERE email = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (totp, email))
        self.db.commit()
        
    def update_email(self, old_email: str, new_email: str) -> None:
        """
        Update the email of a user
        Args:
            old_email (str): the current email of the user
            new_email (str): the new email to set
        Returns: Nothing
        """
        query = "UPDATE Users SET email = ? WHERE email = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (new_email, old_email))
        self.db.commit()
    
    def update_password(self, email: str, new_password: str) -> None:
        """
        Update the password of a user
        Args:
            email (str): the email of the user to update
            new_password (str): the new hashed password
        Returns: Nothing
        """
        query = "UPDATE Users SET hash = ? WHERE email = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (new_password, email))
        self.db.commit()
        
    def update_role(self, email: str, new_role: str) -> None:
        """
        Update the role of a user
        Args:
            email (str): the email of the user to update
            new_role (str): the new role to set
        Returns: Nothing
        """
        query = "UPDATE Users SET role = ? WHERE email = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (new_role, email))
        self.db.commit()
        
    def delete_user(self, email: str) -> None:
        """
        Delete a user from the database
        Args:
            email (str): the email of the user to delete
        Returns: Nothing
        """
        
        query = "DELETE FROM Users WHERE email = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (email,))
        self.db.commit()