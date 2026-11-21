import sys
import pandas as pd
from pyulog import ULog
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ulog = ULog(sys.argv[1])
t0 = ulog.start_timestamp

def table(name):
    df = pd.DataFrame(ulog.get_dataset(name).data)
    df["t"] = (df["timestamp"].astype("int64") - t0) / 1e6
    return df

vtol = table("vtol_vehicle_status")

NAMES = {1:"TRANS->FW", 2:"TRANS->MC", 3:"MC", 4:"FW"}

s = vtol["vehicle_vtol_state"]
change = s != s.shift()
seg = vtol[change][["t", "vehicle_vtol_state"]].reset_index(drop=True)
seg['end'] = seg['t'].shift(-1)
seg['dur'] = seg['end'] - seg['t']

print("State        start(s)  duration(s)")
for _, r in seg.iterrows():
    name = NAMES.get(int(r["vehicle_vtol_state"]), "?")
    print(f"{name:12s} {r['t']:8.2f}  {r['dur']:8.2f}")

front = seg[seg["vehicle_vtol_state"] == 1]["dur"].iloc[0]
back = seg[seg["vehicle_vtol_state"] == 2]["dur"].iloc[0]
print(f"\nFront transition: {front:.2f} s   Back transition: {back:.2f} s")

pos = table("vehicle_local_position")
pos["alt"] = -pos["z"]

fw = seg[seg["vehicle_vtol_state"] == 4].iloc[0]
w = pos[(pos["t"] >= fw["t"]) & (pos['t'] <= fw['end'])]

alt_start = w['alt'].iloc[0]
low = w.loc[w['alt'].idxmin()]
dip = alt_start - low['alt']

print(f"FW start altitude: {alt_start:.1f}m")
print(f"Lowest in FW: {low['alt']:.1f} m at {low['t']:.1f} s")
print(f"Max altitude loss in FW: {dip:.1f} m")

air = table("airspeed_validated")

fig, axs = plt.subplots(3, 1, figsize=(12, 8), sharex=True)

axs[0].plot(pos["t"], pos["alt"])
axs[0].set_ylabel("altitude (m)")

axs[1].plot(air["t"], air["true_airspeed_m_s"])
axs[1].set_ylabel("airspeed (m/s)")

axs[2].step(vtol["t"], vtol["vehicle_vtol_state"], where="post")
axs[2].set_ylabel("vtol state")
axs[2].set_xlabel("time (s)")

for ax in axs:
    ax.axvspan(fw["t"], fw["end"], color="orange", alpha=0.2)
    ax.grid(True)

axs[0].plot(low["t"], low["alt"], "rv")
axs[0].set_title(sys.argv[1] + f"  |  FW dip {dip:.1f} m")

out = sys.argv[1].replace(".ulg", "_report.png")
fig.tight_layout()
fig.savefig(out, dpi=120)
print("saved", out)
