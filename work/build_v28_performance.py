"""Build LI Lab 0.28 (load-time candidate) from the 0.27 source.

Every edit is an exact, single-occurrence replacement so the diff stays auditable.
Model rules (R / R+ / C, SMT, LRL, sweeps) are not touched.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "outputs" / "Liquidity-Inversion-Lab-v27-visual.pine"
DST = ROOT / "outputs" / "Liquidity-Inversion-Lab-v28-performance.pine"

text = SRC.read_text(encoding="utf-8")


def replace_once(old: str, new: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected 1 occurrence, found {count}: {old[:80]!r}")
    text = text.replace(old, new)


# 1. Version labels only.
replace_once('indicator("Liquidity Inversion Lab [experimental 0.27 EN]", "LI Lab 0.27 EN", overlay=true, max_bars_back=5000, ',
             'indicator("Liquidity Inversion Lab [experimental 0.28 EN]", "LI Lab 0.28 EN", overlay=true, ')
replace_once('"LI Lab 0.27 EN\\n"', '"LI Lab 0.28 EN\\n"')
replace_once('"LI LAB 0.27 EN"', '"LI LAB 0.28 EN"')

# 2. Scope the 5000-bar history buffer to the only series that need it.
#    Only f_lrl reads high[offset] / low[offset] with a dynamic offset up to 4000
#    (when "Allow crossing between LRL pivots" is off). Every other history
#    reference uses a fixed or input-sized offset that Pine sizes automatically.
replace_once('string Q = "👁 00 ━ QUICK VIEW · SHOW / HIDE"\n',
             '// 0.28: a 5000-bar buffer only for the series f_lrl scans with a dynamic offset,\n'
             '// instead of a global max_bars_back that sized every series in the script.\n'
             'max_bars_back(high, 5000)\n'
             'max_bars_back(low, 5000)\n\n'
             'string Q = "👁 00 ━ QUICK VIEW · SHOW / HIDE"\n')

# 3. Merge D / W / M requests: 7 calls -> 3. Same symbol, timeframe and lookahead,
#    so each value is identical to the separate call it replaces.
replace_once('[priorDH, priorDL] = request.security(syminfo.tickerid, "D", [high[1], low[1]], lookahead=barmerge.lookahead_on)\n'
             '[priorWH, priorWL] = request.security(syminfo.tickerid, "W", [high[1], low[1]], lookahead=barmerge.lookahead_on)\n'
             '[priorMH, priorML] = request.security(syminfo.tickerid, "M", [high[1], low[1]], lookahead=barmerge.lookahead_on)\n',
             '// Current period OPEN is fixed at period start; prior values use [1]. One request per timeframe.\n'
             '[priorDH, priorDL, dayOpen] = request.security(syminfo.tickerid, "D", [high[1], low[1], open], lookahead=barmerge.lookahead_on)\n'
             '[priorWH, priorWL, weekOpen, priorWeekClose] = request.security(syminfo.tickerid, "W", [high[1], low[1], open, close[1]], lookahead=barmerge.lookahead_on)\n'
             '[priorMH, priorML, monthOpen] = request.security(syminfo.tickerid, "M", [high[1], low[1], open], lookahead=barmerge.lookahead_on)\n')
replace_once('// Current period OPEN is fixed at period start; no future high/low/close is requested.\n'
             'dayOpen = request.security(syminfo.tickerid, "D", open, lookahead=barmerge.lookahead_on)\n'
             'weekOpen = request.security(syminfo.tickerid, "W", open, lookahead=barmerge.lookahead_on)\n'
             'priorWeekClose = request.security(syminfo.tickerid, "W", close[1], lookahead=barmerge.lookahead_on)\n'
             'monthOpen = request.security(syminfo.tickerid, "M", open, lookahead=barmerge.lookahead_on)\n',
             '// dayOpen / weekOpen / priorWeekClose / monthOpen are requested with the prior-period levels above.\n')

# 4. Chart-gap retention. In "Signal-linked only" mode no gap older than
#    signalGapAge can participate (f_ready and f_drawLinkedGaps both require
#    bar_index - born <= signalGapAge) and none has a box of its own, so keeping
#    300 bars only made five per-bar loops longer. "All gaps" keeps 300 for drawings.
replace_once('    // Chart-gap state has a deterministic time horizon independent of drawing count.\n'
             '    // Keep 300 bars for historical drawings and legacy experiments; readiness still\n'
             '    // uses signalGapAge. Neither horizon depends on the number of visible boxes.\n'
             '    int retainBars = math.max(300, signalGapAge)\n',
             '    // Chart-gap state has a deterministic time horizon independent of drawing count.\n'
             '    // "All gaps" keeps 300 bars so its boxes keep updating; "Signal-linked only" keeps\n'
             '    // exactly the signalGapAge window that readiness and linked drawing can use.\n'
             '    // Linked boxes live in linkedGapBoxes and are not deleted by this expiry.\n'
             '    int retainBars = chartGapScope == "All gaps" ? math.max(300, signalGapAge) : signalGapAge\n')

DST.write_text(text, encoding="utf-8")
print(f"wrote {DST.relative_to(ROOT)}")
