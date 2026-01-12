from model.entity import *
from util.connector import Pool


class EntityRepo:
    def __init__(self, databasePool: Pool):
        self.pool = databasePool
        
    def add_entity(self, entity: Entity) -> None:
        """
        Add a new entity to the database
        Args:
            entity (Entity): the entity object to add
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "INSERT INTO Entities (name) VALUES (?)"
            cursor = conn.cursor()
            cursor.execute(query, (entity.get_name(),))
            conn.commit()
        finally:
            conn.close()
        
    def get_all_entities(self) -> list:
        """
        Retrieve all entities from the database
        Args: None
        Returns: A list of Entity objects
        """
        conn = self.pool.get_connection()
        try:
            query = "SELECT name FROM Entities"
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            entities = []
            for row in results:
                entities.append(Entity(name=row[0]))
            return entities
        finally:
            conn.close()
    
    def rename_entity(self, old_name: str, new_name: str) -> None:
        """
        Rename an existing entity
        Args:
            old_name (str): the current name of the entity
            new_name (str): the new name for the entity
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "UPDATE Entities SET name = ? WHERE name = ?"
            cursor = conn.cursor()
            cursor.execute(query, (new_name, old_name))
            conn.commit()
        finally:
            conn.close()
        
    def delete_entity(self, name: str) -> None:
        """
        Delete an entity from the database
        Args:
            name (str): the name of the entity to delete
        Returns: Nothing
        """
        conn = self.pool.get_connection()
        try:
            query = "DELETE FROM Entities WHERE name = ?"
            cursor = conn.cursor()
            cursor.execute(query, (name,))
            conn.commit()
        finally:
            conn.close()