from model.log import Log
from util.connector import Pool
import mariadb  

class LogRepo:
    def __init__(self, databasePool: Pool):
        self.db = databasePool.get_connection()
        
        
    def get_logs(self, entity_name = None, start_timestamp= None, end_timestamp = None, keyword= None,) -> list:
        """
        Retrieve logs with optional filters.
        Args:
            entity_name: Filter by entity name.
            start_timestamp: Filter logs received after this timestamp.
            end_timestamp: Filter logs received before this timestamp.
            keyword: Filter logs containing this keyword in their message.
        Returns: A list of Log objects.
        """
        query = "SELECT ID, FromHost, ReceivedAt, Message FROM SystemEvents WHERE 1=1"
        params = []

        if entity_name:
            query += " AND FromHost = ?"
            params.append(entity_name)
        if start_timestamp:
            query += " AND DeviceReportedTime >= ?"
            params.append(start_timestamp)
        if end_timestamp:
            query += " AND DeviceReportedTime <= ?"
            params.append(end_timestamp)
        if keyword:
            query += " AND MATCH(Message) AGAINST(? IN BOOLEAN MODE)"
            params.append(f"%{keyword}%")

        cursor = self.db.cursor()
        cursor.execute(query, tuple(params))
        results = cursor.fetchall()
        logs = []
        for row in results:
            logs.append(Log(id=row[0], fromHost=row[1], receivedAt=row[2], message=row[3]))
        return logs
