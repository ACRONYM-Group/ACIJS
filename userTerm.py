import ACI
import time
import json

def defInput(prompt, default):
    value = input(prompt)
    if value == "":
        value = default

    return value

print(" ")
print("Welcome to the ACI User Terminal")
print(" ")
    
if defInput("connect to 127.0.0.1:8765 with name 'main'? ('yes'): ", "yes") == "yes":
    ACI.init("client", 8765)

time.sleep(0.1)

while True:
    print(" ")
    cmd = input("Command?: ")
    if cmd == "set":
        ACI.set(defInput("Key ('val'): ", "val"), defInput("dbKey ('db1')?: ", "db1"), input("Val: "))
    
    if cmd == "sets":
        ACI.set(defInput("Key ('val'): ", "val"), defInput("dbKey ('db1')?: ", "db1"), input("Val: "), input("ServerID?: "))

    if cmd == "get":
        value = ACI.get(defInput("Key ('val')?: ", "val"), defInput("dbKey ('db1')?: ", "db1"))
        print("----------------")
        print("Value = " + str(value))
    
    if cmd == "gets":
        value = ACI.get(defInput("Key ('val')?: ", "val"), defInput("dbKey ('db1')?: ", "db1"), input("ServerID?: "))
        print("----------------")
        print("Value = " + str(value))

    if cmd == "ls":
        listOfItems = ACI.listDatabase(defInput("dbKey ('db1')?: ", "db1"))
        print(" ")
        for item in listOfItems:
            print(item)

    if cmd == "lss":
        listOfItems = ACI.listDatabase(defInput("dbKey ('db1')?: ", "db1"), input("ServerID?: "))
        print(" ")
        for item in listOfItems:
            print(item)
    
    if cmd == "wtd":
        ACI.writeToDisk(defInput("serverID ('main')?: ", "main"), defInput("dbKey ('db1')?: ", "db1"))
    
    if cmd == "rfd":
        ACI.readFromDisk(defInput("ServerID ('main')?: ", "main"), defInput("dbKey ('db1')?: ", "db1"))
    
    if cmd == "cts":
        ACI.init("client", defInput("Port (8765)?: ", 8765), defInput("IP Address (127.0.0.1)?: ", "127.0.0.1"), defInput("Name ('main')?: ", "main"))

    if cmd == "help":
        print("Commands:")
        print("-----------------------------------------------------------------------------------")
        print("get - Used for retrieving a value from the default server")
        print("gets - Used for retrieving a value from a specific server")
        print("set - Used for setting a value on the server")
        print("sets - Used for setting a value on a specific server")
        print("ls - list keys in the database")
        print("lss - list keys in the database of a specific server")
        print("wtd - Short for Write To Disk, which forces the server to dump a Database to disk")
        print("rfd - Short for Read From Disk, which forces the server to read a Database from disk")
        print("cts - Short for Connect To Server, which causes the terminal to connect to a new ACI Server")
        print("help - Displays this help sheet")
        print("-----------------------------------------------------------------------------------")
        print("Terminology")
        print("-----------------------------------------------------------------------------------")
        print("key - the name/index of a value in a database")
        print("dbKey - the name of a database")
        print("val - short for Value")
        print("ServerID - the local name of a server")


