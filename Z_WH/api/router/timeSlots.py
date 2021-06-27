from flask import Blueprint
from Z_WH.api.controllers.timeSlot import addTimeSlot, updateTimeSlot, getAllTimeSlot

timeSlotRouter = Blueprint('timeSlot', __name__, url_prefix='/api/time-slot')


# Add time slot
timeSlotRouter.route(
    '',
    endpoint='addTimeSlot',
    methods=['POST']
)(addTimeSlot.addTimeSlotCtrl)

# Update many time slots
timeSlotRouter.route(
    '',
    endpoint='updateTimeSlot',
    methods=['PUT']
)(updateTimeSlot.updateTimeSlotCtrl)

# Get all time slots
timeSlotRouter.route(
    '',
    endpoint='getAllTimeSlot',
    methods=['GET']
)(getAllTimeSlot.getTimeSlotCtrl)
