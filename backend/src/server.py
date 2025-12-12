from flask import Flask, request
from util.connector import Pool
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from service.user_service import UserService
from routes.user_routes import init_user_routes
 

app = Flask(__name__)
databasePool = Pool()

userService = UserService(databasePool)

app.config['SECRET_KEY'] = 'test'
app.config["JWT_SECRET_KEY"] = 'test'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

jwt = JWTManager(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(init_user_routes(userService))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)