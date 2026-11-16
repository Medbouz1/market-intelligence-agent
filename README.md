# Market Intelligence Agent

**Open-source framework for auditable institutional market briefings in French.**

This is a public, reproducible *reference implementation*, NOT an export of ChatGPT's hidden instructions, proprietary architecture or internal reasoning.

**Goal:** provide a shareable starter for friends and a research-only interface to Alpha Lab / Quorum AI.

## Workflow

1. Collect prices, yields, FX, commodities, macro releases and issuer publications from trusted sources.
2. Preserve URL, timestamp, timezone, observation status and comparison basis for every number.
3. Validate the snapshot. Never fill missing information with a guess.
4. Distinguish fact, sourced interpretation and conditional hypothesis.
5. Attempt portfolio reading only with explicit read-only access; never reuse old positions as current.
6. Export an A4 PDF and normalized JSON; never produce trading orders.
7. Feed verified observations (not trading decisions) to research systems.

## Setup (Python 3.11+)

    git clone https://github.com/Medbouz1/market-intelligence-agent.git
    cd market-intelligence-agent
    python -m venv .venv
    # Activate the environment, then:
    python -m pip install -e .
    market-intelligence --input examples/demo_snapshot.json --out reports --allow-synthetic

Output files: reports/market_intelligence.pdf and reports/market_intelligence.json.

**Demo data are entirely fictional. They must not be published as real financial prices.** The CLI refuses synthetic snapshots unless --allow-synthetic is explicitly passed.

To publish a real report, provide a trusted snapshot with synthetic=false, real source URLs, timestamps and citations. No built-in live quote provider or IBKR connection is claimed in v0.1.

## Repository map

- src/market_intelligence/ — validation, reconciliation, PDF exporter and CLI
- prompts/market_intelligence_fr.md — public starting prompt
- docs/SOURCES.md — official portals and source rules
- docs/ARCHITECTURE.md — design and exact implemented boundaries
- docs/ALPHA_LAB_INTEGRATION.md — research-only JSON contract
- docs/SECURITY.md — confidentiality, IBKR and model safety
- examples/ — explicitly synthetic input
- tests/ — automated verification
- ROADMAP.md — work remaining before production

## Status: implemented vs planned

| Area | Status |
|---|---|
| Source, cutoff, quote-status checks | Implemented |
| Reject synthetic reports by default | Implemented |
| PDF + JSON generation from a provided snapshot | Implemented |
| NAV/positions weights and reconciliation, when data supplied | Implemented |
| Offline unit tests | Implemented |
| Live market data ingestion | NOT integrated |
| LLM news research and fact-checking | NOT integrated |
| IBKR authentication and read-only connector | NOT integrated |
| Automatic daily delivery at 08:00 Europe/Paris | NOT deployed |
| Actual Quorum AI integration | Contract only |

## Design principles

**No invented numbers. No unsourced causality. No orders. No secrets.**

Public template: [Use this template](https://github.com/Medbouz1/market-intelligence-agent/generate).
MIT licensed. Contributions and tests welcome.
