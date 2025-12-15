from repository.group_repo import *
from model.user import *
import mariadb

class GroupService:
    def __init__(self, databasePool: Pool):
        """Initialize the GroupService with a database connection pool"""
        self.group_repo = GroupRepo(databasePool)
        
    def add_group(self, name: str, role_claims: str) -> str:
        """
        Service method to add a new group
        Args:
            name (str): the name of the group to add
        Returns: A status message
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            group = Group(name=name)
            self.group_repo.add_group(group)
            return "GROUP_ADDED"
        except mariadb.IntegrityError as e:
            return e.msg
        
    def delete_group(self, name: str, role_claims: str) -> str:
        """
        Service method to delete a group
        Args:
            name (str): the name of the group to delete
        Returns: A status message
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            self.group_repo.delete_group(name)
            return "GROUP_DELETED"
        except mariadb.Error as e:
            return e.msg
        
    def rename_group(self, old_name: str, new_name: str, role_claims: str) -> str:
        """
        Service method to rename a group
        Args:
            old_name (str): the current name of the group
            new_name (str): the new name for the group
        Returns: A status message
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            self.group_repo.rename_group(old_name, new_name)
            return "GROUP_RENAMED"
        except mariadb.Error as e:
            return e.msg
        
    def add_user_to_group(self, email: str, group_name: str, role_claims: str) -> str:
        """
        Service method to add a user to a group
        Args:
            email (str): the email of the user to add
            group_name (str): the name of the group
        Returns: A status message
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            self.group_repo.add_user_to_group(email, group_name)
            return "USER_ADDED_TO_GROUP"
        except mariadb.Error as e:
            return e.msg
        
    def remove_user_from_group(self, email: str, group_name: str, role_claims: str) -> str:
        """
        Service method to remove a user from a group
        Args:
            email (str): the email of the user to remove
            group_name (str): the name of the group
        Returns: A status message
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            self.group_repo.remove_user_from_group(email, group_name)
            return "USER_REMOVED_FROM_GROUP"
        except mariadb.Error as e:
            return e.msg
        
    def get_groups_of_user(self, email: str, role_claims: str):
        """
        Service method to retrieve all groups of a user
        Args:
            email (str): the email of the user
        Returns: A list of group names
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        return self.group_repo.get_groups_of_user(email)
        