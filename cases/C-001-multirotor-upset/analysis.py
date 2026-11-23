# C-001 crash investigation: analysis script
# Run: press the Run button (triangle, top right) in VS Code,
#      or in the terminal:  python3 analysis.py

import pandas as pd

# ---------------------------------------------------------------
# Step 1: read the telemetry file into a table (DataFrame)
# ---------------------------------------------------------------
df = pd.read_csv("data/testing_file.csv")
df.columns = [c.strip() for c in df.columns]   # remove extra spaces from column names

print("Rows, columns:", df.shape)

# ---------------------------------------------------------------
# Step 10: time column t (seconds from the start of the log)
# ---------------------------------------------------------------
df["t"] = df["GNSS H"] * 3600 + df["GNSSM"] * 60 + df["GNSS S"]
df["t"] = df["t"] - df["t"].iloc[0]

print("Log length:", df["t"].iloc[-1], "seconds")

# 4. remove duplicated rows (time must always go forward)
before = len(df)
df = df[df["t"] > df["t"].cummax().shift(1, fill_value=-1)]
print("removed duplicate rows:", before - len(df))
print("log length (s):", df["t"].iloc[-1])

# one row every 60 seconds: a quick look at the whole flight
cols = ["t", "Ground speed(m/s)", "Ground altitude(m)", "Throttle(%)"]
print(df[cols].iloc[::60].to_string(index=False))



# 5. event graph (last 40 seconds)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

z = df[df["t"] >= 830]

fig, ax = plt.subplots(4, 1, figsize=(11, 10), sharex=True)

ax[0].plot(z["t"], z["Current pitch"], label="pitch")
ax[0].plot(z["t"], z["Target pitch"], "--", label="target pitch")
ax[0].plot(z["t"], z["Current roll"], label="roll")
ax[0].plot(z["t"], z["Target roll"], "--", label="target roll")
ax[0].set_ylabel("deg")
ax[0].set_title("Attitude: actual vs target")

ax[1].plot(z["t"], z["Heading"], ".-", label="heading")
ax[1].plot(z["t"], z["Target heading"], "--", label="target heading")
ax[1].set_ylabel("deg")
ax[1].set_title("Heading: uncommanded yaw / spin")

ax[2].plot(z["t"], z["Rudder(%)"], label="yaw output (rudder)")
ax[2].plot(z["t"], z["Throttle(%)"], label="throttle")
ax[2].axhline(-20, color="red", linestyle=":", label="yaw limit -20%")
ax[2].axhline(84, color="black", linestyle=":", label="throttle limit 84%")
ax[2].set_ylabel("%")
ax[2].set_title("Controller outputs: both at their limits")

ax[3].plot(z["t"], z["Ground altitude(m)"], label="altitude (m)")
ax[3].plot(z["t"], z["Voltage2(V)"], label="battery (V)")
ax[3].set_ylabel("m / V")
ax[3].set_xlabel("time from log start (s)")
ax[3].set_title("Altitude and battery")

for a in ax:
    a.axvspan(853, 862, color="red", alpha=0.1)
    a.grid(True)
    a.legend(loc="upper left", fontsize=8)

fig.suptitle("C-001: loss of control at 854 s")
fig.tight_layout()
fig.savefig("event.png", dpi=120)
print("saved: event.png")
