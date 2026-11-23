import sys
from pyulog import ULog

names = ["VT_B_TRANS_DUR", "VT_B_DEC_MSS", "MPC_XY_CRUISE"]

for path in sys.argv[1:]:
    ulog = ULog(path)
    t0 = ulog.start_timestamp
    print("===", path)
    for n in names:
        print(f"  {n:16s} start = {ulog.initial_parameters.get(n)}")
    for t, n, v in ulog.changed_parameters:
        if n in names:
            print(f"  {n:16s} changed at {(t - t0) / 1e6:7.1f} s -> {v}")
