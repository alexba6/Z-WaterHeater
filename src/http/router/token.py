from flask import Blueprint
from src.http.controllers.token import code

tokenRouter = Blueprint('token', __name__, url_prefix='/api/token')


tokenRouter.route('/generate-code', endpoint='generate-code', methods=['GET'])(code.generate_code_ctrl)
tokenRouter.route('/check-code',  endpoint='check-code', methods=['POST'])(code.check_code)
