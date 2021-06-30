from flask import Blueprint
from Z_WH.api.controllers.settings import (
    settingsTempSaver,
    settingsMail,
    settingsOutput,
    settingsTempLimit
)

settingsRouter = Blueprint('settings', __name__, url_prefix='/api/settings')


# Get temp save settings
settingsRouter.route(
    '/temp-saver',
    endpoint='getTempSaverSettings',
    methods=['GET']
)(settingsTempSaver.getTempSaverSettings)

# Update temp saver settings
settingsRouter.route(
    '/temp-saver',
    endpoint='updateTempSaverSettings',
    methods=['PUT']
)(settingsTempSaver.updateTempSaverSettings)

# Get mail settings
settingsRouter.route(
    '/mail',
    endpoint='getMailSettings',
    methods=['GET']
)(settingsMail.getMailSettings)

# Update mail settings
settingsRouter.route(
    '/mail',
    endpoint='updateMailSettings',
    methods=['PUT']
)(settingsMail.updateMailSettings)

# Get output settings
settingsRouter.route(
    '/output',
    endpoint='getOutputSettings',
    methods=['GET']
)(settingsOutput.getTempSaverSettings)

# Update output settings
settingsRouter.route(
    '/output',
    endpoint='updateOutputSettings',
    methods=['PUT']
)(settingsOutput.updateTempSaverSettings)

# Get temp limit settings
settingsRouter.route(
    '/temp-limit',
    endpoint='getTempLimitSettings',
    methods=['GET']
)(settingsTempLimit.getTempLimitSettings)

# Update temp limit settings
settingsRouter.route(
    '/temp-limit',
    endpoint='updateTempLimitSettings',
    methods=['PUT']
)(settingsTempLimit.updateTempLimitSettings)
