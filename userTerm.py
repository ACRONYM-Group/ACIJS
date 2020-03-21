import time

import ACI


def default_input(prompt, default):
    value = input(prompt)
    if value == "":
        return default

    return value


print("\nWelcome to the ACI User Terminal\n")
    
if default_input("Connect to 127.0.0.1:8765 with name 'main'? ('yes'): ", "yes") == "yes":
    ACI.init("client", 8765)

time.sleep(0.1)

while True:
    print("")
    cmd = input("Command?: ")
    if cmd == "set_val":
        ACI.set_value(default_input("Key ('val'): ", "val"), default_input("db_key ('db1')?: ", "db1"), input("Val: "))
    
    if cmd == "sets":
        ACI.set_value(default_input("Key ('val'): ", "val"), default_input("db_key ('db1')?: ", "db1"), input("Val: "),
                      input("ServerID?: "))

    if cmd == "get_val":
        value = ACI.get(default_input("Key ('val')?: ", "val"), default_input("db_key ('db1')?: ", "db1"))
        print("----------------")
        print("Value =", str(value))
    
    if cmd == "gets":
        value = ACI.get(default_input("Key ('val')?: ", "val"), default_input("db_key ('db1')?: ", "db1"),
                        input("ServerID?: "))
        print("----------------")
        print("Value =", str(value))

    if cmd == "ls":
        database_items = ACI.list_database(default_input("db_key ('db1')?: ", "db1"))
        print(" ")
        for item in database_items:
            print(item)

    if cmd == "lss":
        database_items = ACI.list_database(default_input("db_key ('db1')?: ", "db1"), input("ServerID?: "))
        print(" ")
        for item in database_items:
            print(item)
    
    if cmd == "wtd":
        ACI.write_to_disk(default_input("serverID ('main')?: ", "main"), default_input("db_key ('db1')?: ", "db1"))
    
    if cmd == "rfd":
        ACI.read_from_disk(default_input("ServerID ('main')?: ", "main"), default_input("db_key ('db1')?: ", "db1"))
    
    if cmd == "cts":
        ACI.init("client", default_input("Port (8765)?: ", 8765),
                 default_input("IP Address (127.0.0.1)?: ", "127.0.0.1"),
                 default_input("Name ('main')?: ", "main"))

    if cmd == "help":
        print("Commands:")
        print("-----------------------------------------------------------------------------------")
        print("get_val - Used for retrieving a value from the default Server")
        print("gets - Used for retrieving a value from a specific Server")
        print("set_val - Used for setting a value on the Server")
        print("sets - Used for setting a value on a specific Server")
        print("ls - list keys in the Database")
        print("lss - list keys in the Database of a specific Server")
        print("wtd - Short for Write To Disk, which forces the Server to dump a Database to disk")
        print("rfd - Short for Read From Disk, which forces the Server to read a Database from disk")
        print("cts - Short for Connect To Server, which causes the terminal to connect to a new ACI Server")
        print("help - Displays this help sheet")
        print("-----------------------------------------------------------------------------------")
        print("Terminology")
        print("-----------------------------------------------------------------------------------")
        print("key - the name/index of a value in a Database")
        print("db_key - the name of a Database")
        print("val - short for Value")
        print("ServerID - the local name of a Server")
