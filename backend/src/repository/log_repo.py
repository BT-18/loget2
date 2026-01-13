from model.log import Log
from util.connector import Pool
import mariadb  

class LogRepo:
    def __init__(self, databasePool: Pool):
        self.pool = databasePool
        
    def get_logs(self, entities_names: list, start_timestamp=None, end_timestamp=None, keyword=None, limit=50, offset=0) -> list:
        """
        Retrieve logs with optional filters.
        Args:
            entity_name: Filter by entity name.
            start_timestamp: Filter logs received after this timestamp.
            end_timestamp: Filter logs received before this timestamp.
            keyword: Filter logs containing this keyword in their message.
            limit: Maximum number of logs to return (default 1000)
            offset: Number of logs to skip (default 0)
        Returns: A list of Log objects.
        """
        conn = self.pool.get_connection()
        try:
            query = "SELECT ID, FromHost, ReceivedAt, Message FROM SystemEvents WHERE 1=1"
            params = []

            if entities_names:
                placeholders = ','.join('?' for _ in entities_names)
                query += f" AND FromHost IN ({placeholders})"
                params.extend(entities_names)
            if start_timestamp:
                query += " AND DeviceReportedTime >= ?"
                params.append(start_timestamp)
            if end_timestamp:
                query += " AND DeviceReportedTime <= ?"
                params.append(end_timestamp)
            if keyword:
                query += " AND MATCH(Message) AGAINST(? IN BOOLEAN MODE)"
                params.append(keyword)
            
            query += " ORDER BY ReceivedAt DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            logs = []
            for row in results:
                logs.append(Log(id=row[0], fromHost=row[1], receivedAt=row[2], message=row[3]))
            return logs
        finally:
            conn.close()
