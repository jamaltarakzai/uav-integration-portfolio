import sys
import pandas as pd
from pyulog import ULog

ulog = ULog(sys.argv[1])
t0 = ulog.start_timestamp


def table(name):
    df = pd.DataFrame(ulog.get_dataset(name).data)
    df["t"] = (df["timestamp"] - t0) / 1e6
    return df


for name in ["vtol_vehicle_status", "airspeed_validated", "vehicle_local_position"]:
    df = table(name)
    dt = df["t"].diff().median()
    print(f"{name:25s} every {dt:.3f} s  ({1/dt:.1f} Hz)")
