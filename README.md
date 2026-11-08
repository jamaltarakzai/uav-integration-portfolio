# UAV Integration, Repair & Flight Test Portfolio

**Jamal Ahmed Mohmand** · UAV Technical Lead · 25+ years in avionics and unmanned systems
[LinkedIn](https://www.linkedin.com/in/jamal-ahmed-uav) · Jizan, Saudi Arabia

This repository documents real work: field repairs of UAVs, PX4 / ArduPilot configuration and
flight-log analysis, and flight test planning for a 60 kg twin-boom quadplane VTOL.
Every case shows **the problem, the evidence, the fix and the result**.

## At a glance

| Area | What this repo shows |
|---|---|
| Fleet repair | Component-level fault finding on flight controllers, GNSS, datalinks, ESCs, power systems |
| Autopilots | PX4 and ArduPilot setup, VTOL transition tuning, parameter management |
| Log analysis | Root cause from PX4 `.ulg` and ArduPilot `.bin` logs (vibration, EKF, power, link loss) |
| Integration | UART / I2C / CAN / DroneCAN wiring, MAVLink, payload and gimbal integration |
| Flight test | Test plans, test cards, go/no-go criteria, risk assessment |

## Case studies

| ID | Title | Tools | Status |
|---|---|---|---|
| S-001 | GPS loss injected in VTOL SITL, diagnosed from the flight log | PX4, Gazebo, Flight Review, PlotJuggler | planned (Dec 2026) |
| I-001 | Payload / camera pod integration: wiring, levels, control link | MAVLink, RS232/RS422, Ethernet | planned (Jan 2027) |
| F-001 | Flight test plan for a 60 kg twin-boom quadplane VTOL | PX4, test cards, risk matrix | planned (Feb 2027) |

## Repair cases

| ID | Fault | Subsystem | Result |
|---|---|---|---|
| R-001 | _first case coming soon_ | | |

## Repository layout

```
repairs/        real repair cases, one folder per case (R-001, R-002 ...)
simulation/     PX4 / ArduPilot SITL experiments and log analysis (S-xxx)
integration/    wiring diagrams, interface notes, payload integration (I-xxx)
flight-test/    test plans and test card templates (F-xxx)
cpp-for-px4/    C++ exercises from my PX4 learning track
notes/          short study notes (PX4 architecture, MAVLink ...)
templates/      the blank template used for every repair case
```

## Confidentiality
Repair cases are written from my own work with identifying details removed: no client names,
locations, serial numbers, aircraft model names or restricted documents. They describe method
and engineering reasoning only.
