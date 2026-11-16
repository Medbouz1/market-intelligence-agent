# Roadmap

## v0.1 starter
- [x] Public template, documentation, provenance policy, prompt
- [x] Offline schema checks, simulated input and safe default
- [x] Institutional PDF + JSON generator
- [x] NAV weights and reconciliation when actual data are supplied
- [x] Unit test workflow

## v0.2 — live data ingestion
- [ ] Official Treasury/ECB/Bundesbank adapter modules
- [ ] Exchange-index data via licensed providers and dated quotes
- [ ] Macro calendar releases, estimates and revisions
- [ ] Source-freshness/conflict reporting

## v0.3 — publication
- [ ] Verified LLM research pipeline and attribution QA
- [ ] Enhanced PDF with charts and full-source footnotes
- [ ] Scheduler with 08:00 Europe/Paris daylight-saving safeguards
- [ ] Private distribution and persistent history

## v0.4 — private integrations
- [ ] Secure IBKR read-only connector and NAV reconciliation tests
- [ ] Dated ETF look-through
- [ ] Currency-adjusted portfolio attribution
- [ ] Alpha Lab / Quorum AI private staging consumer
- [ ] Out-of-sample feature evaluation, strict no-look-ahead

Never activate a billable API or brokerage permission by default.

## Priorité méthodologique ajoutée (collecte)
- [ ] Conserver observation_at, published_at, retrieved_at, available_at prouvé et vintage_id pour toute publication macro ou donnée révisable
- [ ] Construire des tests de non-fuite temporelle sur données historiques et reconstitutions de publications
- [ ] Vérifier les droits des fournisseurs avant collecte automatisée ou redistribution; éviter le scraping non autorisé de Reuters, Yahoo Finance, Investing.com et Boursorama
- [ ] Intégrer l'adaptateur BCE EUR/USD de démonstration dans un véritable snapshot source-aware (exemple actuel : examples/ecb_eurusd.py)
