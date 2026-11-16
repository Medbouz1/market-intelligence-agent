"""Deterministic validation and portfolio exposure. No network, no orders."""
from __future__ import annotations
from datetime import datetime
from urllib.parse import urlparse

MARKETS = (
    "S&P 500", "Nasdaq 100", "CAC 40", "Euro Stoxx 50",
    "UST 2Y", "UST 10Y", "Bund 2Y", "Bund 10Y",
    "EUR/USD", "Gold", "Brent", "WTI",
)
STATES = {"close", "intraday", "fixing", "reference", "delayed", "unavailable"}
KINDS = {"fact", "interpretation", "hypothesis"}


def parse_time(value):
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError) as exc:
        raise ValueError("Horodatage ISO 8601 invalide : " + str(value)) from exc
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("Fuseau horaire absent : " + str(value))
    return dt


def validate(data):
    required = ("edition", "synthetic", "sources", "summary", "markets",
                "macro", "risks", "events", "portfolio")
    for key in required:
        if key not in data:
            raise ValueError("Champ manquant : " + key)
    if not isinstance(data["synthetic"], bool):
        raise ValueError("synthetic doit être un booléen")
    edition = data["edition"]
    cutoff = parse_time(edition["asof"])
    if edition.get("timezone") != "Europe/Paris":
        raise ValueError("Fuseau de référence Europe/Paris obligatoire")
    sources = {}
    for item in data["sources"]:
        sid, url = item["id"], item["url"]
        if sid in sources:
            raise ValueError("Source en double : " + sid)
        u = urlparse(url)
        if u.scheme != "https" or not u.netloc:
            raise ValueError("Source HTTPS obligatoire : " + sid)
        sources[sid] = item
    warnings = []
    seen = set()
    for item in data["markets"]:
        symbol = item["instrument"]
        if symbol in seen:
            raise ValueError("Instrument en double : " + symbol)
        seen.add(symbol)
        state = item.get("status")
        if state not in STATES:
            raise ValueError("Statut invalide : " + symbol)
        value = item.get("value")
        if value is None:
            if state != "unavailable" or item.get("change") is not None:
                raise ValueError("Valeur manquante mal marquée : " + symbol)
            continue
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError("Cotation non numérique : " + symbol)
        if state == "unavailable":
            raise ValueError("Valeur avec statut unavailable : " + symbol)
        if item.get("source_id") not in sources or not item.get("asof"):
            raise ValueError("Source ou heure absente : " + symbol)
        observed = parse_time(item["asof"])
        if observed > cutoff:
            raise ValueError("Observation après cutoff : " + symbol)
        hours = (cutoff - observed).total_seconds() / 3600
        if hours > 72:
            warnings.append(symbol + " : cotation ancienne (" + str(round(hours)) + " h)")
        if state == "delayed" and item.get("delay_minutes") is None:
            warnings.append(symbol + " : délai inconnu")
    if set(MARKETS) - seen:
        raise ValueError("Instruments non renseignés : " + str(sorted(set(MARKETS) - seen)))
    for field in ("summary", "macro"):
        for item in data[field]:
            if item.get("kind") not in KINDS:
                raise ValueError("Nature fact/interpretation/hypothesis invalide")
            ids = item.get("source_ids", [])
            if any(ref not in sources for ref in ids):
                raise ValueError("Affirmation avec source inconnue")
            if item["kind"] != "hypothesis" and not ids:
                raise ValueError("Fait ou interprétation sans source")
            if not item.get("text"):
                raise ValueError("Affirmation vide")
    if len(data["risks"]) != 3 or len(data["events"]) != 3:
        raise ValueError("Trois risques et trois événements obligatoires")
    for item in data["events"]:
        ids = item.get("source_ids", [])
        if any(ref not in sources for ref in ids):
            raise ValueError("Événement avec source inconnue")
        if item.get("verified"):
            if not ids or not item.get("asof"):
                raise ValueError("Événement vérifié sans source/heure")
            parse_time(item["asof"])
    p = data["portfolio"]
    if p["status"] == "inaccessible":
        if p.get("positions") or p.get("nav") is not None:
            raise ValueError("IBKR inaccessible : NAV/positions interdites")
    elif p["status"] == "verified":
        if not p.get("nav") or float(p["nav"]) <= 0 or not p.get("asof"):
            raise ValueError("Portefeuille vérifié : NAV/heure obligatoires")
        if parse_time(p["asof"]) > cutoff:
            raise ValueError("IBKR observé après cutoff")
        for item in p.get("positions", []):
            if any(k not in item for k in ("ticker", "quantity", "market_value", "currency")):
                raise ValueError("Position incomplète")
    else:
        raise ValueError("Statut IBKR inconnu")
    return warnings


def portfolio_analysis(p):
    if p["status"] == "inaccessible":
        return {"status": "inaccessible",
                "message": "Portefeuille IBKR non accessible pour cette édition"}
    nav = float(p["nav"])
    positions, sectors, currencies = [], {}, {}
    total = 0
    for item in p.get("positions", []):
        mv = float(item["market_value"])
        total += mv
        enriched = dict(item)
        enriched["weight_pct"] = round(100 * mv / nav, 4)
        positions.append(enriched)
        sector = item.get("sector") or "Non ventilé / ETF"
        sectors[sector] = sectors.get(sector, 0) + mv
        currency = item["currency"]
        currencies[currency] = currencies.get(currency, 0) + mv
    cash = float(p.get("cash", 0))
    difference = round(nav - cash - total, 2)
    warnings = []
    if abs(difference) > max(1.0, nav / 1000):
        warnings.append("Ecart NAV / positions + cash : " + str(difference))
    if p.get("realtime") is None:
        warnings.append("IBKR : temps réel ou différé non déterminé")
    return {
        "status": "verified", "nav": nav, "cash": cash, "asof": p["asof"],
        "base_currency": p.get("base_currency", "USD"),
        "realtime": p.get("realtime"), "positions": positions,
        "cash_weight_pct": round(100 * cash / nav, 4),
        "sector_weights_pct": {k: round(v * 100 / nav, 4) for k,v in sectors.items()},
        "currency_weights_pct": {k: round(v * 100 / nav, 4) for k,v in currencies.items()},
        "reconciliation_difference": difference, "warnings": warnings,
    }


def build_report(data):
    warnings = validate(data)
    p = portfolio_analysis(data["portfolio"])
    return {
        "schema_version": "0.1",
        "edition": data["edition"], "synthetic": data["synthetic"],
        "sources": data["sources"], "summary": data["summary"],
        "markets": data["markets"], "macro": data["macro"],
        "risks": data["risks"], "events": data["events"],
        "portfolio": p, "quality_warnings": warnings + p.get("warnings", []),
        "research_only": True, "orders_enabled": False,
    }
