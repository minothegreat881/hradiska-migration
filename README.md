# 🏰 Hradiska.sk - Kompletná Migrácia a Archív

Kompletný nástroj pre migráciu a archiváciu webstránky hradiska.sk (Slovanské Hradiská).

## 🎯 Čo tento projekt robí?

✅ Stiahne **celú webstránku** hradiska.sk lokálne  
✅ Archivuje všetky **články, obrázky, CSS, JS**  
✅ Stiahne a integruje všetky **komentáre** do článkov  
✅ Vytvorí **offline kópiu** ktorá funguje bez internetu  
✅ Pripravené na **migráciu do Next.js** a **export do Word**

---

## 🚀 Rýchly štart

### Windows:
```bash
download_only.bat
```

### Linux/Mac:
```bash
python3 download_mirror.py
```

Po dokončení spustite lokálny server:
```bash
start_local.bat        # Windows
# alebo
python -m http.server 8000 -d backup/hradiska_mirror
```

Otvorte prehliadač: **http://localhost:8000**

---

## 📊 Výsledky

Po stiahnutí budete mať:

- **214 HTML článkov** (roky 2010-2025)
- **743 obrázkov**
- **174 komentárov** (integrovaných do článkov)
- **~95 MB** kompletného obsahu
- **0% strát** - všetko offline!

---

## 🛠️ Nástroje v projekte

### Základné skripty:
- `download_mirror.py` - Stiahne celú stránku
- `verify_download.py` - Overí kompletnosť stiahnutia
- `download_missing_comments.py` - Dostiahne všetky komentáre
- `integrate_comments.py` - Integruje komentáre do HTML
- `analyze_comments.py` - Analyzuje komentáre

### Pomocné:
- `start_local.bat` - Spustí lokálny server
- `download_only.bat` - Jeden-klik stiahnutie (Windows)

---

## 📁 Štruktúra projektu

```
hradiska-migration/
├── backup/
│   └── hradiska_mirror/      # Stiahnutý obsah (NEKOMITUJE SA)
│       ├── index.html
│       ├── 2010-2025/        # Články podľa rokov
│       ├── images/           # 743 obrázkov
│       ├── feeds/            # XML comment feedy
│       └── search/           # Kategórie
├── download_mirror.py        # Hlavný scraper
├── integrate_comments.py     # Integrátor komentárov
└── README.md
```

---

## 🔧 Inštalácia

### Požiadavky:
- Python 3.8+
- requests, beautifulsoup4, lxml

### Inštalácia balíčkov:
```bash
pip install requests beautifulsoup4 lxml
```

---

## 💡 Použitie

### 1. Stiahnutie stránky
```bash
python download_mirror.py
```

### 2. Overenie
```bash
python verify_download.py
```

### 3. Stiahnutie komentárov
```bash
python download_missing_comments.py
```

### 4. Integrácia komentárov
```bash
python integrate_comments.py
```

### 5. Spustenie lokálne
```bash
python -m http.server 8000 -d backup/hradiska_mirror
```

---

## 📋 Features

- ✅ **Kompletný mirror** - všetky HTML, CSS, JS, obrázky
- ✅ **Inteligentné hashovanie** - dlhé URL skrátené pre Windows
- ✅ **Comment integration** - 174 komentárov v článkoch
- ✅ **UTF-8 podpora** - slovenské znaky fungujú
- ✅ **Error handling** - žiadne straty dát
- ✅ **Progress tracking** - vidíte čo sa deje

---

## 🌐 O hradiska.sk

Hradiska.sk je blog o slovanských hradiskách na Slovensku a v strednej Európe. Obsahuje:
- Archeologické nálezy
- Historické dokumenty
- 3D rekonštrukcie hradísk
- Mapy lokalít
- Vedecké články

---

## 📜 Licencia

Obsah stránky hradiska.sk patrí pôvodným autorom.  
Tento nástroj je určený pre archiváciu a osobné použitie.

---

## 👤 Autor migrácie

Created by **Milan** with ❤️ for preserving Slovak history

---

## 🔗 Odkazy

- **Pôvodná stránka**: http://www.hradiska.sk/
- **GitHub**: https://github.com/minothegreat881/hradiska-migration

---

**Poznámka**: Priečinok `backup/` obsahuje ~95MB dát a nie je súčasťou git repozitára. Po stiahnutí budete mať kompletný offline archív.
