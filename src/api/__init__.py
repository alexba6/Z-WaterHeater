from flask import Flask
from flask_cors import CORS
from .router import user, auth, token, control, group, temp, setting

apiHttp = Flask(__name__)
apiHttp.config['DEBUG'] = True

CORS(apiHttp)

apiHttp.config['CORS_HEADERS'] = 'Content-Type'

apiHttp.register_blueprint(user.userRouter)
apiHttp.register_blueprint(auth.authRouter)
apiHttp.register_blueprint(token.tokenRouter)
apiHttp.register_blueprint(control.controlRouter)
apiHttp.register_blueprint(group.groupRouter)
apiHttp.register_blueprint(temp.tempRouter)
apiHttp.register_blueprint(setting.settingRouter)
