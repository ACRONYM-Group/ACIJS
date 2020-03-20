import ACI

ACI.init("client", 8765)
print(ACI.get("val", "db1"))
