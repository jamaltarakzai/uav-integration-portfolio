# R-XXX: <one-line fault title, e.g. "No GPS lock after hard landing">

| Field | Value |
|---|---|
| Aircraft class | <e.g. heavy VTOL ~200 kg / multirotor survey drone / agri spray drone> |
| Autopilot | <PX4 / ArduPilot / proprietary> |
| Subsystem | <GNSS / FC / datalink / ESC / motor / battery / power / payload / airframe> |
| Time to repair | <e.g. 3 h> |
| Result | <Returned to service / part replaced / scrapped> |

## 1. Reported problem
What the operator or pilot reported, in one or two sentences.

## 2. Symptoms observed
What I saw myself on the bench: error messages, LEDs, ground station warnings, behaviour.

## 3. Evidence
- Measurements (voltage, continuity, resistance), with expected vs measured values
- Log plots (attach images in this folder)
- Photos of the damage (no serial numbers, no client markings)

| Test point | Expected | Measured |
|---|---|---|
| <e.g. GPS VCC> | <5.0 V> | <0.0 V> |

## 4. Diagnosis
How I narrowed the fault down, step by step, and the root cause.

## 5. Fix
What I replaced, repaired or reconfigured. Include parameter changes as code:

```
PARAM_NAME   old_value -> new_value
```

## 6. Verification
How I proved the fix: bench test, ground run, hover test, log check.

## 7. Lesson learned
One or two sentences: what this teaches, and how to prevent it.
