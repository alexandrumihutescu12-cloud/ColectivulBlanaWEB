#!/usr/bin/env python3
"""
Utilizare:  python patch_7_noiembrie.py proiecte_nou.html
Rezultat:   proiecte_final.html  (fișierul de intrare rămâne neatins)

Pe 7 noiembrie:
  14:00-15:00  Comunitatea care spune „DA”   (id 1170, nou)
  15:00-16:00  Copiii nu fac ce le spunem    (id 1107, ora se schimbă)
Dacă o ancoră lipsește, scriptul se oprește fără să scrie nimic.
"""
import re, sys

src = sys.argv[1] if len(sys.argv) > 1 else "proiecte_nou.html"
s = open(src, encoding="utf-8", newline="").read().replace("\r\n", "\n")

def must(c, m):
    if not c:
        sys.exit("EROARE: nu am găsit " + m + ". Nu s-a scris nimic.")

BOX = '<div style="display: flex; align-items: flex-start; background-color: #fffaf5; padding: 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #f7e6d7;">'
ICO = '<div style="background-color: #ffece0; color: #d97736; min-width: 50px; height: 50px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-right: 15px;"><i class="fas %s"></i></div>'
H4 = '<h4 style="margin:0 0 5px 0; color:#1A330E; font-size:16px;">🐾 %s</h4>'
P = '<p style="margin:0; font-size:14px; color:#4A5A43; line-height:1.5; margin-bottom:8px;">%s</p>'
LINK = '<a href="%s" target="_blank" style="font-size:13px; color:#D97736; font-weight:bold; text-decoration:none; display:flex; align-items:center;"><i class="fas fa-map-marker-alt" style="margin-right:5px;"></i> Vezi locația</a>'
REG = '<a href="#" onclick="openRegistrationModal(%d); return false;" style="font-size:13px; color:#D97736; font-weight:bold; text-decoration:none; display:flex; align-items:center;"><i class="fas fa-pen" style="margin-right:5px;"></i> Înscrie-te</a>'
LOC = "https://maps.app.goo.gl/6kunAE5zqKrcaF7r6"
DA_ID = 1170
DA_TITLU = "Comunitatea care spune „DA”"

DA_CARD_TXT = ("Sâmbătă, <strong>7 noiembrie</strong>, între <strong>14:00 și 15:00</strong>.<br> "
  "De multe ori primim mesaje care încep la fel: „Am găsit un cățel. Veniți să îl luați.” sau „Este o pisică cu pui în curtea mea. "
  "Faceți ceva, unde pot să o aduc?” Întrebarea pe care ne-o punem de fiecare dată este alta: „Dar tu ce poți face? Hai să te ajutăm să ajuți și tu!” "
  "Nu pentru că vrem să pasăm responsabilitatea, ci pentru că nicio asociație nu poate fi în toate locurile în același timp. "
  "Problema abandonului nu poate fi rezolvată doar de ONG-uri, ci doar de comunități în care fiecare om își asumă o parte din responsabilitate. "
  "Atelierul vorbește despre solidaritate și despre faptul că nu trebuie să fii salvator, trebuie doar să fii prezent. "
  "La final, participanții vor înțelege că fiecare poate contribui la binele comunității, vor descoperi forme de voluntariat accesibile oricui, "
  "vor vedea cât contează colaborarea dintre cetățeni, ONG-uri și instituții și vor pleca cu un plan concret prin care pot ajuta fără a fi voluntari permanenți.")

da_card = ("\n" + BOX + "\n" + ICO % "fa-comments" + "\n<div style=\"flex: 1;\">\n" + H4 % DA_TITLU + "\n" + P % DA_CARD_TXT +
           '\n<div style="display:flex; gap:15px; flex-wrap:wrap;">\n' + LINK % LOC + "\n" + REG % DA_ID +
           "\n</div>\n</div>\n</div>\n")

# ---- 1. card: Copiii -> 15:00, DA înainte de el ----
print("Fișier citit:", src, "| apariții '1107':", s.count("1107"), "| apariții 'Copiii nu fac':", len(re.findall(r"copiii nu fac", s, re.I)))
if s.count("1107") == 0:
    sys.exit("EROARE: fișierul '" + src + "' nu conține evenimentele din noiembrie (ID 1107). "
             "Rulează scriptul pe proiecte_nou.html, generat de aplica_modificari.py, nu pe proiecte.html original.")

BOXP = BOX[:70]
m = re.search(r'<h4[^>]*>[^<]*copiii nu fac', s, re.I)
must(m, "titlul cardului 'Copiii nu fac ce le spunem' (în <h4>)")
st = s.rfind(BOXP, 0, m.start())
must(st >= 0, "începutul cardului 'Copiii nu fac ce le spunem'")
en = s.find(BOXP, m.start())
if en < 0:
    en = s.find("</div>\n</div>\n</div>\n", m.start()) + len("</div>\n</div>\n</div>\n")
bloc = s[st:en]
must("14:00 și 16:00" in bloc, "ora '14:00 și 16:00' în cardul 'Copiii nu fac ce le spunem'")
bloc = bloc.replace("14:00 și 16:00", "15:00 și 16:00", 1)
s = s[:st] + da_card.lstrip("\n") + "\n" + bloc + s[en:]

# ---- 2. calendar: titlul celulei + elementul din listă ----
s, n = re.subn(r'data-date="2026-11-07" title="[^"]*"',
               'data-date="2026-11-07" title="Comunitatea care spune „DA” și Atelier interactiv cu animale"', s, count=1)
must(n == 1, "celula 7 noiembrie din calendar")
k = s.find('data-month="2026-11"')
j = s.find('<li><span class="event-date">7</span>', k)
must(k > 0 and j > k, "elementul 7 din lista de noiembrie")
li = ('<li><span class="event-date">7</span> <span class="event-label">%s</span>'
      '<button class="btn-info" onclick="openEventInfoModal(%d)" aria-label="Detalii eveniment"><i class="fas fa-info"></i></button>'
      '<button class="btn-inscrie" onclick="openRegistrationModal(%d)">Înscrie-te</button></li>\n') % (DA_TITLU, DA_ID, DA_ID)
s = s[:j] + li + s[j:]

# ---- 3. EVENT_INFO: ora pentru 1107 + intrarea nouă ----
s, n = re.subn(r"(\n    1107: \{.*?ora: ')[^']*(')", lambda m: m.group(1) + "15:00 – 16:00" + m.group(2), s, count=1, flags=re.S)
must(n == 1, "EVENT_INFO[1107].ora")

info = '''
    1170: {
        title: "Comunitatea care spune „DA”",
        data: "Sâmbătă, 7 noiembrie 2026",
        ora: '14:00 – 15:00',
        locatie: 'Centrul de zi pentru Copii cu Dizabilități Podul Lung',
        locatieUrl: EVENT_LOCATIE_URL_2,
        paragraphs: [
            "De multe ori primim mesaje care încep la fel: „Am găsit un cățel. Veniți să îl luați.” sau „Este o pisică cu pui în curtea mea. Faceți ceva, unde pot să o aduc?” Întrebarea pe care ne-o punem de fiecare dată este alta: „Dar tu ce poți face? Hai să te ajutăm să ajuți și tu!”",
            "Nu pentru că vrem să pasăm responsabilitatea, ci pentru că nicio asociație nu poate fi în toate locurile în același timp. Problema abandonului nu poate fi rezolvată doar de ONG-uri, ci doar de comunități în care fiecare om își asumă o parte din responsabilitate. Atelierul vorbește despre solidaritate și despre faptul că nu trebuie să fii salvator, trebuie doar să fii prezent.",
            "La final, participanții vor înțelege că fiecare poate contribui la binele comunității, vor descoperi forme de voluntariat accesibile oricui, vor vedea cât contează colaborarea dintre cetățeni, ONG-uri și instituții și vor pleca cu un plan concret prin care pot ajuta fără a fi voluntari permanenți."
        ]
    },'''
must(s.count("\n    1107: {") == 1, "intrarea 1107 din EVENT_INFO")
s = s.replace("\n    1107: {", info + "\n    1107: {", 1)

# ---- 4. REGISTRATION_EVENTS ----
r = re.search(r'\n    1107: "7 Noiembrie', s)
must(r, "REGISTRATION_EVENTS[1107]")
s = s[:r.start()] + '\n    1170: "7 Noiembrie - Comunitatea care spune DA",' + s[r.start():]

# ---- 5. generatorul de modale + listele de ID-uri ----
must(s.count("1107, 1111, 1124, 1126]") == 3, "cele 3 liste de ID-uri (2 liste + generatorul)")
s = s.replace("1107, 1111, 1124, 1126]", "1107, 1170, 1111, 1124, 1126]")
s, n = re.subn(r'(\n\s+)(1107: "Atelier interactiv cu animale: Copiii nu fac ce le spunem",)',
               lambda m: m.group(1) + '1170: "Comunitatea care spune „DA”",' + m.group(1) + m.group(2), s, count=1)
must(n == 1, "titlul 1107 din generatorul de modale")

out = "proiecte_final.html"
open(out, "w", encoding="utf-8", newline="\n").write(s)
print("Gata:", out)