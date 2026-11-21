import sys
from pyulog import ULog

ulog = ULog(sys.argv[1])
print("Topics in log:", len(ulog.data_list))
for d in ulog.data_list:
    n = len(d.data["timestamp"])
    print(f"{d.name:35s}{n:7d} samples")
