# Collecte automatique et vérification des sources — Market Intelligence

**Statut : architecture documentée, pas collecte automatique déjà déployée.** La version 0.1 du dépôt valide un snapshot fourni et produit un PDF/JSON. Elle ne se connecte pas encore à Reuters, Yahoo Finance, Investing.com, Boursorama, IBKR ou à un flux de cotations temps réel.

## 1. Ce que fait un assistant avec recherche web

Un assistant disposant de recherche web peut effectuer des requêtes ciblées, ouvrir certaines pages accessibles, extraire des faits, lire leurs dates et liens, comparer les sources puis synthétiser les résultats.

Il ne s'agit ni d'un robot permanent qui aspire les sites, ni d'un accès direct garanti aux bases propriétaires. Les mécanismes internes de ChatGPT et son raisonnement privé ne sont pas publiés ici.

Pipeline conceptuel et reproductible :

    APIs officielles ou flux licenciés --------> Collecteur structuré
                                                   |
    Recherche web accessible ---------------> Extraction documentaire
                   |                               |
                   +------------> Vérificateur <---+
                                      |
                           Faits vs interprétations
                           vs hypothèses conditionnelles
                                      |
                          Rapport institutionnel PDF/JSON
                                      |
                          Alpha Lab / Quorum AI (recherche)

Une citation ne suffit pas à prouver la justesse d'un chiffre. Vérifier indépendamment unités, niveau, variations, source, heure, période de référence et type de cours.

## 2. Comparatif Reuters, Yahoo Finance, Investing.com et Boursorama

| Site | Accès informatif | Limites à considérer | Recommandation |
|---|---|---|---|
| Reuters | Pages accessibles, articles indexés et liens; produits sous licence | Ne pas reproduire ou scraper les contenus Reuters sans les autorisations exigées pour le service concerné | Attribution + liens, flux sous licence si nécessaire |
| Yahoo Finance | Pages publiques; bibliothèques non officielles telles que yfinance | Les bibliothèques non officielles ne constituent pas une licence commerciale ni une API officiellement garantie | Prototype personnel; flux licencié pour production |
| Investing.com | Pages accessibles, widgets développeur | Le support Investing indique ne pas offrir d'API publique | Utiliser les widgets dans leurs conditions ou choisir un fournisseur tiers |
| Boursorama | Actualités et pages consultables | Certaines conditions Boursorama interdisent la récupération automatisée et encadrent la redistribution | Consultation, liens; demander autorisation pour collecteur |

Conditions et références (leurs périmètres varient selon les services, à recontrôler avant de déployer) :

- Reuters Connect (conditions propres à ce produit) : https://cdn1.agency.thomsonreuters.com/static/Reuters-Connect-Platform-Terms-and-Conditions.pdf
- Thomson Reuters Developers : https://developers.thomsonreuters.com/terms-of-use
- Yahoo API Terms (ne constituent pas une licence générale Yahoo Finance) : https://legal.yahoo.com/us/en/yahoo/terms/product-atos/apitnc/index.html
- Investing.com, absence d'API publique : https://www.investing-support.com/hc/en-us/articles/115005473825-Do-You-Offer-API-Access-at-Investing-com
- Boursorama, mentions légales/CGU : https://www.boursorama.com/aide/mentions-legales-et-cgu
- Boursorama, conditions membre historiques (vérifier l'applicabilité actuelle) : https://www.boursorama.com/static/pdf/cg-licensing/cgu-membres.pdf

Ne jamais contourner protections techniques, CAPTCHA, paywalls, restrictions de débit ni droits de diffusion. L'accès à une page ne donne pas automatiquement les droits de la collecter ni de redistribuer ses données.

## 3. Architecture des données recommandée

| Besoin | Source recommandée | Précaution |
|---|---|---|
| EUR/USD et séries BCE | https://data.ecb.europa.eu/help/api/data | API SDMX, fixing != spot temps réel |
| Treasury US 2/10 ans | https://home.treasury.gov/resource-center/data-chart-center/interest-rates | Référence journalière, non cotation live |
| Séries économiques et anciennes versions | https://fred.stlouisfed.org/docs/api/fred/ | Clé API et vintages ALFRED pour reconstitution historique |
| Inflation, emploi US | https://www.bls.gov/audience/developers.htm | API publique avec quotas et versions distinctes |
| PIB, PCE | https://www.bea.gov/resources/for-developers | API officielle |
| Bund 2/10 ans | https://www.bundesbank.de/ | Série/teneur précise à identifier |
| CAC / EuroStoxx / Nasdaq / S&P | Administrateurs des indices et fournisseur autorisé | Licence de cotation/redistribution à confirmer |
| Filings et résultats | https://www.sec.gov/edgar/search/ | Source primaire, suivre le dépôt et l'heure d'accès |
| ETF | Sites des émetteurs | Composition datée, expositions indirectes et licences |
| Pétrole et or | Fournisseurs licenciés, ICE/CME pour futures | Spot vs future, contrat et échéance |

Privilégier les API officielles pour les chiffres, la recherche documentaire pour les explications, et l'IA pour la rédaction en distinguant faits, attributions et hypothèses.

## 4. Exemple exécutable EUR/USD

Voir [examples/ecb_eurusd.py](../examples/ecb_eurusd.py).

    python examples/ecb_eurusd.py

Ce script utilise uniquement la bibliothèque standard Python et l'API BCE officielle, série EXR/D.USD.EUR.SP00.A ; il récupère deux dernières observations de référence. Documentation de l'endpoint : https://data.ecb.europa.eu/help/api/data-examples

La date TIME_PERIOD est une **date d'observation**, pas la preuve de l'heure exacte de publication. Le script constitue un démonstrateur de collecte, pas un archiveur point-in-time ni un flux forex temps réel.

## 5. Provenance : informations à conserver pour chaque chiffre

- Identifiant de l'instrument et de la série, fournisseur, URL source.
- Valeur, unité, variation, méthode et base de comparaison.
- Type : clôture, fixing, référence journalière, intrajournalier, différé ou indisponible.
- Période observée et heure de fin de séance.
- Heure de publication, heure de récupération, délai fournisseur et première disponibilité **démontrée**.
- Date de version/révision (vintage), licence et avertissements.
- Fuseau explicite, de préférence ISO 8601 avec offset et IANA Europe/Paris pour le calendrier.

Le schéma actuel du dépôt est moins riche : ces champs avancés sont une **cible de développement**, pas des fonctionnalités déjà présentes.

À 08:00 Paris, les actions US n'ont pas ouvert pour la nouvelle séance : utiliser la clôture régulière précédente, et distinguer futurs/prémarché. Le fixing BCE n'est pas un cours live. Ne jamais remplacer silencieusement une valeur manquante par un cours historique.

## 6. Recherche Alpha Lab / Quorum AI : éviter le look-ahead bias

Distinguer quatre événements temporels :

1. Observation : séance ou mois auquel se rapporte la statistique.
2. Publication : quand le fournisseur a réellement diffusé la statistique.
3. Récupération : quand notre collecteur l'a reçue.
4. Disponibilité pour le modèle : première preuve qu'elle pouvait être utilisée.

Exemple : une statistique d'octobre publiée en novembre ne peut pas entrer dans un backtest du 31 octobre, même si son observation porte sur octobre.

De même, une version révisée téléchargée aujourd'hui ne peut pas remplacer rétroactivement la version initiale sans journaliser sa vintage. FRED/ALFRED permettent de travailler sur les révisions, mais il faut encore établir les instants de disponibilité et les latences réelles.

Politique d'ingestion envisagée, **non codée dans la v0.1** :

    Rejeter les données synthétiques ou sans droits établis.
    Isoler les observations dont la disponibilité historique est inconnue.
    Rejeter toute observation devenue disponible après l'heure de décision.
    Versionner chaque publication et correction.
    Alimenter uniquement un contexte de recherche en lecture seule.
    Ne transmettre aucun ordre à un moteur de trading.

## 7. Ordre des prochaines réalisations

1. Connecteurs BCE, Treasury, FRED/ALFRED, BLS et BEA.
2. Cotations indices/ETF/matières premières via fournisseur autorisé.
3. Extraction et attribution de l'actualité, avec source et heure.
4. Base append-only, historique des versions, contrôles point-in-time.
5. Planification 08:00 Europe/Paris et livraison PDF avec contrôles.
6. Plus tard : accès privé IBKR lecture seule.
7. Consommateur recherche privé Alpha Lab / Quorum AI, sans ordres.

**Ce document n'active aucune collecte automatique ni connexion à un compte.**
