from flask import Flask
from flask_cors import CORS
from src.http.router import user, auth, token, control, group

api = Flask(__name__)

CORS(api)

api.register_blueprint(user.userRouter)
api.register_blueprint(auth.authRouter)
api.register_blueprint(token.tokenRouter)
api.register_blueprint(control.controlRouter)
api.register_blueprint(group.groupRouter)
