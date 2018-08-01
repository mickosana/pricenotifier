import uuid

from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store(object):
    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.tag_name = tag_name
        self.query = query
        self._id = uuid.uuid4().hex if _id == None else _id

    def __repr__(self):
        return "<Store {} >".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTIONS, {"_id": id}))

    def save_to_mongo(self):
        Database.insert(StoreConstants.COLLECTIONS, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTIONS, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        """

        :param url_prefix:
        :return:
        """
        return cls(
            **Database.find_one(StoreConstants.COLLECTIONS, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}}))

    @classmethod
    def find_by_url(cls, url):
        """
        return a store from a url
        :param url: the item's url
        :return: a store or a raises a store not found exception if no store was found

        """
        for i in range(0, len(url) + 1):
            try:
                store = cls.get_by_url_prefix(url[:i])
                return store
            except:
                raise StoreErrors.StoreNoteFoundError("the store was not found")
