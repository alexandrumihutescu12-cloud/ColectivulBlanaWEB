#!/usr/bin/env python3
"""
Adaugă evenimentul "Cine salvează pe cine?" (4 decembrie 2026, ID 1204)
în proiecte.html.

Utilizare:
    python adauga_eveniment_4_decembrie.py                 # folosește proiecte.html
    python adauga_eveniment_4_decembrie.py cale/proiecte.html

- Face backup (proiecte.html.bak) înainte de orice modificare.
- Verifică fiecare punct de inserare; dacă ceva nu e găsit exact o dată,
  se oprește fără să scrie nimic.
- Poate fi rulat de mai multe ori: dacă evenimentul există deja, nu face nimic.
"""
import re
import shutil
import sys

EVENT_ID = 1204

# ---------------------------------------------------------------- conținut nou

CARD_HTML = """<div style="display: flex; align-items: flex-start; background-color: #fffaf5; padding: 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #f7e6d7;">
<div style="background-color: #ffece0; color: #d97736; min-width: 50px; height: 50px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-right: 15px;"><i class="fas fa-hand-holding-heart"></i></div>
<div style="flex: 1;">
<h4 style="margin:0 0 5px 0; color:#1A330E; font-size:16px;">🐾 Cine salvează pe cine?</h4>
<p style="margin:0; font-size:14px; color:#4A5A43; line-height:1.5; margin-bottom:8px;">Vineri, <strong>4 decembrie</strong>, între <strong>18:00 și 20:00</strong>.<br> „Am pornit să salvăm animale. La final am descoperit că ele ne-au schimbat pe noi.” Toată lumea spune că animalele au nevoie de oameni. Noi credem că și oamenii au nevoie de animale. De multe ori, un câine nu îți schimbă programul, îți schimbă felul în care privești viața. O pisică nu îți ocupă fotoliul, îți ocupă golurile din suflet. Am întâlnit oameni care au ieșit din depresie pentru că un animal îi obliga să se ridice dimineața din pat, copii care au învățat răbdarea îngrijind un animal, persoane în vârstă care și-au recăpătat bucuria de a trăi pentru că aveau din nou pe cineva care îi aștepta acasă și voluntari care au venit să salveze animale și au plecat schimbându-și complet modul de a privi oamenii. Atelierul este despre toate aceste transformări și urmărește conștientizarea impactului pozitiv pe care relația dintre om și animal îl poate avea asupra sănătății emoționale, stării de bine și relațiilor din comunitate.</p>
<div style="display:flex; gap:15px; flex-wrap:wrap;">
<a href="https://maps.app.goo.gl/6kunAE5zqKrcaF7r6" target="_blank" style="font-size:13px; color:#D97736; font-weight:bold; text-decoration:none; display:flex; align-items:center;"><i class="fas fa-map-marker-alt" style="margin-right:5px;"></i> Vezi locația</a>
<a href="#" onclick="openRegistrationModal(1204); return false;" style="font-size:13px; color:#D97736; font-weight:bold; text-decoration:none; display:flex; align-items:center;"><i class="fas fa-pen" style="margin-right:5px;"></i> Înscrie-te</a>
</div>
</div>
</div>

"""

CALENDAR_LI = (
    '<li>\n'
    '                            <span class="event-date">4</span>\n'
    '                            <span class="event-label">Cine salvează pe cine?</span>\n'
    '                            <button class="btn-info" onclick="openEventInfoModal(1204)" aria-label="Detalii eveniment"><i class="fas fa-info"></i></button>\n'
    '                            <button class="btn-inscrie" onclick="openRegistrationModal(1204)">Înscrie-te</button>\n'
    '                        </li>'
)

EVENT_INFO_ENTRY = """    1204: {
        title: "Cine salvează pe cine?",
        data: "Vineri, 4 decembrie 2026",
        ora: '18:00 – 20:00',
        locatie: 'Centrul de zi pentru Copii cu Dizabilități Podul Lung',
        locatieUrl: EVENT_LOCATIE_URL_2,
        paragraphs: [
            "„Am pornit să salvăm animale. La final am descoperit că ele ne-au schimbat pe noi.”",
            "Toată lumea spune că animalele au nevoie de oameni. Noi credem că și oamenii au nevoie de animale. De multe ori, un câine nu îți schimbă programul. Îți schimbă felul în care privești viața. O pisică nu îți ocupă fotoliul. Îți ocupă golurile din suflet.",
            "Am întâlnit oameni care au ieșit din depresie pentru că un animal îi obliga să se ridice dimineața din pat. Am întâlnit copii care au învățat răbdarea îngrijind un animal. Am întâlnit persoane în vârstă care și-au recăpătat bucuria de a trăi pentru că aveau din nou pe cineva care îi aștepta acasă. Și am întâlnit voluntari care au venit să salveze animale și au plecat schimbându-și complet modul de a privi oamenii.",
            "Atelierul este despre toate aceste transformări. Scopul lui este conștientizarea impactului pozitiv pe care relația dintre om și animal îl poate avea asupra sănătății emoționale, stării de bine și relațiilor din comunitate."
        ]
    }"""

# ------------------------------------------------------------------ utilitare

def replace_once(text, old, new, label):
    """Înlocuiește `old` cu `new`, cu condiția ca `old` să apară exact o dată."""
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"[{label}] ancora a fost găsită de {n} ori (se aștepta 1).")
    return text.replace(old, new)


def apply_changes(t):
    # 1. Cardul evenimentului, înaintea blocului cu logo-urile de finanțare
    anchor = ('<div style="display:flex; align-items:center; justify-content:space-between; '
              'gap:14px; margin-top:20px; padding-top:16px; border-top:1px solid #eaddc7;">')
    t = replace_once(t, anchor, CARD_HTML + anchor, "1. card eveniment")

    # 2a. Calendar: titlul celulei din 4 decembrie
    t = replace_once(
        t,
        '<div class="day-cell event" data-date="2026-12-04" title="Detalii în curând">4</div>',
        '<div class="day-cell event" data-date="2026-12-04" title="Cine salvează pe cine?">4</div>',
        "2a. celulă calendar",
    )

    # 2b. Calendar: lista de sub luna decembrie
    t = replace_once(
        t,
        '<li><span class="event-date">4</span> <span class="event-label">Detalii în curând</span></li>',
        CALENDAR_LI,
        "2b. listă calendar",
    )

    # 3a. Modalul de înscriere generat din JS: lista de ID-uri
    t = replace_once(
        t,
        "[1107, 1170, 1111, 1124, 1126].forEach(function (id) {",
        "[1107, 1170, 1111, 1124, 1126, 1204].forEach(function (id) {",
        "3a. generare modal (ID-uri)",
    )

    # 3b. Modalul de înscriere generat din JS: titlul
    t = replace_once(
        t,
        '1126: "Atelier interactiv cu animale: Familia nu se cumpără, se construiește"',
        '1126: "Atelier interactiv cu animale: Familia nu se cumpără, se construiește",\n'
        '        1204: "Cine salvează pe cine?"',
        "3b. generare modal (titlu)",
    )

    # 4. Închiderea cu Escape
    t = replace_once(
        t,
        "[25, 26, 29, 3, 5, 10, 19, 24, 28, 31, 1107, 1170, 1111, 1124, 1126].forEach(closeRegistrationModal);",
        "[25, 26, 29, 3, 5, 10, 19, 24, 28, 31, 1107, 1170, 1111, 1124, 1126, 1204].forEach(closeRegistrationModal);",
        "4. Escape",
    )

    # 5a. EVENT_INFO: după intrarea 1126 (ultima din obiect)
    pattern = re.compile(r"\}(\s*)\};(\s*)function openEventInfoModal\(id\)")
    matches = pattern.findall(t)
    if len(matches) != 1:
        raise RuntimeError(f"[5a. EVENT_INFO] sfârșitul obiectului găsit de {len(matches)} ori (se aștepta 1).")
    t = pattern.sub(
        lambda m: "},\n" + EVENT_INFO_ENTRY + "\n};\n\nfunction openEventInfoModal(id)",
        t,
    )

    # 5b. REGISTRATION_EVENTS
    t = replace_once(
        t,
        '1126: "26 Noiembrie - Atelier interactiv cu animale (Familia nu se cumpără, se construiește)"',
        '1126: "26 Noiembrie - Atelier interactiv cu animale (Familia nu se cumpără, se construiește)",\n'
        '    1204: "4 Decembrie - Cine salvează pe cine?"',
        "5b. REGISTRATION_EVENTS",
    )

    # 6. Listenerul de submit
    t = replace_once(
        t,
        "[25, 26, 29, 3, 5, 10, 19, 24, 28, 31, 1107, 1170, 1111, 1124, 1126].forEach(function (id) {",
        "[25, 26, 29, 3, 5, 10, 19, 24, 28, 31, 1107, 1170, 1111, 1124, 1126, 1204].forEach(function (id) {",
        "6. listener submit",
    )
    return t


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "proiecte.html"

    try:
        with open(path, "r", encoding="utf-8", newline="") as f:
            raw = f.read()
    except FileNotFoundError:
        sys.exit(f"Fișierul '{path}' nu există. Dă calea corectă ca argument.")

    # Păstrăm tipul de sfârșit de linie (CRLF / LF)
    crlf = "\r\n" in raw
    text = raw.replace("\r\n", "\n")

    if f"openRegistrationModal({EVENT_ID})" in text:
        print("Evenimentul 1204 există deja în fișier. Nu am modificat nimic.")
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

    print(f"Gata! Evenimentul „Cine salvează pe cine?” a fost adăugat în {path}")
    print(f"Backup salvat în {path}.bak")
    print("Nu uita: dacă ai o listă de evenimente în Google Apps Script, adaugă și")
    print('  "4 Decembrie - Cine salvează pe cine?"  (text identic).')


if __name__ == "__main__":
    main()