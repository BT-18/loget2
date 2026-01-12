import mariadb
import sys

pool_config = {
    "pool_name": "pool1",
    'host': 'localhost',
    'port': 3306,
    'user': 'rsyslog',
    'password': '1234',
    'database': 'Syslog',
    "pool_size": 10
}


class Pool:
    """Class to manage a pool of database connections using MariaDB."""
    def __init__(self):
        """
        Constructor for the connection pool
        """
        self.pool = mariadb.ConnectionPool(**pool_config)

    def get_connection(self):
        """
        Get a connection from the pool
        Returns: A connection object
        """
        try:
            conn = self.pool.get_connection()
            return conn
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            sys.exit(1)
            
