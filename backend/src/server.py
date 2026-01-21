from flask import Flask, request
from util.connector import Pool
from flask_jwt_extended import JWTManager, jwt_required, get_jwt
from service.user_service import UserService
from service.group_service import GroupService
from service.entity_service import EntityService
from service.log_service import LogService

from routes.user_route import init_user_routes
from routes.group_route import init_group_routes
from routes.entity_route import init_entity_routes
from routes.log_route import init_log_routes
 

app = Flask(__name__)
databasePool = Pool()

userService = UserService(databasePool)
groupService = GroupService(databasePool)
entityService = EntityService(databasePool)
logService = LogService(databasePool)


#app.config['SECRET_KEY'] = 'test'
app.config["JWT_SECRET_KEY"] = 'test'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = False # A METTRE A TRUE EN PRODUCTION POUR UTILISER LE HTTPS
app.config["JWT_COOKIE_CSRF_PROTECT"] = True  

jwt = JWTManager(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(init_user_routes(userService))
app.register_blueprint(init_group_routes(groupService))
app.register_blueprint(init_entity_routes(entityService))
app.register_blueprint(init_log_routes(logService))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)