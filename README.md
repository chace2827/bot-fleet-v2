# bot-fleet-v2

Systematic 0DTE options program on Option Alpha — rebuilt 2026-07-30 as a clean project after a forensic
audit found the previous folder's config record wrong and its exit engine silently dead since June. This
folder holds only the corrected record: the ledger (`data/trades.csv`) plus an explicit corrections layer
(`data/corrections.csv`), the forensics that produced it, and the loop being built to make sure it never
drifts again. Start with `CLAUDE.md`, then `docs/current-state.md`. The old folder `~/bot-fleet` is a
permanent read-only archive — never modify it.
