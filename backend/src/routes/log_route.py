from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from service.log_service import *

log_bp = Blueprint('log', __name__, url_prefix='/log')

def init_log_routes(log_service):
    
    #identity, entities_names, start_timestamp= None, end_timestamp = None, keyword= None
    
    @log_bp.route("/get_logs", methods=["GET"])
    @jwt_required()
    def get_logs():
        data = request.json
        entities = data.get("entities")
        start_timestamp = data.get("start_timestamp")
        end_timestamp = data.get("end_timestamp")
        keyword = data.get("keyword")
        identity = get_jwt_identity()
        result = log_service.get_logs(identity, entities, start_timestamp, end_timestamp, keyword)
        return result
    
    return log_bp