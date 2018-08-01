from flask import Blueprint

__author__ = 'courage kosana'


item_blueprint = Blueprint('items', __name__)


@item_blueprint.route('/item/<string:name>')
def item_page(name):
    pass
