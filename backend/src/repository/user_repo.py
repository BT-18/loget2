from model.user import User
from util.connector import Pool
import mariadb

class UserRepo:
    def __init__(self, databasePool: Pool):
        self.pool = databasePool
        
    def get_user_by_email(self, email: str):
        """
        Retrieve a user from the database by email
        Args:
            email (str): the email of the user to retrieve
        Returns: A User object if found, None otherwise
        """
        conn = self.pool.get_connection()
        try:
            query = "SELECT email, hash, role, totp FROM Users WHERE email = ?"
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result:
                print(result)
                return User(result[0], result[1], result[2], totp=result[3])
            else:
                return None
        finally:
            conn.close()
        
    def add_user(self, user: User) -> None:
        """
        Add a new user to the database
        Args:
            user (User): the user object to add
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "INSERT INTO Users (email, hash, role, totp) VALUES (?, ?, ?, ?)"
            cursor = conn.cursor()
            cursor.execute(query, (user.get_email(), user.get_password(), user.get_role(), user.get_totp()))
            conn.commit()
        finally:
            conn.close()
        
    def update_totp(self, email: str, totp: str) -> None:
        """
        Update the TOTP key for a user
        Args:
            email (str): the email of the user to update
            totp (str): the new TOTP key
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "UPDATE Users SET totp = ? WHERE email = ?"
            cursor = conn.cursor()
            cursor.execute(query, (totp, email))
            conn.commit()
        finally:
            conn.close()
        
    def update_email(self, old_email: str, new_email: str) -> None:
        """
        Update the email of a user
        Args:
            old_email (str): the current email of the user
            new_email (str): the new email to set
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "UPDATE Users SET email = ? WHERE email = ?"
            cursor = conn.cursor()
            cursor.execute(query, (new_email, old_email))
            conn.commit()
        finally:
            conn.close()
    
    def update_password(self, email: str, new_password: str) -> None:
        """
        Update the password of a user
        Args:
            email (str): the email of the user to update
            new_password (str): the new hashed password
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "UPDATE Users SET hash = ? WHERE email = ?"
            cursor = conn.cursor()
            cursor.execute(query, (new_password, email))
            conn.commit()
        finally:
            conn.close()
        
    def update_role(self, email: str, new_role: str) -> None:
        """
        Update the role of a user
        Args:
            email (str): the email of the user to update
            new_role (str): the new role to set
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "UPDATE Users SET role = ? WHERE email = ?"
            cursor = conn.cursor()
            cursor.execute(query, (new_role, email))
            conn.commit()
        finally:
            conn.close()
        
    def delete_user(self, email: str) -> None:
        """
        Delete a user from the database
        Args:
            email (str): the email of the user to delete
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "DELETE FROM Users WHERE email = ?"
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            conn.commit()
        finally:
            conn.close()
        
    def get_all_users(self) -> list:
        """
        Retrieve all users from the database
        Args: None
        Returns: A list of User objects
        """
        conn = self.pool.get_connection()
        try:
            query = "SELECT email, hash, role, totp FROM Users"
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            users = []
            for result in results:
                users.append(User(result[0], result[1], result[2], totp=result[3]))
            return users
        finally:
            conn.close()
    
    def get_groups_of_users(self, email: str) -> list:
        """
        Retrieve the groups associated with the user
        Returns: A list of group names
        """
        conn = self.pool.get_connection()
        try:
            query = "SELECT G.name FROM Groups G JOIN UserGroup UG ON G.id = UG.group_id JOIN Users U ON UG.user_id = U.id WHERE U.email = ?"
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            results = cursor.fetchall()
            groups = []
            for row in results:
                groups.append(row[0])
            return groups
        finally:
            conn.close()

    def get_entities_of_users(self, email: str) -> list:
        """
        Retrieve the entities associated with the user
        Returns: A list of entity names
        """
        entities_list = []
        user_groups = self.get_groups_of_users(email)
        
        if not user_groups:
            return entities_list
        
        conn = self.pool.get_connection()  
        try:
            for group_name in user_groups:
                query = "SELECT E.name FROM Entities E JOIN EntityGroup GE ON E.id = GE.entity_id JOIN Groups G ON GE.group_id = G.id WHERE G.name = ?"
                cursor = conn.cursor()
                cursor.execute(query, (group_name,))
                results = cursor.fetchall()
                for row in results:
                    if row[0] not in entities_list:
                        entities_list.append(row[0])
        finally:
            conn.close()
        
        return entities_list