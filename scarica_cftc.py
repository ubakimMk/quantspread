#!/usr/bin/env python3
"""
Scarica gli ultimi report CFTC COT (Disaggregated, Futures Only)
e salva cot.json con le posizioni nette.

Uso:   python3 scarica_cftc.py
Serve: solo Python 3.8+ (nessuna libreria extra).
Dati:  pubblici e gratuiti, aggiornati ogni venerdì.
"""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://publicreporting.cftc.gov/resource/72hh-3qpy.json"

# Codice contratto CFTC -> nome nell'app
MERCATI = {
    "067651": "WTI Crude Oil",
    "088691": "Gold",
    "002602": "Corn",
    "001602": "Wheat (CBOT)",
    "005602": "Soybeans",
    "080732": "Sugar #11",
    "054642": "Lean Hogs",
}


def scarica(codice):
    params = urllib.parse.urlencode({
        "cftc_contract_market_code": codice,
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": 2,  # ultimo report + precedente (per la variazione)
    })
    req = urllib.request.Request(
        f"{API}?{params}", headers={"User-Agent": "quantspread/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def numero(riga, campo):
    try:
        return int(float(riga[campo]))
    except (KeyError, TypeError, ValueError):
        return None


def netto(riga, lungo, corto):
    a, b = numero(riga, lungo), numero(riga, corto)
    return None if a is None or b is None else a - b


def main():
    risultato = {
        "aggiornato": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fonte": "CFTC Disaggregated Futures Only",
        "mercati": {},
    }
    for codice, nome in MERCATI.items():
        try:
            righe = scarica(codice)
            if not righe:
                print(f"[vuoto]  {nome}: nessun dato")
                continue
            ora = righe[0]
            prima = righe[1] if len(righe) > 1 else None
            spec = netto(ora, "m_money_positions_long_all", "m_money_positions_short_all")
            comm = netto(ora, "prod_merc_positions_long", "prod_merc_positions_short")
            spec_prima = (
                netto(prima, "m_money_positions_long_all", "m_money_positions_short_all")
                if prima else None
            )
            risultato["mercati"][nome] = {
                "data_report": ora.get("report_date_as_yyyy_mm_dd", "")[:10],
                "open_interest": numero(ora, "open_interest_all"),
                "speculatori_netto": spec,
                "speculatori_variazione": (
                    spec - spec_prima if spec is not None and spec_prima is not None else None
                ),
                "commerciali_netto": comm,
            }
            print(f"[ok]     {nome}: speculatori netto {spec}, commerciali netto {comm}")
        except Exception as e:  # rete o formato cambiato
            print(f"[errore] {nome}: {e}")

    if not risultato["mercati"]:
        raise SystemExit("Nessun dato scaricato: cot.json non modificato")
    with open("cot.json", "w", encoding="utf-8") as f:
        json.dump(risultato, f, ensure_ascii=False, indent=2)
    print("\nSalvato: cot.json")


if __name__ == "__main__":
    main()
