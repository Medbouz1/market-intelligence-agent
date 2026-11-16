# Architecture — what this framework does and does not do

The daily Market Intelligence assistant built in ChatGPT uses tools available inside that environment. This repo does not reproduce model internals, hidden system instructions, private reasoning, or proprietary tools.

This independently implemented framework accepts a structured JSON snapshot produced by a collector or human analyst.

    Official exchanges / Treasury / ECB / issuers / reputable press
                         |
                Pluggable collectors (future)
                         |
              timestamped snapshot + URLs
                         |
              Deterministic validation gate
                         |
             Editorial fact / interpretation / hypothesis
                         |
              Optional read-only portfolio snapshot
                         |
                      PDF + JSON
                         |
              Research-only Alpha Lab / Quorum AI

### Non-negotiable controls

- Market observations must be dated, source-linked and not later than report cutoff.
- A value that is unavailable must be null and explicitly marked unavailable.
- At 08:00 Paris, use US previous-day closes, not imaginary European intraday figures.
- Do not conflate fixing, intraday, close, delayed or daily reference.
- Market explanations must be attributed to a source; hypotheses are distinguished.
- NAV must be reconciled against positions + cash, and discrepancies shown.
- ETF domicile is not ultimate economic exposure. Constituents need independently dated look-through sources.
- No account numbers, API tokens or actual private positions in public examples.

### Implemented

This version supplies a basic offline snapshot validator and PDF/JSON renderer. It is not yet a fully automated news or market data pipeline.

### To operate every morning

Deploy your own scheduler with Europe/Paris time zone, configure data collectors with their own authorized API access, save immutable dated snapshots, then run the CLI. Do not schedule a synthetic demo as a public live report.
