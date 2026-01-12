from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

entity_bp = Blueprint('entity', __name__, url_prefix='/entity')

def init_entity_routes(entity_service):
    
    @entity_bp.route("/add", methods=["POST"])
    @jwt_required()
    def add_entity():
        data = request.json
        name = data.get("name")
        role_claims = get_jwt().get("role", "")
        result = entity_service.add_entity(name, role_claims)
        if result == "ENTITY_ADDED":
            return {"msg":"ENTITY_ADDED"}, 200
        elif result == "ADMIN_PRIVILEGES_REQUIRED":
            return {"msg":"ADMIN_PRIVILEGES_REQUIRED"}, 403
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @entity_bp.route("/delete", methods=["POST"])
    @jwt_required()
    def delete_entity():
        data = request.json
        name = data.get("name")
        role_claims = get_jwt().get("role", "")
        result = entity_service.delete_entity(name, role_claims)
        if result == "ENTITY_DELETED":
            return {"msg":"ENTITY_DELETED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @entity_bp.route("/rename", methods=["POST"])
    @jwt_required()
    def rename_entity():
        data = request.json
        old_name = data.get("old_name")
        new_name = data.get("new_name")
        role_claims = get_jwt().get("role", "")
        result = entity_service.rename_entity(old_name, new_name, role_claims)
        if result == "ENTITY_RENAMED":
            return {"msg":"ENTITY_RENAMED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    
    
    return entity_bp