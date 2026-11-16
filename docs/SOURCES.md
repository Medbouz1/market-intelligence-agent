# Sources and provenance policy

Prefer primary sources, then licensed market feeds, then attributed reputable financial press. Every observation needs a source URL, observation time, timezone, units, status and comparison basis.

| Topic | Primary portal |
|---|---|
| US Treasury 2Y/10Y | https://home.treasury.gov/resource-center/data-chart-center/interest-rates |
| USD/EUR reference FX | https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html |
| ECB rates and series | https://data.ecb.europa.eu/ |
| German government yields | https://www.bundesbank.de/ |
| US CPI/employment | https://www.bls.gov/ |
| US GDP/PCE | https://www.bea.gov/ |
| Euro area statistics | https://ec.europa.eu/eurostat |
| CAC 40 | https://live.euronext.com/ |
| Euro Stoxx 50 | https://www.stoxx.com/ |
| Nasdaq 100 | https://www.nasdaq.com/ |
| S&P 500 | https://www.spglobal.com/spdji/en/ |
| Corporate filings | https://www.sec.gov/edgar/search/ |
| ETF holdings | https://www.ishares.com/ |
| Oil inventory | https://www.eia.gov/ |
| Brent / WTI futures | https://www.ice.com/ / https://www.cmegroup.com/ |
| Attributed news | https://www.reuters.com/ / https://apnews.com/ |

Portal URL does not imply that a free API or redistribution license is available. Check terms, costs, delayed flags and permissions before implementation. All local clock conversions must account for US and European DST changes.

**Facts:** cite an exact observation. **Interpretations:** say who attributed it. **Hypotheses:** conditional, not observed. Consensus is not a released statistic.

Failure rule: do not fill a gap with the previous report. Mark missing as unavailable, explain why, and continue only with validated inputs.

## Collecte web, API et limites d'utilisation

Voir le [guide détaillé de collecte automatisée](COLLECTE_AUTOMATISEE.md) pour le comparatif Reuters / Yahoo Finance / Investing.com / Boursorama, les conditions d'accès, la collecte BCE et les limites des bibliothèques non officielles. Voir aussi [l'exemple officiel EUR/USD](../examples/ecb_eurusd.py).

Pour le backtesting, privilégier les **vintages historiques** et un instant de disponibilité prouvé; l'heure de l'observation n'est pas la date à laquelle un participant au marché pouvait connaître la valeur.
