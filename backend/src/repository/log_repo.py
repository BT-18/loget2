from model.log import Log
from util.connector import Pool
import mariadb  

class LogRepo:
    def __init__(self, databasePool: Pool):
        self.db = databasePool.get_connection()
        

        
    def get_logs_from_entity(self, entity_name: str) -> list:
        """
        Retrieve all logs associated with a specific entity
        Args:
            entity_name (str): the name of the entity
        Returns: A list of Log objects
        """
        query = "SELECT ID, FromHost, ReceivedAt, Message FROM SystemEvents WHERE FromHost = ?"
        cursor = self.db.cursor()
        cursor.execute(query, (entity_name,))
        results = cursor.fetchall()
        logs = []
        for row in results:
            logs.append(Log(id=row[0], fromHost=row[1], receivedAt=row[2], message=row[3]))
        return logs
    
    def get_logs_before_timestamp(self, timestamp: str) -> list:
        """
        Retrieve all logs received before a specific timestamp
        Args:
            timestamp (str): the timestamp to filter logs
        Returns: A list of Log objects
        """
        query = "SELECT ID, FromHost, ReceivedAt, Message FROM SystemEvents WHERE DeviceReportedTime < ?"
        cursor = self.db.cursor()
        cursor.execute(query, (timestamp,))
        results = cursor.fetchall()
        logs = []
        for row in results:
            logs.append(Log(id=row[0], fromHost=row[1], receivedAt=row[2], message=row[3]))
        return logs
    
