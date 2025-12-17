from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from service.log_service import *

log_bp = Blueprint('log', __name__, url_prefix='/log')

def init_log_routes(log_service):
    
    #identity, entities_names, start_timestamp= None, end_timestamp = None, keyword= None
    
    @log_bp.route("/get_logs", methods=["POST"])
    @jwt_required()
    def get_logs():
        data = request.json
        entities = data.get("entities")
        start_timestamp = data.get("start_timestamp")
        end_timestamp = data.get("end_timestamp")
        keyword = data.get("keyword")
        identity = get_jwt_identity()
        role_claims = get_jwt().get("role", "")
        if result == "GROUP_ADDED":
            return {"msg":"GROUP_ADDED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
    
    return log_bp