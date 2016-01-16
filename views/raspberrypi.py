from flask import Blueprint, jsonify
from .stats import Stats

raspberrypi = Blueprint('raspberrypi', __name__)


@raspberrypi.route('/api/stats')
def stats():
    return jsonify(Stats().data())