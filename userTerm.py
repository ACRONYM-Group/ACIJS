import ACI
import time

print(" ")
print("ACI User Terminal")
print(" ")
    
ACI.init("client", 8765)

while True:
    print(" ")
    cmd = input("Command?: ")
    if cmd == "set":
        ACI.set(input("Key: "), input("dbKey: "), input("Val: "))

    if cmd == "get":
        value = ACI.get(input("Key: "), input("dbKey: "))
        print("----------------")
        print("Value = " + str(value))

