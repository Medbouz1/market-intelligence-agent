#!/usr/bin/env python3
"""Récupère 2 observations EUR/USD de référence via l'API officielle BCE.

TIME_PERIOD = date d'observation, PAS heure effective de publication.
Ne pas utiliser seul pour un historique point-in-time.
"""
import csv
import io
from datetime import datetime, timezone
from urllib.request import Request, urlopen

URL = (
    "https://data-api.ecb.europa.eu/service/data/"
    "EXR/D.USD.EUR.SP00.A?lastNObservations=2&format=csvdata"
)


def main():
    request = Request(URL, headers={
        "Accept": "text/csv",
        "User-Agent": "market-intelligence-agent/0.1 educational example"
    })
    with urlopen(request, timeout=20) as response:
        raw = response.read().decode("utf-8-sig")
    fetched_at = datetime.now(timezone.utc).isoformat()
    rows = list(csv.DictReader(io.StringIO(raw)))
    if not rows:
        raise RuntimeError("Aucune observation renvoyée par la BCE")
    print("Source :", URL)
    print("Récupéré à UTC :", fetched_at)
    print("Statut : référence BCE (pas un taux spot temps réel)")
    for row in rows:
        date = row.get("TIME_PERIOD")
        value = row.get("OBS_VALUE")
        if not date or not value:
            raise RuntimeError("Colonnes TIME_PERIOD / OBS_VALUE absentes")
        print(f"{date} : 1 EUR = {value} USD")
    print("Note : la date ne prouve pas l'heure de publication.")


if __name__ == "__main__":
    main()
