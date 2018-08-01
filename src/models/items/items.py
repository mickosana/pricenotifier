import re

import requests
from bs4 import BeautifulSoup
from src.models.stores.stores import Store
from src.common.database import Database
import uuid
import src.models.items.constants as ItemConstants


class Item(object):
    def __init__(self, name, url,price=None ,_id=None):
        self.name = name
        self.url = url
        store = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query = store.query
        self._id = uuid.uuid4().hex if _id == None else _id
        self.price = None if price is None else price


    def __repr__(self):
        return "Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        # <span id="priceblock_ourprice" class="a=size-medium a-color-price">$2,499.00</span>
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name,self.query)
        string_price = element.text.strip()

        pattern = re.compile("(\d+.\d+)")  # extract the price from the match
        match = pattern.search(string_price)
        self.price=match.group()
        return  self.price

    def save_to_db(self):
        Database.update(ItemConstants.COLLECTION,{"_id":self._id} ,self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url": self.url,
            "price":self.price
        }
    @classmethod
    def get_by_id(cls,item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTIONS,{"_id":item_id}))