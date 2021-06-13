from flask import Blueprint

from ..controllers.setting import smtp, operationState, tempChart

settingRouter = Blueprint('setting', __name__, url_prefix='/api/setting')


settingRouter.route('/smtp', endpoint='get-smtp', methods=['GET'])(smtp.getSMTPSettingCtrl)
settingRouter.route('/smtp', endpoint='update-smtp', methods=['PUT'])(smtp.updateSMTPSettingCtrl)

settingRouter.route('/operation-state', endpoint='get-operation-state', methods=['GET'])(
    operationState.getOperationStateSettingCtrl
)
settingRouter.route('/operation-state', endpoint='update-operation-state', methods=['PUT'])(
    operationState.updateOperationStateSettingCtrl
)

settingRouter.route('/temp-chart', endpoint='get-temp-chart', methods=['GET'])(
    tempChart.getTempChartSettingCtrl
)
settingRouter.route('/temp-chart', endpoint='update-temp-chart', methods=['PUT'])(
    tempChart.updateTempChartSettingCtrl
)
