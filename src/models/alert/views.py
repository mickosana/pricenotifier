from flask import Blueprint, render_template, request, session

from src.models.alert.alerts import Alert
from src.models.items.items import Item

alert_blueprint = Blueprint("alerts", __name__)
@alert_blueprint.route('/')
def index():
    return "this is the alerts homepage"

@alert_blueprint.route('/new', methods=['POST','GET'])
def create_alert():
    if request.method==['POST']:
        name=request.form['name']
        url=request.form['url']
        price_limit=request.form['price_limit']
        item=Item(name,url)
        item.save_to_db()
        alert=Alert(session['email'],price_limit,item._id)
        Alert.save_to_mongo(alert)
    return render_template('alerts/create_alert.html')



@alert_blueprint.route('/deactivate/<string:item_id>')
def deactivate_alert(alert_id):
    pass


@alert_blueprint.route('<string:alert_id>')
def get_alert_page(alert_id):
    alert=Alert.find_by_id(alert_id)
    return render_template('alerts/alert.html',alert=alert)


@alert_blueprint.route('/for_user/<string:user_id>')
def get_alerts_for_user(user_id):
    pass
