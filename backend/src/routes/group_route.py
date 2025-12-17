from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

group_bp = Blueprint('group', __name__, url_prefix='/group')

def init_group_routes(group_service):
    
    @group_bp.route("/add", methods=["POST"])
    @jwt_required()
    def add_group():
        data = request.json
        name = data.get("name")
        role_claims = get_jwt().get("role", "")
        result = group_service.add_group(name, role_claims)
        if result == "GROUP_ADDED":
            return {"msg":"GROUP_ADDED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @group_bp.route("/delete", methods=["POST"])
    @jwt_required()
    def delete_group():
        data = request.json
        name = data.get("name")
        role_claims = get_jwt().get("role", "")
        result = group_service.delete_group(name, role_claims)
        if result == "GROUP_DELETED":
            return {"msg":"GROUP_DELETED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    
    
    return group_bp