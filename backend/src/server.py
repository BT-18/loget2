from flask import Flask, request
from util.connector import Pool
from service.user_service import *
from flask_jwt_extended import JWTManager, jwt_required

databasePool = Pool()

userService = UserService(databasePool)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
app.config["JWT_SECRET_KEY"] = 'test'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/add_user", methods=["POST"])
@jwt_required()
def add_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    totp = data.get("totp")
    userService.add_user(email, password, totp)
    return "<p>User added!</p>"

@app.route("/authenticate", methods=["POST"])
def authenticate():
    data = request.json
    print(data)
    email = data["email"]
    password = data["password"]
    print("email:", email, "password:", password)
    access_token = userService.authenticate(email, password)
    if access_token == "ERROR":
        return {"msg": "ERROR"}, 501
    elif access_token == "AUTH_FAILED":
        return {"msg": "AUTH_FAILED"}, 401
    elif access_token == "TOTP_REQUIRED":
        return {"msg": "TOTP_REQUIRED"}, 401
    else:
        return {"access_token": access_token}, 200
    
@app.route("/check_totp", methods=["POST"])
def check_totp():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    totp = data.get("totp")
    access_token = userService.check_totp(email, password, totp)
    if access_token == "ERROR":
        return {"msg": "ERROR"}, 501
    elif access_token == "AUTH_FAILED":
        return {"msg": "AUTH_FAILED"}, 401
    elif access_token == "TOTP_FAILED":
        return {"msg": "TOTP_FAILED"}, 401
    else:
        return {"access_token": access_token}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)