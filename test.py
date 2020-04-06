import ACI
import time

conn = ACI.create(ACI.Client, port=8765)
time.sleep(1)
conn["db1"].set_item_plain("val", "Hello3")
print(conn["db1"].get_item_plain("val"))