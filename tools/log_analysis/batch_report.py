import sys
from pathlib import Path
import pandas as pd
from pyulog import ULog

def analyze(path):
    ulog = ULog(str(path))
    t0 = ulog.start_timestamp

    def table(name):
        df = pd.DataFrame(ulog.get_dataset(name).data)
        df["t"] = (df["timestamp"].astype("int64") - t0) / 1e6
        return df

    vtol = table("vtol_vehicle_status")
    s = vtol["vehicle_vtol_state"]
    seg = vtol[s != s.shift()][["t", "vehicle_vtol_state"]].reset_index(drop=True)
    seg["end"] = seg["t"].shift(-1)
    seg["dur"] = seg["end"] - seg["t"]

    states = set(seg["vehicle_vtol_state"])
    if 4 not in states:
        raise ValueError("no FW flight")
    if 1 not in states:
        raise ValueError("no front transition")
    if 2 not in states:
        raise ValueError("no back transition")

    front = seg[seg["vehicle_vtol_state"] == 1]["dur"].iloc[0]
    back = seg[seg["vehicle_vtol_state"] == 2]["dur"].iloc[0]

    pos = table("vehicle_local_position")
    pos["alt"] = -pos["z"]
    fw = seg[seg["vehicle_vtol_state"] == 4].iloc[0]
    w = pos[(pos["t"] >= fw["t"]) & (pos["t"] <= fw["end"])]
    dip = w["alt"].iloc[0] - w["alt"].min()

    return {"log": path.name,
            "front_s": round(float(front), 2),
            "back_s": round(float(back), 2),
            "dip_m": round(float(dip), 1)}




if len(sys.argv) < 2:
    print("Usage: python3 batch_report.py <folder>")
    sys.exit(1)

folder = Path(sys.argv[1])
logs = sorted(folder.rglob("*.ulg"))

print("Found", len(logs), "logs")
rows = []
for i, p in enumerate(logs, start=1):
    print(f"[{i}/{len(logs)}] {p.name}", flush=True)
    try:
        r = analyze(p)
        r["status"] = "ok"
    except Exception as e:
        r = {"log": p.name, "status": "skipped: " + str(e)}
    r["date"] = p.parent.name
    rows.append(r)

df = pd.DataFrame(rows)
df = df.reindex(columns=["date", "log", "status", "front_s", "back_s", "dip_m"])
print()
print(df.to_string(index=False))
df.to_csv("report.csv", index=False)
print("\nsaved report.csv")