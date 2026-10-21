#!/usr/bin/env python3
"""
Utilizare:  python aplica_modificari.py proiecte.html
Rezultat:   proiecte_nou.html  (originalul rămâne neatins)

Face:
 - scoate evenimentul "Comunitatea care spune DA" (23 octombrie) peste tot
 - adaugă evenimentele din noiembrie (card, calendar, info, înscriere)
Dacă un punct de ancorare nu e găsit, scriptul se oprește cu eroare și nu scrie nimic.
"""
import re, sys

src = sys.argv[1] if len(sys.argv) > 1 else "proiecte.html"
s = open(src, encoding="utf-8", newline="").read().replace("\r\n", "\n")
s0 = s

print("aplica_modificari.py - versiunea 3")

def must(cond, msg):
    if not cond:
        sys.exit("EROARE: nu am găsit " + msg + ". Nu s-a modificat nimic.")

def soft(cond, msg):
    """Pentru ștergerea evenimentului din 23 oct: dacă lipsește deja, doar avertizează."""
    if not cond:
        print("ATENȚIE: nu am găsit " + msg + " (sar peste, poate fiind deja șters).")
    return cond

# ---------- date evenimente noi ----------
LOC = "https://maps.app.goo.gl/6kunAE5zqKrcaF7r6"
LOC_NAME = "Centrul de zi pentru Copii cu Dizabilități Podul Lung"
EV = [  # id, icon, titlu, zi_sapt, zi, ora_start, ora_end, placeholder
 (1107, "fa-child", "Atelier interactiv cu animale: COPIII NU FAC CE LE SPUNEM. FAC CE NE VĂD PE NOI FĂCÂND.",
  "Sâmbătă", "7", "14:00", "16:00", "Aici_Pui_Descrierea_Pentru_Atelier_Interactiv_Cu_Animale_COPIII_NU_FAC_CE_LE_SPUNEM"),
 (1111, "fa-stethoscope", "Curs educativ veterinar: De la abandon la responsabilitate",
  "Miercuri", "11", "18:00", "20:00", "Aici_Pui_Descrierea_Pentru_Curs_Educativ_Veterinar_11_Noiembrie"),
 (1124, "fa-stethoscope", "Curs educativ veterinar: De la abandon la responsabilitate",
  "Marți", "24", "18:00", "20:00", "Aici_Pui_Descrierea_Pentru_Curs_Educativ_Veterinar_24_Noiembrie"),
 (1126, "fa-house", "Atelier interactiv cu animale: Familia nu se cumpără, se construiește",
  "Joi", "26", "18:00", "20:00", "Aici_Pui_Descrierea_Pentru_Atelier_Interactiv_Cu_Animale_Familia_Nu_Se_Cumpara_Se_Construieste"),
]
NEW_IDS = [e[0] for e in EV]

BOX = '<div style="display: flex; align-items: flex-start; background-color: #fffaf5; padding: 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #f7e6d7;">'
ICO = '<div style="background-color: #ffece0; color: #d97736; min-width: 50px; height: 50px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-right: 15px;"><i class="fas %s"></i></div>'
H4 = '<h4 style="margin:0 0 5px 0; color:#1A330E; font-size:16px;">🐾 %s</h4>'
P = '<p style="margin:0; font-size:14px; color:#4A5A43; line-height:1.5; margin-bottom:8px;">%s</p>'
LINK = '<a href="%s" target="_blank" style="font-size:13px; color:#D97736; font-weight:bold; text-decoration:none; display:flex; align-items:center;"><i class="fas fa-map-marker-alt" style="margin-right:5px;"></i> Vezi locația</a>'
REG = '<a href="#" onclick="openRegistrationModal(%d); return false;" style="font-size:13px; color:#D97736; font-weight:bold; text-decoration:none; display:flex; align-items:center;"><i class="fas fa-pen" style="margin-right:5px;"></i> Înscrie-te</a>'

def card_block(e):
    id_, ic, t, zs, z, a, b, ph = e
    txt = '%s, <strong>%s noiembrie</strong>, între <strong>%s și %s</strong>.<br> %s' % (zs, z, a, b, ph)
    return ("\n" + BOX + "\n" + ICO % ic + "\n<div style=\"flex: 1;\">\n" + H4 % t + "\n" + P % txt +
            '\n<div style="display:flex; gap:15px; flex-wrap:wrap;">\n' + LINK % LOC + "\n" + REG % id_ +
            "\n</div>\n</div>\n</div>\n")

TARG = ("\n" + BOX + "\n" + ICO % "fa-paw" + "\n<div style=\"flex: 1;\">\n" + H4 % "Târg de Adopții" + "\n" +
        P % "Sâmbătă, <strong>21 noiembrie</strong>, între <strong>11:00 și 16:00</strong>. Locație externă. Detalii în curând." +
        "\n</div>\n</div>\n")

# ---------- 1. scoate 23 octombrie ----------
# card
i = s.find("openRegistrationModal(23); return false;")
if soft(i > 0, "blocul din card pentru 23 octombrie"):
    st = s.rfind(BOX[:80], 0, i)
    en = s.find(BOX[:80], i)
    if soft(st > 0 and en > i, "limitele blocului 23 octombrie"):
        s = s[:st] + s[en:]

# calendar: celula + elementul din listă
s, n = re.subn(r'<div class="day-cell event" data-date="2026-10-23"[^>]*>\s*23\s*</div>', '<div class="day-cell">23</div>', s, count=1)
soft(n == 1, "celula 23 din calendar")
s, n = re.subn(r'\n\s*<li>\s*<span class="event-date">\s*23\s*</span>.*?</li>', "", s, count=1, flags=re.S)
soft(n == 1, "elementul <li> 23 din calendar")

# modal înscriere
s, n = re.subn(r'<!-- 23 Octombrie\b.*?(?=<!-- 24 Octombrie\b)', "", s, count=1, flags=re.S)
soft(n == 1, "modalul de înscriere 23")

# JS: EVENT_INFO și REGISTRATION_EVENTS
s, n = re.subn(r'\n    23: \{.*?(?=\n    24: \{)', "", s, count=1, flags=re.S)
soft(n == 1, "EVENT_INFO[23]")
s, n = re.subn(r'\n    23: "23 Octombrie[^\n]*', "", s, count=1)
soft(n == 1, "REGISTRATION_EVENTS[23]")

# listele de ID-uri
OLD_IDS = "[25, 26, 29, 3, 5, 10, 19, 23, 24, 28, 31]"
must(s.count(OLD_IDS) == 2, "cele 2 liste de ID-uri")
s = s.replace(OLD_IDS, "[25, 26, 29, 3, 5, 10, 19, 24, 28, 31, " + ", ".join(map(str, NEW_IDS)) + "]")

# ---------- 2. card: evenimente noi ----------
anchor = '<div style="display:flex; align-items:center; justify-content:space-between; gap:14px; margin-top:20px; padding-top:16px;'
k = s.find(anchor)
must(k > 0, "rândul cu logo-uri de finanțare din cardul O Comunitate")
s = s[:k] + "\n<!-- ===== NOIEMBRIE ===== -->" + card_block(EV[0]) + card_block(EV[1]) + TARG + card_block(EV[2]) + card_block(EV[3]) + "\n" + s[k:]

# ---------- 3. calendar noiembrie ----------
for zi, t in [("07", "Atelier interactiv cu animale"), ("11", "Curs educativ veterinar"), ("21", "Târg de Adopții"),
              ("24", "Curs educativ veterinar"), ("26", "Atelier interactiv cu animale")]:
    s, n = re.subn(r'data-date="2026-11-%s" title="[^"]*"' % zi,
                   lambda m, zi=zi, t=t: 'data-date="2026-11-%s" title="%s"' % (zi, t), s, count=1)
    must(n == 1, "celula 2026-11-" + zi)

def li(e):
    return ('<li><span class="event-date">%s</span> <span class="event-label">%s</span>'
            '<button class="btn-info" onclick="openEventInfoModal(%d)" aria-label="Detalii eveniment"><i class="fas fa-info"></i></button>'
            '<button class="btn-inscrie" onclick="openRegistrationModal(%d)">Înscrie-te</button></li>\n' % (e[4], e[2], e[0], e[0]))

new_ul = ('<ul class="event-list">\n' + li(EV[0]) + li(EV[1]) +
          '<li><span class="event-date">21</span> <span class="event-label">Târg de Adopții (detalii în curând)</span></li>\n' +
          li(EV[2]) + li(EV[3]) + '</ul>')
s, n = re.subn(r'(data-month="2026-11".*?)<ul class="event-list">.*?</ul>', lambda m: m.group(1) + new_ul, s, count=1, flags=re.S)
must(n == 1, "lista de evenimente din noiembrie")

# ---------- 4. JS ----------
o = "const CAPACITATE_EVENIMENT = { 28: 10 };"
must(o in s, "CAPACITATE_EVENIMENT")
s = s.replace(o, "const CAPACITATE_EVENIMENT = { 28: 10, 1124: 10 };")

NOI_REG = (',\n    1107: "7 Noiembrie - Atelier interactiv cu animale (Copiii nu fac ce le spunem)",\n'
  '    1111: "11 Noiembrie - Curs educativ veterinar (De la abandon la responsabilitate)",\n'
  '    1124: "24 Noiembrie - Curs educativ veterinar (De la abandon la responsabilitate)",\n'
  '    1126: "26 Noiembrie - Atelier interactiv cu animale (Familia nu se cumpără, se construiește)"')
s, n = re.subn(r'(\n    31: "31 Octombrie[^\n]*?")(\s*\n\};)', lambda m: m.group(1) + NOI_REG + m.group(2), s, count=1)
must(n == 1, "ultima intrare din REGISTRATION_EVENTS")

info_js = ""
for e in EV:
    id_, ic, t, zs, z, a, b, ph = e
    info_js += (',\n    %d: {\n        title: "%s",\n        data: "%s, %s noiembrie 2026",\n        ora: \'%s – %s\',\n'
                '        locatie: \'%s\',\n        locatieUrl: EVENT_LOCATIE_URL_2,\n        paragraphs: [\n'
                '            "%s_Paragraful_1",\n            "%s_Paragraful_2"\n        ]\n    }') % (id_, t, zs, z, a, b, LOC_NAME, ph, ph)
s, n = re.subn(r'(\n\};\s*function openEventInfoModal)', lambda m: info_js + m.group(1), s, count=1)
must(n == 1, "sfârșitul obiectului EVENT_INFO")

GEN = r"""/* Modale de înscriere generate pentru noiembrie */
[1107, 1111, 1124, 1126].forEach(function (id) {
    var titluri = {
        1107: "Atelier interactiv cu animale: Copiii nu fac ce le spunem",
        1111: "Curs educativ veterinar: De la abandon la responsabilitate",
        1124: "Curs educativ veterinar: De la abandon la responsabilitate",
        1126: "Atelier interactiv cu animale: Familia nu se cumpără, se construiește"
    };
    var cap = id === 1124 ? 10 : 20;
    var el = document.createElement('div');
    el.className = 'registration-modal-overlay';
    el.id = 'registrationModalOverlay-' + id;
    el.setAttribute('onclick', 'closeRegistrationModalOnBackdrop(event, ' + id + ')');
    el.innerHTML =
    '<div class="registration-modal">' +
      '<button class="registration-modal-close" onclick="closeRegistrationModal(' + id + ')" aria-label="Închide"><i class="fas fa-xmark"></i></button>' +
      '<h2>Înscriere: <span id="registrationEventName-' + id + '">' + titluri[id] + '</span></h2>' +
      '<p class="registration-seats" id="registrationSeatsInfo-' + id + '">Capacitate: ' + cap + ' de locuri (tu + însoțitorii tăi ocupă câte un loc fiecare).</p>' +
      '<form id="registrationForm-' + id + '">' +
        '<div class="form-group"><label for="reg-nume-' + id + '">Nume</label><input type="text" id="reg-nume-' + id + '" required></div>' +
        '<div class="form-group"><label for="reg-prenume-' + id + '">Prenume</label><input type="text" id="reg-prenume-' + id + '" required></div>' +
        '<div class="form-group"><label for="reg-telefon-' + id + '">Număr de telefon</label><input type="tel" id="reg-telefon-' + id + '" required></div>' +
        '<div class="form-group"><label for="reg-email-' + id + '">Adresă de email</label><input type="email" id="reg-email-' + id + '" required></div>' +
        '<div class="form-group"><label for="reg-varsta-' + id + '">Vârstă</label><input type="number" id="reg-varsta-' + id + '" min="1" max="120" required></div>' +
        '<div class="form-group"><label>Însoțitori (opțional — doar numele)</label><div class="companions-list" id="companionsList-' + id + '"></div>' +
          '<button type="button" class="btn-add-companion" onclick="addCompanionField(' + id + ')"><i class="fas fa-plus"></i> Adaugă însoțitor</button></div>' +
        '<div class="hp-field" aria-hidden="true"><label for="reg-website-' + id + '">Nu completa acest câmp</label><input type="text" id="reg-website-' + id + '" name="website" tabindex="-1" autocomplete="off"></div>' +
        '<label class="form-checkbox"><input type="checkbox" id="reg-confirmare18-' + id + '" required> Confirm că am peste 18 ani.</label>' +
        '<label class="form-checkbox"><input type="checkbox" id="reg-consimtamant-' + id + '" required> Sunt de acord cu prelucrarea datelor mele personale (nume, prenume, telefon, email, vârstă) de către Colectivul Blană, în scop de sondaj în cadrul proiectului „O Comunitate". Semnarea listei de prezență la eveniment reprezintă confirmarea acestui acord.</label>' +
        '<button type="submit" class="btn-submit-inscriere" id="registrationSubmitBtn-' + id + '">Trimite înscrierea</button>' +
        '<div class="form-message" id="registrationMessage-' + id + '"></div>' +
        '<p class="form-support-note">Ai probleme la înscrierea online? Scrie-ne la <a href="mailto:colectivulblana@gmail.com">colectivulblana@gmail.com</a>.</p>' +
      '</form>' +
      '<div class="funding-footer">' +
        '<img src="Imagini/LogoDASMT.png" alt="Direcția de Asistență Socială a Municipiului Timișoara" class="funding-logo">' +
        '<p class="funding-text">Proiect finanțat prin programul „O Comunitate 2026" de Direcția de Asistență Socială a Municipiului Timișoara</p>' +
        '<img src="Imagini/logoOComunitate2026.png" alt="O Comunitate 2026" class="funding-logo">' +
      '</div>' +
    '</div>';
    document.body.appendChild(el);
});

"""
o = "const calendarMonths = ["
must(s.count(o) == 1, "const calendarMonths")
s = s.replace(o, GEN + o)

def echilibru(t):
    return len(re.findall(r'<div\b', t)) - len(re.findall(r'</div>', t))
print("Echilibru <div> înainte/după:", echilibru(s0), "/", echilibru(s), "(trebuie să fie egale)")
print("Blocuri <style>:", s0.count("<style>"), "/", s.count("<style>"),
      "| link style.css:", s0.count('href="style.css"'), "/", s.count('href="style.css"'))
if echilibru(s0) != echilibru(s):
    sys.exit("EROARE: structura HTML ar fi dezechilibrată. Nu s-a scris nimic. Trimite-mi mesajul.")

out = src.rsplit(".", 1)[0] + "_nou.html"
open(out, "w", encoding="utf-8", newline="\n").write(s)
print("Gata:", out)