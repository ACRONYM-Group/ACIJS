class Item:
    """
        Database Item
    """
    def __init__(self, key, value, owner):
        self.key = key
        self.value = value
        self.owner = owner
        self.subs = []

    def get_val(self):
        return self.value

    def set_val(self, value):
        self.value = value


class Database:
    """
        Database
    """
    def __init__(self):
        self.data = {}

    def get_val(self, key):
        if (key in self.data):
            return self.data[key].get_val()
        else:
            return None

    def set_val(self, key, value):
        if not (key in self.data):
            self.new_item(key, value)
        self.data[key].set_val(value)

    def new_item(self, key, value, owner="self"):
        self.data[key] = Item(key, value, owner)
