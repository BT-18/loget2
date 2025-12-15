from repository.entity_repo import *
from model.entity import *
import mariadb

class EntityService:
    def __init__(self, databasePool: Pool):
        """Initialize the EntityService with a database connection pool"""
        self.entity_repo = EntityRepo(databasePool)
        
    def add_entity(self, name: str, role_claims: str) -> str:
        """
        Service method to add a new entity
        Args:
            name (str): the name of the entity to add
        Returns: A status message
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            entity = Entity(name=name)
            self.entity_repo.add_entity(entity)
            return "ENTITY_ADDED"
        except mariadb.IntegrityError as e:
            return e.msg
        
    def get_all_entities(self, role_claims: str):
        """
        Service method to retrieve all entities
        Args: None
        Returns: A list of Entity objects
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        return self.entity_repo.get_all_entities()
    
    def rename_entity(self, old_name: str, new_name: str, role_claims: str) -> str:
        """
        Service method to rename an entity
        Args:
            old_name (str): the current name of the entity
            new_name (str): the new name for the entity
        Returns: A status message
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            self.entity_repo.rename_entity(old_name, new_name)
            return "ENTITY_RENAMED"
        except mariadb.Error as e:
            return e.msg
        
    def delete_entity(self, name: str, role_claims: str) -> str:
        """
        Service method to delete an entity
        Args:
            name (str): the name of the entity to delete
        Returns: A status message
        """
        if role_claims != "admin":
            return "ADMIN_PRIVILEGES_REQUIRED"
        try:
            self.entity_repo.delete_entity(name)
            return "ENTITY_DELETED"
        except mariadb.Error as e:
            return e.msg