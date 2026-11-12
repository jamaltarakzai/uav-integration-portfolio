# T6: VTOL transition test (SITL)
- Params: VT_ARSP_TRANS=..., VT_ARSP_BLEND=..., VT_B_TRANS_DUR=...
- Takeoff alt: 30 m (MIS_TAKEOFF_ALT)
- Run 1: front ... s, back ... s (VT_B_TRANS_DUR default)
- Run 2: back ... s (VT_B_TRANS_DUR = 8)
- Finding: smoot transition for this model
- Params reset to default after test
