from flask import Blueprint
from Z_WH.api.controllers.outGroup import groupGet, groupAdd, groupUpdate, groupDelete

outGroupRouter = Blueprint('outGroup', __name__, url_prefix='/api/out-group')


# Get group
outGroupRouter.route(
    '',
    endpoint='getGroup',
    methods=['GET']
)(groupGet.getGroupCtrl)


# Add group
outGroupRouter.route(
    '',
    endpoint='addGroup',
    methods=['POST']
)(groupAdd.addGroupCtrl)


# Update group
outGroupRouter.route(
    '/<groupId>',
    endpoint='updateGroup',
    methods=['PUT']
)(groupUpdate.updateGroupCtrl)

# Delete group
outGroupRouter.route(
    '/<groupId>',
    endpoint='deleteGroup',
    methods=['DELETE']
)(groupDelete.deleteGroupCtrl)
