import ACI

conn = ACI.create(ACI.Client, 8675, "127.0.0.1")

conn["db1"]["val"] = "Hello World!"
