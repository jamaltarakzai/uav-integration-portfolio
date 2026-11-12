# T6/T7: VTOL back-transition test (PX4 SITL)

## Objective
Measure how VT_B_TRANS_DUR changes the back transition (FW -> MC).

## Setup
- PX4 SITL + Gazebo, model: standard_vtol
- MIS_TAKEOFF_ALT = 30 m, VT_ARSP_TRANS = 10 m/s
- One parameter changed per run; all others default

## Results (from flight logs, Flight Review)
| Run | VT_B_TRANS_DUR | Front transition | Back transition | Altitude in back transition |
|-----|----------------|------------------|-----------------|-----------------------------|
| 1   | 10 s           | 2.5 s            | 5.7 s           | no loss (+1 m)              |
| 2   | 4 s            | 2.5 s            | 4.0 s           | ~1 m loss                   |

## Findings
1. Run 1: back transition finished by itself at 5.7 s, before the 10 s limit.
2. Run 2: back transition was cut at exactly 4.0 s by the limit. The vehicle
   switched to MC while still moving (~4 m/s), so lift motors had to absorb it.
3. Recommendation: VT_B_TRANS_DUR should be longer than the natural
   deceleration time of the vehicle (~6 s for this model).
4. Largest altitude loss (~7-8 m) was not in transition but in the first
   FW loiter turn (bank up to 47 deg). Lesson: avoid steep turns right after
   front transition.

## Tools
Flight Review, PX4 logs (.ulg), topics: vtol_vehicle_status, roll angle, altitude estimate.# T6: VTOL transition test (SITL)
- Params: VT_ARSP_TRANS=..., VT_ARSP_BLEND=..., VT_B_TRANS_DUR=...
- Takeoff alt: 30 m (MIS_TAKEOFF_ALT)
- Run 1: front ... s, back ... s (VT_B_TRANS_DUR default)
- Run 2: back ... s (VT_B_TRANS_DUR = 8)
- Finding: smoot transition for this model
- Params reset to default after test
