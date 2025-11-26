import os
from PIL import Image
import argparse

# SZÍNEK (ékezetek nélül használandó)
filterek = {
    "none": (0, 0, 0),
    "piros": (255, 0, 0),
    "zold": (0, 255, 0),
    "kek": (0, 0, 255),
    "sarga": (255, 255, 0),
    "lila": (128, 0, 128),
    "narancs": (255, 165, 0),
    "ruzsas": (255, 20, 147),
    "ciankek": (0, 255, 255),
    "malyva": (180, 70, 140),
    "feher": (255, 255, 255),
    "fekete": (50, 50, 50),
    "szurke": (128, 128, 128),
    "barna": (139, 69, 19),
    "vilagoskek": (135, 206, 235),
    "sotetkek": (0, 0, 139),
    "menta": (152, 255, 152),
    "arany": (255, 215, 0),
    "ezust": (192, 192, 192),
    "lime": (0, 255, 50)
}

# PARANCSSORI ARGUMENTUMOK
parser = argparse.ArgumentParser(description="Képszerkesztő")

parser.add_argument("--kep", type=str, required=True,
                    help="A szerkesztendő kép fájlneve a kepek mappából")

parser.add_argument("--meret", type=int, default=1000,
                    help="Új szélesség pixelben")

parser.add_argument("--forgatas", type=int, default=0,
                    help="Forgatás szöge (0–360)")

parser.add_argument("--szin", type=str, default="none",
                    choices=list(filterek.keys()),
                    help="Filter színe")

args = parser.parse_args()

# MAPPÁK ÉS FÁJLTÍPUSOK
bemeneti_mappa = "kepek"
kimeneti_mappa = "szerkesztett_kepek"

elfogadott_formatum = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

#KÉP BEOLVASÁSA
kep_helye = os.path.join(bemeneti_mappa, args.kep)

# HIBÁK KEZELÉSE
if not os.path.exists(kep_helye):
    print(f"Hiba: A '{args.kep}' fájl nem található a kepek mappában!")
    exit()

if not args.kep.lower().endswith(elfogadott_formatum):
    print("Hiba: A megadott fájl nem támogatott képformátum.")
    exit()

# KÉP MEGNYITÁSA
kep = Image.open(kep_helye)

# MÉRET
w, h = kep.size
scale = args.meret / w
kep = kep.resize((args.meret, int(h * scale)))

# FORGATÁS
if args.forgatas != 0:
    kep = kep.rotate(args.forgatas, expand=True)

# FILTER ALKALMAZÁSA
if args.szin != "none":
    r, g, b = filterek[args.szin]
    overlay = Image.new("RGB", kep.size, (r, g, b)) 
    kep = Image.blend(kep, overlay, alpha=0.35)

# MENTÉS
nev, kiterj = os.path.splitext(args.kep)
alap_nev = f"{nev}_szerkesztett"

verzio = 1
uj_nev = f"{alap_nev}_v{verzio}{kiterj}"
mentes_helye = os.path.join(kimeneti_mappa, uj_nev)

while os.path.exists(mentes_helye):
    verzio += 1
    uj_nev = f"{alap_nev}_v{verzio}{kiterj}"
    mentes_helye = os.path.join(kimeneti_mappa, uj_nev)

kep.save(mentes_helye)

print(f"Kész! Mentve ide: {mentes_helye}")