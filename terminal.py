import ACI

connections = {}
LAST = None

usages = {"help": "help",
          "conn": "conn [ip] [port] [name]",
          "lsconn": "lsconn",
          "get": "get [key] [database] [server]",
          "set": "set [key] [database] [value] [server]",
          "exit": "exit",
          "ls": "ls [database] [server]",
          "write": "write [database] [server]",
          "read": "read [database] [server]"}
info = {"help": "Displays help information",
        "conn": "Connects to a new server defaults to [main] 127.0.0.1:8765",
        "lsconn": "Lists all of the currently open connections",
        "get": "Gets a value from the server server name defaults to main",
        "set": "Sets a value on the server server name defaults to main",
        "exit": "Exists the terminal",
        "ls": "Lists all of the values in a database on a server server defaults to main",
        "write": "Writes a database to disk",
        "read": "Reads a database from disk"}


def _help():
    print("Help")
    print("  Commands:")
    for cmd in usages:
        print("    %s:%s%s%s%s" % (cmd, " " * max(0, 7 - len(cmd)), usages[cmd], " " * max(40 - len(usages[cmd]), 0),
                                   info[cmd]))


def _connect(ip="127.0.0.1", port=8765, name="main"):
    global connections

    connections[name] = ACI.create(ACI.Client, port, ip, name)
    return None


def _list_connections():
    print("Connections: ")

    if len(connections.values()) == 0:
        print("\tNone")
    else:
        for name in connections:
            print("\t[%s] %s:%i" % (name, connections[name].ip, connections[name].port))


def _get(key, database, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    print("%s:%s[%s] = %s" % (server, database, key, connections[server][database][key]))


def _set(key, database, value, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    connections[server][database][key] = value
    print("%s:%s[%s] = %s" % (server, database, key, value))


def _list(database, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    result = connections[server][database].list_databases()
    if len(result) == 0:
        print("\tNone")
    else:
        for data in result:
            print("\t%s" % data)


def _write(database, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    connections[server][database].write_to_disk()


def _read(database, server="main"):
    if server not in connections:
        print("Server '%s' Not Found" % server)

    connections[server][database].read_from_disk()


instructions = {"help": _help, "conn": _connect, "lsconn": _list_connections, "get": _get, "set": _set, "ls": _list,
                "write": _write, "read": _read}


def main():
    print("ACI User Terminal\n\n")
    while instruction() is None:
        pass

    print("Exiting Terminal")
    ACI.stop()


def exec_instruction(inst, raw_args):
    global instructions

    if inst not in instructions:
        print("Unknown Instruction '%s'" % inst)
        return None

    kwargs = {}
    args = []
    current_arg = ""

    for val in raw_args:
        if val.startswith("-"):
            current_arg = val[1:]
            kwargs[current_arg] = []
        else:
            if current_arg == "":
                args.append(val)
            else:
                kwargs[current_arg].append(val)

    for key in kwargs:
        if len(kwargs[key]) == 1:
            kwargs[key] = kwargs[key][0]
        elif len(kwargs[key]) == 0:
            kwargs[key] = True

    try:
        return instructions[inst](*args, **kwargs)
    except TypeError as e:
        if e.args[0].startswith(instructions[inst].__name__):
            print("Incorrect Argument Usage")
            print("Correct Usage:", usages[inst])
        else:
            raise e


def instruction():
    global LAST

    inst = input("$> ")

    if inst == "":
        return
    elif inst == "exit":
        return False

    command, *args = inst.split(" ")

    LAST = exec_instruction(command, args)


main()
