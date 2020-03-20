import asyncio 
import websockets

class item:
    def __init__(self, key, value, owner):
        self.key = key
        self.value = value
        self.owner = owner
        self.subs = []
    
    def get(self):
        return self.value

    def set(self, value):
        self.value = value

class database:
    def __init__(self):
        self.data = {}

    def get(self, key):
        if (key in self.data):
            return self.data[key].get()
        else:
            return None

    def set(self, key, value):
        if not (key in self.data):
            self.newItem(key, value)
        self.data[key].set(value)

    def newItem(self, key, value, owner="self"):
        self.data[key] = item(key, value, owner)
        
    
