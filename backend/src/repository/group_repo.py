from model.group import Group
from util.connector import Pool 

class GroupRepo:
    def __init__(self, databasePool: Pool):
        self.pool = databasePool
        
    def add_group(self, group: Group) -> None:
        """
        Add a new group to the database
        Args:
            group (Group): the group object to add
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "INSERT INTO Groups (name) VALUES (?)"
            cursor = conn.cursor()
            cursor.execute(query, (group.get_name(),))
            conn.commit()
        finally:
            conn.close()
        
    def add_user_to_group(self, email: str, group_name: str) -> None:
        """
        Add a user to a group
        Args:
            email (str): the email of the user to add
            group_name (str): the name of the group
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "INSERT INTO UserGroups (user_id, group_id) VALUES ((SELECT id FROM Users WHERE email = ?), (SELECT id FROM Groups WHERE name = ?))"
            cursor = conn.cursor()
            cursor.execute(query, (email, group_name))
            conn.commit()
        finally:
            conn.close()
        
    def remove_user_from_group(self, email: str, group_name: str) -> None:
        """
        Remove a user from a group
        Args:
            email (str): the email of the user to remove
            group_name (str): the name of the group
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "DELETE FROM UserGroups WHERE user_id = (SELECT id FROM Users WHERE email = ?) AND group_id = (SELECT id FROM Groups WHERE name = ?)"
            cursor = conn.cursor()
            cursor.execute(query, (email, group_name))
            conn.commit()
        finally:
            conn.close()
        
    def get_all_groups(self) -> list:
        """
        Retrieve all groups from the database
        Args: None
        Returns: A list of Group objects
        """
        conn = self.pool.get_connection()
        try:
            query = "SELECT name FROM Groups"
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            groups = []
            for row in results:
                groups.append(Group(name=row[0]))
            return groups
        finally:
            conn.close()
    
    def delete_group(self, group_name: str) -> None:
        """
        Delete a group from the database
        Args:
            group_name (str): the name of the group to delete
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "DELETE FROM Groups WHERE name = ?"
            cursor = conn.cursor()
            cursor.execute(query, (group_name,))
            conn.commit()
        finally:
            conn.close()
        
    def get_users_in_group(self, group_name: str) -> list:
        """
        Retrieve all users in a group
        Args:
            group_name (str): the name of the group
        Returns: A list of user emails
        """
        conn = self.pool.get_connection()
        try:
            query = "SELECT U.email FROM Users U JOIN UserGroups UG ON U.id = UG.user_id JOIN Groups G ON UG.group_id = G.id WHERE G.name = ?"
            cursor = conn.cursor()
            cursor.execute(query, (group_name,))
            results = cursor.fetchall()
            users = []
            for row in results:
                users.append(row[0])
            return users
        finally:
            conn.close()
    
    def rename_group(self, old_name: str, new_name: str) -> None:
        """
        Rename a group
        Args:
            old_name (str): the current name of the group
            new_name (str): the new name of the group
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "UPDATE Groups SET name = ? WHERE name = ?"
            cursor = conn.cursor()
            cursor.execute(query, (new_name, old_name))
            conn.commit()
        finally:
            conn.close()