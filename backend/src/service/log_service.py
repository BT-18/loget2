from repository.group_repo import GroupRepo
from repository.log_repo import *
from repository.user_repo import *
from model.entity import *
from model.log import *
from model.group import *
import mariadb



class LogService:
    def __init__(self, databasePool: Pool):
        """Initialize the LogService with a database connection pool"""
        self.log_repo = LogRepo(databasePool)
        self.user_repo = UserRepo(databasePool)
        
    def get_logs(self, identity, entities_names, start_timestamp=None, end_timestamp=None, keyword=None, limit=1000, offset=0):
        """
        Service method to retrieve logs with optional filters.
        Args:
            identity :
            entities_names: Filter by entity names.
            start_timestamp: Filter logs received after this timestamp.
            end_timestamp: Filter logs received before this timestamp.
            keyword: Filter logs containing this keyword in their message.
            limit: Maximum number of logs to return
            offset: Number of logs to skip
        Returns: A list of Log objects.
        """
        print("identity for getting logs: ", identity)
        authorized_entities = self.user_repo.get_entities_of_users(identity)
        
        if entities_names is None:
            entities_names = []
        
        final_entity_list = []
        if not entities_names:  
            final_entity_list = authorized_entities
        else:
            for entity in entities_names:
                if entity in authorized_entities:
                    final_entity_list.append(entity)
        
        return self.log_repo.get_logs(entities_names=final_entity_list, start_timestamp=start_timestamp, end_timestamp=end_timestamp, keyword=keyword, limit=limit, offset=offset)