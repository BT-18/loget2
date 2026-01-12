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
        
    @group_bp.route("/rename", methods=["POST"])
    @jwt_required()
    def rename_group():
        data = request.json
        old_name = data.get("old_name")
        new_name = data.get("new_name")
        role_claims = get_jwt().get("role", "")
        result = group_service.rename_group(old_name, new_name, role_claims)
        if result == "GROUP_RENAMED":
            return {"msg":"GROUP_RENAMED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
      
    @group_bp.route("/add_entity", methods=["POST"])
    @jwt_required()  
    def add_entity_to_group():
        data = request.json
        entity_name = data.get("entity_name")
        group_name = data.get("group_name")
        role_claims = get_jwt().get("role", "")
        result = group_service.add_entity_to_group(entity_name, group_name, role_claims)
        if result == "ENTITY_ADDED_TO_GROUP":
            return {"msg":"ENTITY_ADDED_TO_GROUP"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @group_bp.route("/remove_entity", methods=["POST"])
    @jwt_required()  
    def remove_entity_from_group():
        data = request.json
        entity_name = data.get("entity_name")
        group_name = data.get("group_name")
        role_claims = get_jwt().get("role", "")
        result = group_service.remove_entity_from_group(entity_name, group_name, role_claims)
        if result == "ENTITY_REMOVED_FROM_GROUP":
            return {"msg":"ENTITY_REMOVED_FROM_GROUP"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @group_bp.route("/add_user", methods=["POST"])
    @jwt_required()
    def add_user_to_group():
        data = request.json
        email = data.get("email")
        group_name = data.get("group_name")
        role_claims = get_jwt().get("role", "")
        result = group_service.add_user_to_group(email, group_name, role_claims)
        if result == "USER_ADDED_TO_GROUP":
            return {"msg":"USER_ADDED_TO_GROUP"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @group_bp.route("/remove_user", methods=["POST"])
    @jwt_required()
    def remove_user_from_group():
        data = request.json
        email = data.get("email")
        group_name = data.get("group_name")
        role_claims = get_jwt().get("role", "")
        result = group_service.remove_user_from_group(email, group_name, role_claims)
        if result == "USER_REMOVED_FROM_GROUP":
            return {"msg":"USER_REMOVED_FROM_GROUP"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
    
    return group_bp