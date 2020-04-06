import ACI
import time

conn = ACI.create(ACI.Client)
time.sleep(2)
print(conn["db1"]["val"])