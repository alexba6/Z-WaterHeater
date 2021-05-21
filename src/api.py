from flask import Flask
from .router import user, auth, token

api = Flask(__name__)

api.register_blueprint(user.userRouter)
api.register_blueprint(auth.authRouter)
api.register_blueprint(token.tokenRouter)
