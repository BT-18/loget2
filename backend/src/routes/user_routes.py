from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt

user_bp = Blueprint('user', __name__, url_prefix='/user')

def init_user_routes(user_service):
    @user_bp.route("/add", methods=["POST"])
    @jwt_required()
    def add_user():
        data = request.json
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")
        totp = data.get("totp")
        role_claims = get_jwt().get("role", "")
        result = user_service.add_user(email, password, role, totp, role_claims)
        if result == "USER_ADDED":
            return {"msg":"USER_ADDED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @user_bp.route("/delete", methods=["POST"])
    @jwt_required()
    def delete_user():
        data = request.json
        email = data.get("email")
        role_claims = get_jwt().get("role", "")
        result = user_service.delete_user(email, role_claims)
        if result == "USER_DELETED":
            return {"msg":"USER_DELETED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501

    @user_bp.route("/authenticate", methods=["POST"])
    def authenticate():
        data = request.json
        email = data["email"]
        password = data["password"]
        access_token = user_service.authenticate(email, password)
        if access_token == "ERROR":
            return {"msg": "ERROR"}, 501
        elif access_token == "AUTH_FAILED":
            return {"msg": "AUTH_FAILED"}, 401
        elif access_token == "TOTP_REQUIRED":
            return {"msg": "TOTP_REQUIRED"}, 401
        else:
            return {"access_token": access_token}, 200
    
    @user_bp.route("/check_totp", methods=["POST"])
    def check_totp():
        data = request.json
        email = data.get("email")
        password = data.get("password")
        totp = data.get("totp")
        access_token = user_service.check_totp(email, password, totp)
        if access_token == "ERROR":
            return {"msg": "ERROR"}, 501
        elif access_token == "AUTH_FAILED":
            return {"msg": "AUTH_FAILED"}, 401
        elif access_token == "TOTP_FAILED":
            return {"msg": "TOTP_FAILED"}, 401
        else:
            return {"access_token": access_token}, 200
        
    @user_bp.route("/update_email", methods=["POST"])
    @jwt_required()
    def update_email():
        data = request.json
        old_email = data.get("old_email")
        new_email = data.get("new_email")
        identity = get_jwt()["sub"]
        role_claim = get_jwt().get("role", "")
        result = user_service.update_email(old_email, new_email, identity, role_claim)
        if result == "EMAIL_UPDATED":
            return {"msg":"EMAIL_UPDATED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @user_bp.route("/update_password", methods=["POST"])
    @jwt_required()
    def update_password():
        data = request.json
        email = data.get("email")
        new_password = data.get("new_password")
        identity = get_jwt()["sub"]
        role_claim = get_jwt().get("role", "")
        result = user_service.update_password(email, new_password, identity, role_claim)
        if result == "PASSWORD_UPDATED":
            return {"msg":"PASSWORD_UPDATED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    @user_bp.route("/update_totp", methods=["POST"])
    @jwt_required()
    def update_totp():
        data = request.json
        email = data.get("email")
        new_totp = data.get("new_totp")
        identity = get_jwt()["sub"]
        role_claim = get_jwt().get("role", "")
        result = user_service.update_totp(email, new_totp, identity, role_claim)
        if result == "TOTP_UPDATED":
            return {"msg":"TOTP_UPDATED"}, 200
        else:
            return {"msg":f"ERROR {result}"}, 501
        
    return user_bp