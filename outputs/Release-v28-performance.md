# LI Lab 0.28 — load-time candidate (NOT compiled, NOT validated)

Base: `Liquidity-Inversion-Lab-v27-visual.pine` (itself still pending a TradingView compile).
Source: `Liquidity-Inversion-Lab-v28-performance.pine`, built by `work/build_v28_performance.py`.
Rollback: 0.26 (user-installed); 0.27 is kept unchanged.

## Changes (no model, input or default changes)

| # | Change | Intended effect | Behavior impact (by source reading) |
|---|--------|-----------------|-------------------------------------|
| 1 | Removed global `max_bars_back=5000`; added `max_bars_back(high, 5000)` and `max_bars_back(low, 5000)` | Pine no longer keeps a 5000-bar history buffer for every series in the script | None expected. Only `f_lrl` reads `high[offset]`/`low[offset]` with a dynamic offset (≤ 4000, only when "Allow crossing between LRL pivots" is off). All other history references use fixed/input offsets. **Risk:** if Pine's automatic buffer sizing fails somewhere, TradingView shows a max_bars_back runtime error — revert this item only. |
| 2 | D/W/M `request.security` calls merged: 7 → 3 (total 15 → 11) | Fewer security contexts to load | None: same symbol, timeframe and `lookahead_on`; `open` and `[1]` expressions are unchanged inside the tuples. |
| 3 | Chart-gap retention in "Signal-linked only" mode: 300 bars → `signalGapAge` bars (default 20). "All gaps" keeps 300. | Five per-bar loops over `gaps` (4× `f_ready` + inversion loop) and the `f_addGap` scan iterate over far fewer items | None for signals: `f_ready` and `f_drawLinkedGaps` already require `bar_index - born <= signalGapAge`; expiry uses the exact complement on the same bar, before new gaps and readiness. Linked boxes are owned by `linkedGapBoxes` and were never deleted by this expiry in signal-linked mode. `inverseBull/inverseBear` are assigned but unused. |

The size of the speed-up is **unknown**; it was not measured. TradingView's Pine Profiler would show it.

## Not changed (considered, rejected because they could alter behavior)

- Pruning touched short-pivot levels from `signalLevels` — changes which levels hit the 60-level cap.
- Sharing the `"15"` / `"60"` requests with `tf1` / `tf2` — those are editable inputs.
- Limiting calculated history (`calc_bars_count`) — would hide older signals; this is the user's call.

## Validation still required

1. Compile in TradingView (Pine Editor) — no compile has been observed.
2. Run on NQ1! 1m and 30s with v27 and v28 side by side, identical inputs; the Data Window `LAB signal code` should match bar for bar.
3. Repeat with "Allow crossing between LRL pivots" OFF (exercises item 1) and with "All gaps".
4. Optional: Pine Profiler before/after to measure load time.
