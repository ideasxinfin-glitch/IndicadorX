# LI Lab — project handoff for Claude Code

Read this file before changing the TradingView Pine indicator. The user wants to continue this project with Claude Code and expects the work to build on the recorded versions, not restart from scratch.

## User's goal and working preferences

- Maintain an independent English-language Pine Script v6 reconstruction of the visible concepts and settings of EzTrades ManipulationX V.8. Its source is protected and unavailable; do not claim exact source equivalence.
- The user trades NQ intraday using ICT / Smart Money concepts, chiefly 1m and 30s execution, 5m/15m continuation context, HTF FVGs at 15m/1h/4h, New York's 09:30–11:00 main window and optional 08:00–12:10 extension, plus London and Asia sessions.
- Preserve the distinction: base R = eligible liquidity sweep + LTF FVG inversion; R+ = R with sweep-linked HTF delivery; C = trend/DOL + retest of a fresh 5m/15m FVG + LTF inversion. A+ and checklist counts are experimental confluence descriptions, never validated win probabilities.
- Prioritize understandable English settings grouped by feature, optional family-by-family appearance controls, legible charts, historical visibility and acceptable load/runtime behavior. The user's request is iterative improvement without losing a known rollback.
- Never say the indicator is “100% functional,” accurate, profitable, or validated from a short sample. Separate visual changes from model changes and disclose whether each candidate was actually compiled and compared in TradingView.

## Version status — read before publishing or replacing anything

- **0.26 is the last user-installed/reference candidate**. It remains the rollback. Source: `outputs/Liquidity-Inversion-Lab-v26-gap-age.pine`.
- **0.27 is a local experimental candidate only**: `outputs/Liquidity-Inversion-Lab-v27-visual.pine`. The user's first TradingView compile screenshot showed CE10235 in `f_archiveSwing`/its caller. The local helper/caller branches have been adjusted to return consistent `void`, but this correction has not yet been confirmed by a fresh Pine compilation. Do not represent it as live or ready for use. Its release notes are `outputs/Release-v27-visual.md`.
- The user already installed earlier private LI Lab versions. Creating or editing a local `.pine` file does not publish it to TradingView; adding/saving a script there and checking compilation are separate steps.
- Browser automation recently stopped because it could not establish the active browser URL with enough certainty to apply policy. Do not bypass that restriction with hidden browser protocols. Continue local work or explain that the user must compile/paste the candidate themselves if TradingView remains inaccessible.
- The delivery archive `outputs/ManipulationX-Laboratorio-entrega.zip` includes the v27 file, report and preserved older artifacts; v27 is still marked pending inside its release notes.

## What 0.27 changes

1. Chart-timeframe FVG/iFVG view defaults to “Signal-linked only”; “All gaps” is optional. Only inverted gaps satisfying the signal's existing gap eligibility and participating in a confirmed R/R+/C are drawn. The box starts at its earlier gap origin, so that historical edge is not an advance signal. HTF 15m/1h/4h boxes have separate existing controls.
2. Organizes the English inputs into numbered feature families. Adds independent label shape/size and line-style controls across sessions, references, liquidity, sweeps, EQH/EQL, LRL and SMT. TradingView owns the native settings dialog's header font and cannot provide custom jump buttons.
3. Retains a bounded visual history of retired swing lines without reintroducing those levels into signal calculations. Lowers the *display-only* swing-size threshold from 5 to 1.5 ATR(200); this affected 44 versus 22 pivots in the supplied CSV reconstruction.
4. Separates LRL visible-line limit from analytical structure retention (default 4 to preserve the previous model cap). Adds a provisional “Balanced” geometry profile (1.5 ATR(14) alignment / 8 ATR(200) cluster) and a “Custom / v26” option (previous adjustable defaults 0.5 / 4). The wider profile passes one NQ swing structure that v26 rejected, but is not calibrated against the protected indicator and can change LRL/DOL availability and C signals.
5. Adds customizable SMT line labels and a toggle for confirmation-bar text. SMT pairing calculations remain unchanged; exactness cannot be verified from NQ-only data.
6. Carries forward the recorded user's matched 0.26 test inputs as new-instance defaults: short pivots on, chart FVG minimum 0.5 points, all eligible inversions required, signal gap age 20 bars, V window 3. Other personal TradingView inputs may differ; compare with all relevant settings visibly matched.

## Validation already performed and still needed

- Local source-level checks passed for input dependency order, unchanged R/C predicates, SMT conditions, plot/alert call budget, signal-to-gap ownership exclusions, a 20,000-bar display-pool simulation and basic intact-LRL geometry cases. These do not substitute for Pine compilation.
- CSV `C:/Users/Felipe Plascencia/Downloads/CME_MINI_NQ1!, 1 (11).csv`: 710 one-minute NQ bars, approximately 02:48–14:37 New York on Oct 2, 2026. ATR warmup and the limited sample can differ from TradingView's longer chart history. See `outputs/Structure-audit-v27.md`.
- The corrected v25/v26 comparison with the user's matched settings had 19 signals per version, 16 exact matches, 3 added and 3 absent at their former timestamps, no same-bar reclassifications; it does not validate v27. See `outputs/CSV-validation-v25-v26-corrected.md`.
- A prior original-versus-reconstruction comparison found differences; for example the 10:41 classification remained unresolved. Do not erase that discrepancy from project notes.
- Next: compile v27 in TradingView, inspect 30s and 1m; compare v26/v27 with matched inputs, first using “Custom / v26” geometry then Balanced; inspect signal-linked FVG boxes, LRL expiry, and runtime/object limits. Export same-period, same-timezone **ES1! 1m OHLC** to check the SMT pivot pairs alongside NQ.
- Inspect Pine `request.security`, confirmed-bar behavior, object limits, history handling, alert/plot budget and the user's loaded settings before changing code. Avoid lookahead/repainting claims unless verified.

## Repository state (GitHub `IndicadorX`, started 2026-10-02)

- The repo was seeded with only this file plus the 0.27 source the user pasted into chat: `outputs/Liquidity-Inversion-Lab-v27-visual.pine`. The first line of the paste read `/@version=6`, an apparent copy truncation; it was restored to `//@version=6`. Nothing else was changed.
- **Not yet in the repo:** the v26 rollback source, the release notes, audits, CSV comparisons, the delivery zip and the `work/` scripts listed below. They exist only on the user's machine. Do not recreate them from memory. Ask the user to upload them, starting with v26.
- Static counts for the v27 file: 15 `request.security` calls, 19 plot/plotshape calls, 40 `alertcondition` calls. These are counts only; nothing has been compiled.

- **0.28 (`outputs/Liquidity-Inversion-Lab-v28-performance.pine`) is a load-time candidate built from 0.27** by `work/build_v28_performance.py`: scoped `max_bars_back`, D/W/M request merge (15 → 11 calls), signal-linked chart-gap retention = `signalGapAge`. Intended to be behavior-identical; not compiled or compared. See `outputs/Release-v28-performance.md`.

## Important project files

- Current installed/reference source: `outputs/Liquidity-Inversion-Lab-v26-gap-age.pine`
- Unvalidated successor: `outputs/Liquidity-Inversion-Lab-v27-visual.pine`
- v27 feature/validation details: `outputs/Release-v27-visual.md`
- CSV-derived structure audit: `outputs/Structure-audit-v27.md` and `.json`
- Matched v25/v26 CSV comparison: `outputs/CSV-validation-v25-v26-corrected.md` and `.json`
- All prior source versions and delivery notes: `outputs/ManipulationX-Laboratorio-entrega.zip`
- Reproducible v27 source builder: `work/build_v27_visual.py`
- Local verification/audit scripts: `work/verify_v27_visual.py`, `work/audit_v27_structure.py`
- Earlier regression checks: `work/verify_v25_performance.py`, `work/verify_v16_lrl.py`, `work/verify_v20_models.py`

Before editing, inspect the current tree and these files. Preserve 0.26, build changes as a new candidate, document input/default changes, compare signals on identical closed bars, and update the delivery archive only after preserving the old versions. Never report compile or upload success without directly observing it in TradingView.
