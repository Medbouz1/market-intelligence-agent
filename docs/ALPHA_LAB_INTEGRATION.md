# Research-only integration with Alpha Lab / Quorum AI

Existing AI Venture OS, Quorum AI and other projects are private and remain separate. This public project does not copy their code or connect to their repositories.

## JSON contract

Generated reports/market_intelligence.json contains:

- schema_version and edition.asof in an offset-aware ISO 8601 format;
- markets with value, unit, change, status, asof and source_id;
- summary and macro item kinds: fact, interpretation, hypothesis;
- risks: exactly three conditional scenarios;
- events: three upcoming entries, verified flag and sources;
- portfolio: verified + calculated weights or inaccessible;
- quality_warnings; synthetic; research_only=true; orders_enabled=false.

## Safe data flow

    Market Intelligence validated JSON
          ↓
      Private read-only ingestion
          ↓
    Time-aware historical store
          ↓
      Research features / regimes
          ↓
        Equity Desk backtesting
          ↓
      Human review, no order execution

The Quorum consumer MUST reject synthetic=true, observations arriving after its backtest cutoff, unknown source IDs, unreconciled NAV when portfolio data matter, and any payload requesting trading action.

Potential research: macro surprises vs pre-release consensus, sector rotation, oil/FX/rates sensitivity, event volatility, cross-sectional dispersion. These ideas have no proven alpha unless tested out of sample after realistic costs.

## Données as-of et disponibilité effective : exigence supplémentaire

La politique temporelle détaillée figure dans [Collecte automatique et vérification des sources](COLLECTE_AUTOMATISEE.md). Le contrat v0.1 ne vérifie encore que l'heure du snapshot et l'heure asof : **cela ne prouve pas l'absence de fuite temporelle** pour une publication macro ou une statistique révisée.

Avant d'alimenter un backtest Alpha Lab, il faudra ajouter un stockage append-only et des champs distincts pour observation, publication, récupération, disponibilité et vintage. Le consommateur de recherche devra mettre en quarantaine toute information sans date de disponibilité démontrée, et empêcher le transfert direct vers un exécuteur d'ordres.
