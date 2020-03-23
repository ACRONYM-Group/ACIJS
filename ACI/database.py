import json
import os


class Item:
    def __init__(self, key, value, owner, read=False, rootDir="./", read_db=""):
        self.key = key
        self.value = value
        self.owner = owner
        self.subs = []
        self.rootDir = rootDir
        
        if read:
            self.read_from_disk(read_db)
    
    def get_val(self):
        return self.value

    def set_val(self, value):
        self.value = value

    def write_to_disk(self, database):
        filename = "./%s/" % database
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != os.errno.EEXIST:
                    raise

        with open("./%s/%s.Item" % (database, self.key), 'w') as file:
            file.write(json.dumps([self.key, self.value, self.owner, self.subs]))

    def read_from_disk(self, read_db):
        try:
            filename = self.rootDir + "%s/%s.Item" % (read_db, self.key)
            with open(filename, 'r') as file:
                print("Reading", filename)
                data = json.loads(file.read())

            _, self.value, self.owner, self.subs = data
        except Exception:
            print("WARNING")
            print("-Unable to read " + str(self.rootDir + read_db + "/" + self.key + ".Item"))


class Database:
    def __init__(self, name, read=False, rootDir="./"):
        self.data = {}
        self.name = name
        self.rootDir = rootDir

        if read:
            self.read_from_disk()

    def get(self, key):
        if key in self.data:
            return self.data[key].get_val()
        else:
            return None

    def set(self, key, value):
        if not (key in self.data):
            self.new_item(key, value)
        self.data[key].set_val(value)

        self.data[key].write_to_disk(self.name)

    def new_item(self, key, value, owner="self"):
        self.data[key] = Item(key, value, owner, rootDir=self.rootDir)

    def write_to_disk(self):
        filename = "./" + self.name + "/"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != os.errno.EEXIST:
                    raise

        item_keys = []
        for val in self.data.values():
            val.write_to_disk(self.name)
            item_keys.append(val.key)

        with open(self.rootDir + "%s/%s.Database" % (self.name, self.name), "w") as file:
            file.write(json.dumps([self.name, item_keys]))

    def read_from_disk(self):
        filename = self.rootDir + "%s/%s.Database" % (self.name, self.name)
        with open(filename, 'r') as file:
            print(filename)
            db_data = json.loads(file.read())

        for itemKey in db_data[1]:
            self.data[itemKey] = Item(itemKey, "None", "None", read=True, read_db=self.name)
