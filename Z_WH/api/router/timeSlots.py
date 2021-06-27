from flask import Blueprint
from Z_WH.api.controllers.timeSlot import timeSlotAdd, timeSlotUpdate, timeSlotGet, timeSlotDelete

timeSlotRouter = Blueprint('timeSlot', __name__, url_prefix='/api/time-slot')


# Add time slot
timeSlotRouter.route(
    '',
    endpoint='addTimeSlot',
    methods=['POST']
)(timeSlotAdd.addTimeSlotCtrl)

# Update many time slots
timeSlotRouter.route(
    '',
    endpoint='updateTimeSlot',
    methods=['PUT']
)(timeSlotUpdate.updateTimeSlotCtrl)

# Get all time slots
timeSlotRouter.route(
    '',
    endpoint='getAllTimeSlot',
    methods=['GET']
)(timeSlotGet.getTimeSlotCtrl)

# Delete time slots
timeSlotRouter.route(
    '/<slotId>',
    endpoint='deleteTimeSlot',
    methods=['DELETE']
)(timeSlotDelete.deleteTimeSlotCtrl)
