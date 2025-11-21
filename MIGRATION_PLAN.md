# Migračný plán pre hradiska.sk

## 📋 Prehľad projektu
Kompletná migrácia webstránky hradiska.sk vrátane zálohy, lokálneho spustenia, nasadenia na Vercel a exportu do Word dokumentov.

## 🎯 Ciele migrácie
1. Vytvorenie kompletnej lokálnej zálohy existujúcej stránky
2. Konverzia na modernú architektúru (Next.js/React)
3. Lokálne spustenie a testovanie
4. Nasadenie na Git a Vercel
5. Export všetkého obsahu do Word dokumentov

## 📁 Štruktúra projektu
```
hradiska-migration/
├── backup/                 # Originálna záloha stránky
│   ├── html/              # HTML súbory
│   ├── assets/            # Obrázky, CSS, JS
│   ├── documents/         # PDF a iné dokumenty
│   └── database/          # Exportované dáta
├── nextjs-app/            # Nová Next.js aplikácia
│   ├── pages/
│   ├── components/
│   ├── public/
│   └── content/
├── word-export/           # Word dokumenty
│   ├── articles/          # Jednotlivé články
│   ├── complete/          # Kompletný dokument
│   └── images/            # Obrázky pre Word
├── scripts/               # Migračné skripty
│   ├── scraper.py
│   ├── converter.py
│   └── word-exporter.py
└── docs/                  # Dokumentácia

```

## 🛠️ Technológie a nástroje
- **Web scraping**: Python (BeautifulSoup, Scrapy)
- **Lokálny server**: Node.js, Next.js
- **Version control**: Git
- **Hosting**: Vercel
- **Word export**: python-docx
- **Databáza obsahu**: JSON/Markdown

## 📊 Fázy migrácie

### Fáza 1: Analýza a príprava (1-2 dni)
- [ ] Mapovanie štruktúry stránky
- [ ] Identifikácia všetkých typov obsahu
- [ ] Vytvorenie zoznamu URL adries
- [ ] Analýza technológií použitých na stránke

### Fáza 2: Zálohovanie (2-3 dni)
- [ ] Stiahnutie všetkých HTML stránok
- [ ] Stiahnutie všetkých obrázkov a médií
- [ ] Záloha CSS a JavaScript súborov
- [ ] Export databázového obsahu (ak existuje)
- [ ] Vytvorenie sitemap.xml

### Fáza 3: Konverzia obsahu (3-4 dni)
- [ ] Parsovanie HTML do štruktúrovaných dát
- [ ] Konverzia na Markdown/MDX
- [ ] Optimalizácia obrázkov
- [ ] Vytvorenie JSON databázy článkov

### Fáza 4: Vývoj novej aplikácie (5-7 dní)
- [ ] Inicializácia Next.js projektu
- [ ] Vytvorenie komponentov
- [ ] Implementácia routingu
- [ ] Migrácia obsahu
- [ ] Styling a responzívny dizajn
- [ ] SEO optimalizácia

### Fáza 5: Testovanie (2-3 dni)
- [ ] Lokálne testovanie
- [ ] Kontrola všetkých odkazov
- [ ] Responzívne testovanie
- [ ] Výkonnostné testy
- [ ] SEO audit

### Fáza 6: Nasadenie (1 deň)
- [ ] Git repository setup
- [ ] Push na GitHub
- [ ] Vercel konfigurácia
- [ ] Nasadenie na produkciu
- [ ] DNS konfigurácia

### Fáza 7: Word export (2-3 dni)
- [ ] Vytvorenie šablóny Word dokumentu
- [ ] Export článkov
- [ ] Vloženie obrázkov
- [ ] Formátovanie a štruktúra
- [ ] Generovanie obsahu a indexu

## 🔧 Detailné kroky

### 1. Web Scraping Setup
```bash
# Inštalácia potrebných knižníc
pip install beautifulsoup4 scrapy requests wget python-docx
npm install -g website-scraper website-scraper-puppeteer
```

### 2. Stiahnutie celej stránky
```bash
# Použitie wget pre kompletné stiahnutie
wget --mirror --convert-links --adjust-extension --page-requisites --no-parent http://www.hradiska.sk/

# Alternatíva s HTTrack
httrack "http://www.hradiska.sk/" -O "./backup" "+*.hradiska.sk/*" -v
```

### 3. Next.js Setup
```bash
# Vytvorenie Next.js aplikácie
npx create-next-app@latest nextjs-app --typescript --tailwind --app
cd nextjs-app
npm install gray-matter remark remark-html
```

### 4. Git a Vercel
```bash
# Git inicializácia
git init
git add .
git commit -m "Initial commit"
git remote add origin [your-repo-url]
git push -u origin main

# Vercel nasadenie
vercel --prod
```

## 📝 Štruktúra Word dokumentu

### Hlavný dokument
1. **Titulná strana**
   - Názov: Slovanské Hradiská
   - Podnázov: Kompletná dokumentácia
   - Dátum exportu

2. **Obsah**
   - Automaticky generovaný
   - Hierarchická štruktúra

3. **Kapitoly**
   - Historické články
   - Archeologické nálezy
   - Mytológia a kultúra
   - Mapy a lokality
   - Galéria obrázkov

4. **Prílohy**
   - Zoznam všetkých URL
   - Technické detaily
   - Bibliografia

## 🎨 Dizajn konverzia
- Zachovanie originálnej farebnej schémy
- Responzívny dizajn pre mobilné zariadenia
- Optimalizácia rýchlosti načítania
- Moderné UI komponenty
- Zachovanie SEO hodnoty

## 📊 Odhadovaný časový harmonogram
- **Celková doba**: 15-20 pracovných dní
- **Analýza a príprava**: 2 dni
- **Zálohovanie**: 3 dni
- **Konverzia**: 4 dni
- **Vývoj**: 7 dní
- **Testovanie**: 3 dni
- **Nasadenie**: 1 deň
- **Word export**: 3 dni

## ⚠️ Riziká a riešenia
1. **Nedostupnosť stránky**: Použitie web archive
2. **Veľký objem dát**: Postupné spracovanie
3. **Komplexná štruktúra**: Manuálna kontrola
4. **SEO strata**: 301 redirecty
5. **Chýbajúce súbory**: Záložné zdroje

## 📌 Kontrolný zoznam pred spustením
- [ ] Záloha všetkých dát
- [ ] Test lokálneho prostredia
- [ ] Kontrola všetkých odkazov
- [ ] SEO meta tagy
- [ ] Responzívny dizajn
- [ ] Výkonnostné testy
- [ ] Bezpečnostná kontrola
- [ ] Word dokumenty skompletizované

## 🚀 Post-migračné aktivity
1. Monitoring výkonu
2. Pravidelné zálohy
3. Aktualizácie obsahu
4. SEO optimalizácia
5. Užívateľská spätná väzba