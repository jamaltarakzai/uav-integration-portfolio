import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------
# 1. read and clean (same as analysis.py)
# ------------------------------------------------------------
df = pd.read_csv("data/testing_file.csv")
df.columns = [c.strip() for c in df.columns]
df["t"] = df["GNSS H"]*3600 + df["GNSSM"]*60 + df["GNSS S"]
df["t"] = df["t"] - df["t"].iloc[0]
df = df[df["t"] > df["t"].cummax().shift(1, fill_value=-1)]

# 2. keep only the columns we need (never Latitude / Longitude)
keep = ["t", "Current pitch", "Target pitch", "Current roll", "Target roll",
        "Heading", "Target heading", "Rudder(%)", "Throttle(%)",
        "Ground altitude(m)", "Voltage2(V)"]
df = df[keep]

# ------------------------------------------------------------
# 3. style: one place for colours and fonts
# ------------------------------------------------------------
BLUE, ORANGE, AQUA, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6", "#e34948"
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
FONT = "Inter, Segoe UI, Arial, sans-serif"

titles = ("Attitude: actual (solid) vs target (dashed)",
          "Heading: target held, aircraft spins",
          "Controller outputs: both pinned at their limits",
          "Height above take-off point",
          "Battery voltage (6S)")

fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                    row_heights=[0.25, 0.22, 0.22, 0.16, 0.15],
                    subplot_titles=titles)

groups = {1: "Attitude", 2: "Heading", 3: "Controller", 4: "Height", 5: "Battery"}

def line(col, name, row, color, unit, dash="solid", width=2):
    fig.add_trace(go.Scatter(
        x=df["t"], y=df[col], name=name, mode="lines",
        line=dict(color=color, width=width, dash=dash),
        legendgroup=str(row), legendgrouptitle_text=groups[row],
        hovertemplate="%{y:.1f} " + unit),
        row=row, col=1)

line("Current pitch", "pitch", 1, BLUE, "deg")
line("Target pitch", "target pitch", 1, BLUE, "deg", "dash", 1.5)
line("Current roll", "roll", 1, ORANGE, "deg")
line("Target roll", "target roll", 1, ORANGE, "deg", "dash", 1.5)

line("Heading", "heading", 2, VIOLET, "deg")
line("Target heading", "target heading", 2, MUTED, "deg", "dash", 1.5)

line("Rudder(%)", "yaw output", 3, RED, "%")
line("Throttle(%)", "throttle", 3, AQUA, "%")

line("Ground altitude(m)", "height", 4, BLUE, "m")
line("Voltage2(V)", "battery", 5, ORANGE, "V")

# ------------------------------------------------------------
# 4. context: limits, event band, key labels
# ------------------------------------------------------------
fig.add_hline(y=84, line=dict(color=MUTED, width=1, dash="dot"), row=3, col=1,
              annotation_text="throttle limit 84%", annotation_position="top left",
              annotation_font=dict(size=11, color=MUTED))
fig.add_hline(y=-20, line=dict(color=MUTED, width=1, dash="dot"), row=3, col=1,
              annotation_text="yaw limit -20%", annotation_position="bottom left",
              annotation_font=dict(size=11, color=MUTED))

fig.add_vrect(x0=853, x1=862, fillcolor=RED, opacity=0.07, line_width=0)

fig.add_annotation(x=855, y=-103, text="inverted: roll -103 deg", row=1, col=1,
                   showarrow=True, arrowhead=0, arrowcolor=MUTED, ax=70, ay=0,
                   font=dict(size=11, color=INK), bgcolor=SURFACE)
fig.add_annotation(x=854, y=236, text="uncommanded yaw: 116 deg in 2 s", row=2, col=1,
                   showarrow=True, arrowhead=0, arrowcolor=MUTED, ax=-120, ay=40,
                   font=dict(size=11, color=INK), bgcolor=SURFACE)
fig.add_annotation(x=861, y=-24, text="-35 m in 7 s", row=4, col=1,
                   showarrow=True, arrowhead=0, arrowcolor=MUTED, ax=60, ay=0,
                   font=dict(size=11, color=INK), bgcolor=SURFACE)
fig.add_annotation(x=844, y=-6, text="constant yaw correction before the event",
                   row=3, col=1, showarrow=False, yshift=14,
                   font=dict(size=11, color=MUTED))

# ------------------------------------------------------------
# 5. axes, crosshair, layout
# ------------------------------------------------------------
fig.update_xaxes(range=[830, 870], gridcolor=GRID, zeroline=False,
                 showspikes=True, spikemode="across", spikesnap="cursor",
                 spikethickness=1, spikedash="dot", spikecolor=MUTED)
fig.update_xaxes(title_text="time from log start (s)", row=5, col=1)
fig.update_yaxes(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED))
for row, unit in [(1, "deg"), (2, "deg"), (3, "%"), (4, "m"), (5, "V")]:
    fig.update_yaxes(title_text=unit, row=row, col=1)

fig.update_annotations(font_family=FONT)
for a in fig.layout.annotations[:5]:          # the five panel titles
    a.update(x=0, xanchor="left", font=dict(size=13, color=INK))

fig.update_layout(
    height=1150, template="plotly_white",
    paper_bgcolor=SURFACE, plot_bgcolor=SURFACE,
    font=dict(family=FONT, size=12, color=INK),
    margin=dict(l=60, r=30, t=60, b=50),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="white", bordercolor=GRID, font_family=FONT),
    legend=dict(tracegroupgap=24, groupclick="togglegroup", font=dict(color=MUTED)),
    updatemenus=[dict(type="buttons", direction="right", x=0, y=1.045,
                      xanchor="left", yanchor="bottom", showactive=True,
                      bgcolor="white", bordercolor=GRID, font=dict(size=12),
                      buttons=[dict(label="Event (830-870 s)", method="relayout",
                                    args=[{"xaxis.range": [830, 870]}]),
                               dict(label="Full flight", method="relayout",
                                    args=[{"xaxis.range": [0, 870]}])])])

chart = fig.to_html(full_html=False, include_plotlyjs="cdn",
                    config={"displaylogo": False, "responsive": True})

# ------------------------------------------------------------
# 6. the web page around the chart
# ------------------------------------------------------------
page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>C-001 Multirotor upset: flight log analysis</title>
<style>
  body { margin:0; background:#f4f3ef; color:#0b0b0b;
         font-family: Inter, "Segoe UI", Arial, sans-serif; }
  .wrap { max-width:1180px; margin:0 auto; padding:32px 20px 48px; }
  .tag { display:inline-block; font-size:12px; letter-spacing:.08em; text-transform:uppercase;
         color:#52514e; border:1px solid #d9d8d3; border-radius:999px; padding:3px 10px; }
  h1 { font-size:28px; margin:12px 0 6px; }
  .lead { color:#52514e; font-size:16px; line-height:1.55; max-width:820px; margin:0 0 22px; }
  .tiles { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:18px; }
  .tile { background:#fcfcfb; border:1px solid #e6e5e1; border-radius:12px; padding:14px 16px; }
  .tile b { display:block; font-size:24px; }
  .tile span { color:#52514e; font-size:13px; }
  .card { background:#fcfcfb; border:1px solid #e6e5e1; border-radius:14px; padding:10px; }
  .cols { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:18px; }
  .cols .card { padding:16px 20px; }
  h2 { font-size:16px; margin:4px 0 8px; }
  li { line-height:1.6; color:#2b2a28; }
  .note { color:#52514e; font-size:13px; margin-top:18px; line-height:1.5; }
  @media (max-width:800px){ .tiles{grid-template-columns:1fr 1fr} .cols{grid-template-columns:1fr} }
</style></head><body><div class="wrap">
  <span class="tag">Case C-001 &middot; flight log analysis</span>
  <h1>Multirotor upset at 854 s</h1>
  <p class="lead">In steady forward flight the aircraft suddenly spun and rolled inverted.
  The controller drove yaw and throttle to their limits for 8 s before it recovered.
  Battery, GPS, radio link, flight mode and the attitude sensor were all normal:
  the evidence points to a sudden, temporary loss of thrust on one motor, propeller or ESC.</p>

  <div class="tiles">
    <div class="tile"><b>116&deg; / 2 s</b><span>uncommanded yaw</span></div>
    <div class="tile"><b>-103&deg;</b><span>peak roll (inverted)</span></div>
    <div class="tile"><b>8 s</b><span>yaw output pinned at limit</span></div>
    <div class="tile"><b>3.78 V/cell</b><span>battery before the event</span></div>
  </div>

  <div class="card">{{CHART}}</div>

  <div class="cols">
    <div class="card"><h2>Ruled out</h2><ul>
      <li>Battery: healthy before the event; sag followed throttle and recovered</li>
      <li>GPS: 28 satellites, 1 m accuracy</li>
      <li>Radio link and failsafe: RC rate steady 66-67 Hz, mode never changed</li>
      <li>Sensor or controller fault: INS steady 200 Hz, error word 0</li>
    </ul></div>
    <div class="card"><h2>Evidence for motor / prop / ESC</h2><ul>
      <li>Target heading held at 352&deg; while the aircraft spun</li>
      <li>Yaw output at its -20% limit and throttle at 84% together</li>
      <li>Yaw output sat at -5 to -7% through normal flight: an existing imbalance</li>
      <li>Recovery after 8 s: loss was temporary (e.g. ESC desync, loose prop)</li>
    </ul></div>
  </div>

  <p class="note">Source: 1 Hz ground-station telemetry. 6 duplicated rows removed, one record (853 s) missing.
  No per-motor RPM in the log, so the specific motor cannot be identified from data alone.
  Hover for values, drag to zoom, double-click to reset, click a legend group to hide it.</p>
</div></body></html>"""

with open("c001_interactive.html", "w", encoding="utf-8") as f:
    f.write(page.replace("{{CHART}}", chart))
print("saved: c001_interactive.html")
