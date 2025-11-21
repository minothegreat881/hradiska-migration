# 🚀 Rýchly štart - Lokálne stiahnutie hradiska.sk

## Čo toto spraví?
✅ Stiahne **celú webstránku** hradiska.sk k vám na počítač
✅ Vytvorí **offline kópiu** ktorá funguje bez internetu
✅ Umožní vám **lokálne spustiť** stránku v prehliadači
✅ **BEZ konverzie** - zachová pôvodný HTML/CSS/JS

---

## 📋 Čo potrebujete?
- **Python 3.8+** (skontrolujte: `python --version`)
- **Internetové pripojenie** (len na stiahnutie)
- **2GB miesta** na disku

---

## ⚡ Spustenie (3 jednoduché kroky)

### WINDOWS:
```batch
download_only.bat
```
Dvojklik na súbor a hotovo!

### LINUX/MAC:
```bash
python3 download_mirror.py
```

---

## ⏱️ Ako dlho to trvá?
- **30-60 minút** (závisí od veľkosti stránky)
- Uvidíte progress s počtom stiahnutých súborov
- Môžete to kedykoľvek zastaviť (Ctrl+C)

---

## 📁 Čo dostanete?

```
backup/
└── hradiska_mirror/
    ├── index.html          # Hlavná stránka
    ├── 2011/              # Články z 2011
    ├── 2012/              # Články z 2012
    ├── images/            # Všetky obrázky
    ├── css/               # Štýly
    └── js/                # JavaScript
```

**Kompletný mirror** presne ako na webe!

---

## 🌐 Spustenie lokálnej stránky

### Metóda 1: Automatický skript (najjednoduchšie)
```batch
start_local_server.bat
```

### Metóda 2: Python server (manuálne)
```bash
cd backup\hradiska_mirror
python -m http.server 8000
```

### Metóda 3: Node.js (ak máte nainštalovaný)
```bash
npx http-server backup/hradiska_mirror -p 8000
```

Potom otvorte prehliadač: **http://localhost:8000**

---

## ✅ Overenie

Po dokončení by ste mali vidieť:
```
✅ SŤAHOVANIE DOKONČENÉ!
📊 Štatistiky:
  • HTML stránok: 250
  • Obrázkov: 450
  • CSS súborov: 15
  • JS súborov: 20
  • CELKOM: 735 súborov
```

---

## 🎯 Často kladené otázky

### ❓ Bude to fungovať offline?
**Áno!** Všetky súbory sú lokálne, nepotrebujete internet.

### ❓ Budú fungovať všetky odkazy?
**Áno!** Skript automaticky opraví všetky cesty.

### ❓ Môžem to upravovať?
**Áno!** Sú to bežné HTML/CSS súbory, môžete ich editovať.

### ❓ Koľko miesta to zaberá?
Typicky **100-500 MB** v závislosti od počtu obrázkov.

### ❓ Čo ak sa sťahovanie preruší?
Môžete ho **spustiť znova** - preskočí už stiahnuté súbory.

### ❓ Bude mať moderný dizajn?
**Nie** - toto je presná kópia originálnej stránky.
Ak chcete modernú verziu, použite `run_migration.bat`.

---

## 🔧 Riešenie problémov

### Python nie je nájdený
```bash
# Stiahnite z: https://www.python.org/downloads/
# Pri inštalácii zaškrtnite "Add Python to PATH"
```

### "Permission denied" pri spustení
```bash
# Linux/Mac:
chmod +x start_local_server.bat
```

### Port 8000 je obsadený
```bash
# Použite iný port:
python -m http.server 8080
# Potom: http://localhost:8080
```

### Niektoré obrázky sa nestiahli
```bash
# Znova spustite skript - dostiahne chýbajúce
python download_mirror.py
```

---

## 📊 Progress počas sťahovania

Uvidíte niečo takéto:
```
📥 [125/1000] 2011/02/hradec-prievidza.html
📊 Stiahnuté: 125 súborov (HTML: 85, Obrázky: 30, CSS: 5, JS: 5)
```

---

## 🎉 Hotovo!

Po dokončení:
1. ✅ Máte **kompletný backup** stránky
2. ✅ Funguje **offline** bez internetu
3. ✅ Môžete ju **editovať** podľa potreby
4. ✅ Pripravená na **archiváciu**

---

## 🔜 Ďalšie možnosti

Ak neskôr budete chcieť:
- **Modernú verziu** (Next.js): použite `run_migration.bat`
- **Word export**: spustite `python scripts/word_exporter.py`
- **Deploy na web**: najprv modernizujte, potom Vercel

---

## 💡 TIP

Odporúčam najprv urobiť túto lokálnu kópiu a potom sa rozhodnúť o ďalších krokoch. Budete mať:
- ✅ Bezpečný **backup**
- ✅ Čas na **preskúmanie** obsahu
- ✅ Možnosť **testovania** lokálne

---

**Otázky?** Skontrolujte hlavný `README.md` alebo `MIGRATION_PLAN.md`