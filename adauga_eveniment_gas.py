#!/usr/bin/env python3
"""
Adaugă evenimentul "4 Decembrie - Cine salvează pe cine?" în scriptul Google Apps Script.

Utilizare:
    1. Salvează codul din Apps Script într-un fișier, ex. Code.gs
    2. python adauga_eveniment_gas.py Code.gs
    3. Copiază conținutul fișierului înapoi în editorul Apps Script.
"""
import re
import shutil
import sys

CHEIE = "4 Decembrie - Cine salvează pe cine?"
TAB = "4 Decembrie"

DETALII = """,
  '%s': {
    titlu: 'Cine salvează pe cine?',
    data: 'Vineri, 4 decembrie 2026',
    ora: '18:00 – 20:00',
    locatie: LOCATIE_PODUL_LUNG
  }
};""" % CHEIE


def replace_once(text, old, new, label):
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"[{label}] ancora a fost găsită de {n} ori (se aștepta 1).")
    return text.replace(old, new)


def apply_changes(t):
    # 1. EVENIMENTE_DETALII: ultima intrare din obiect se termină cu "}\n};"
    pattern = re.compile(r"(locatie: LOCATIE_PODUL_LUNG\s*\})\s*\};")
    if len(pattern.findall(t)) != 1:
        raise RuntimeError("[1. EVENIMENTE_DETALII] sfârșitul obiectului nu a fost găsit exact o dată.")
    t = pattern.sub(lambda m: m.group(1) + DETALII, t)

    # 2. EVENIMENTE_SHEET
    t = replace_once(
        t,
        "'26 Noiembrie - Atelier interactiv cu animale (Familia nu se cumpără, se construiește)': '26 Noiembrie'",
        "'26 Noiembrie - Atelier interactiv cu animale (Familia nu se cumpără, se construiește)': '26 Noiembrie',\n"
        "  '%s': '%s'" % (CHEIE, TAB),
        "2. EVENIMENTE_SHEET",
    )

    # 3. Comentariile din antet (nu sunt critice)
    if t.count(' *      "26 Noiembrie"') == 1:
        t = t.replace(' *      "26 Noiembrie"', ' *      "26 Noiembrie"\n *      "%s"' % TAB)
    if t.count("Creează 15 tab-uri") == 1:
        t = t.replace("Creează 15 tab-uri", "Creează 16 tab-uri")
    return t


def main():
    if len(sys.argv) < 2:
        sys.exit("Utilizare: python adauga_eveniment_gas.py Code.gs")
    path = sys.argv[1]

    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            raw = f.read()
    except FileNotFoundError:
        sys.exit(f"Fișierul '{path}' nu există.")

    crlf = "\r\n" in raw
    text = raw.replace("\r\n", "\n")

    if CHEIE in text:
        print("Evenimentul există deja în script. Nu am modificat nimic.")
        return

    try:
        new_text = apply_changes(text)
    except RuntimeError as e:
        sys.exit(f"EROARE: {e}\nNu am scris nimic în fișier.")

    shutil.copyfile(path, path + ".bak")
    if crlf:
        new_text = new_text.replace("\n", "\r\n")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(new_text)

    print(f"Gata! Backup: {path}.bak")
    print(f'Creează în Google Sheet un tab numit exact: {TAB}')
    print("Apoi fă redeploy: Deploy > Manage deployments > Edit > New version.")


if __name__ == "__main__":
    main()