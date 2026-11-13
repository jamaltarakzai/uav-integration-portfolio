# T6/T7: VTOL back-transition test (PX4 SITL)

## Objective
Measure how VT_B_TRANS_DUR changes the back transition (FW -> MC).

## Setup
- PX4 SITL + Gazebo, model: standard_vtol
- MIS_TAKEOFF_ALT = 30 m, VT_ARSP_TRANS = 10 m/s
- One parameter changed per run; all others default

## Results (PlotJuggler: vtol_vehicle_status, airspeed_validated, vehicle_local_position)
| Run | VT_B_TRANS_DUR | Front transition | Back transition | Max altitude loss in FW |
|-----|----------------|------------------|-----------------|-------------------------|
| 1   | 10 s           | 2.0 s            | 5.0 s           | 8.0 m                   |
| 2   | 4 s            | 2.0 s            | ~4 s (limit)    | 7.3 m                   |

## Findings
1. Front transition completed at ~10-12 m/s airspeed, matching VT_ARSP_TRANS = 10 m/s.
2. Run 1: back transition ended by itself at 5.0 s, before the 10 s limit.
3. Run 2: back transition was cut at the 4 s limit; after switching to MC the vehicle
   still had ~3 m/s airspeed and showed ~2 m altitude bumps.
4. Largest altitude loss was not in transition but in the first FW loiter turn
   (bank up to 47 deg): altitude was traded for airspeed (energy trade).
5. Recommendation: VT_B_TRANS_DUR should be longer than the natural deceleration
   time (~5 s for this model); avoid steep turns right after front transition.

## Tools
PX4 ULog (.ulg), PlotJuggler 4, Flight Review.
