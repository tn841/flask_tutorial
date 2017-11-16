# -*- coding: utf-8 -*-
from flask.blueprints import Blueprint

board_api = Blueprint('board_api',__name__)

@board_api.route("/create_board_action", methods=['POST'])
def create_board():
    pass