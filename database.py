import asyncio 
import websockets
import json
import os

class item:
    def __init__(self, key, value, owner, read=False, readdb=""):
        self.key = key
        self.value = value
        self.owner = owner
        self.subs = []
        
        if (read == True):
            self.readFromDisk(readdb)
    
    def get(self):
        return self.value

    def set(self, value):
        self.value = value

    def writeToDisk(self, database):
        filename = "./" + str(database) + "/"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        file = open("./" + str(database) + "/" + str(self.key) + ".item","w")
        file.write(json.dumps([self.key, self.value, self.owner, self.subs]))
        file.close()

    def readFromDisk(self, readdb):
        file = open("./" + readdb + "/" + self.key + ".item")
        print("Reading "+ str("./" + readdb + "/" + self.key + ".item"))
        data = json.loads(file.read())
        file.close()
        self.value = data[1]
        self.owner = data[2]
        self.subs = data[3]

class database:
    def __init__(self, name, read=False):
        self.data = {}
        self.name = name

        if read == True:
            self.readFromDisk()

    def get(self, key):
        if (key in self.data):
            return self.data[key].get()
        else:
            return None

    def set(self, key, value):
        if not (key in self.data):
            self.newItem(key, value)
        self.data[key].set(value)

        self.data[key].writeToDisk(self.name)

    def newItem(self, key, value, owner="self"):
        self.data[key] = item(key, value, owner)

    def writeToDisk(self):
        filename = "./" + self.name + "/"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        itemKeys = []
        for itemKey in self.data:
            self.data[itemKey].writeToDisk(self.name)
            itemKeys.append(self.data[itemKey].key)

        file = open("./" + self.name + "/" + self.name + ".database", "w")
        file.write(json.dumps([self.name, itemKeys]))
        file.close()

    def readFromDisk(self):
        file = open("./" + self.name + "/" + self.name + ".database")
        print("Reading " + str("./" + self.name + "/" + self.name + ".database"))
        dbData = json.loads(file.read())
        file.close()
        for itemKey in dbData[1]:
            self.data[itemKey] = item(itemKey, "None", "None", read=True, readdb=self.name)

        
    
