import datetime
import uuid
import requests
import src.models.alert.constants as AlertConstants
from src.common.database import Database
from src.models.items.items import Item


class Alert(object):
    def __init__(self, user_email, price_limit, item_id,last_checked=None, _id=None):
        self.user = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self._id = uuid.uuid4().hex if _id == None else _id
        self.last_checked=datetime.datetime.utcnow() if last_checked is None else last_checked

    def __repr__(self):
        return "<Alert for {} on item{} with price {}>".format(
            self.user, self.item.name, self.price_limit)

    def send(self):
        return requests.post(
            AlertConstants.URL,
            auth=("api", AlertConstants.API_KEY),
            data={
                "from": AlertConstants.FROM,
                "to": self.user.email,
                "subject": "price limit reached for {}".format(self.item.name),
                "text": "we've  found a deal (link here)"

            }

        )
    @classmethod
    def find_needing_update(cls,minutes_since_update=AlertConstants.TIMEOUT):
        last_updated_limit=datetime.datetime.utcnow()-datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTIONS,
                                                    {"last_checked":
                                                         {"$lte":last_updated_limit}

                                                     })]
    def save_to_mongo(self):
        Database.insert(AlertConstants.COLLECTIONS,{"_id":self._id},self.json())

    def json(self):
        return{
            "_id":self._id,
            "price_limit":self.last_checked,
            "user":self.user_email,
            "item_id":self.item._id
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked=datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()

        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price<self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTIONS,{'user_email':user_email})]

    @classmethod
    def find_by_id(cls,alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTIONS,{'_id':alert_id}))