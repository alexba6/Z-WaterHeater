from flask import Flask
from .router import user, auth

api = Flask(__name__)

api.register_blueprint(user.userRouter)
api.register_blueprint(auth.authRouter)
