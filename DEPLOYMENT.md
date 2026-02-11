# 🚀 Deployment Guide - Auto Services Scraper

Ghid pas-cu-pas pentru deployment complet pe GitHub.

## ✅ Pre-requisite

Înainte de deployment, asigură-te că ai:
- [x] Cont Google Cloud cu Places API activat
- [x] API Key generat și restricționat
- [x] Cont GitHub (free tier este ok)

## 📋 Checklist Deployment

### Step 1: Creează Repository GitHub

1. Accesează [github.com/new](https://github.com/new)
2. Configurare:
   - **Repository name**: `auto-service-rca-bot` (sau alt nume)
   - **Visibility**: **Public** (pentru GitHub Actions și Pages gratuit)
   - **Description**: "Scraper automat pentru service-uri auto din România"
   - ❌ **NU** adăuga README/LICENSE/.gitignore (le avem deja)
3. Click **Create repository**

### Step 2: Push Codul pe GitHub

În terminal, în folderul proiectului:

```bash
# Verifică că ești în directorul corect
pwd
# Output așteptat: /Users/ionut/Desktop/App-scraping-service-auto

# Adaugă remote origin (înlocuiește USERNAME cu username-ul tău GitHub)
git remote add origin https://github.com/USERNAME/auto-service-rca-bot.git

# Push pe branch main
git branch -M main
git push -u origin main
```

**Output așteptat**: "Branch 'main' set up to track remote branch 'main' from 'origin'."

### Step 3: Configurează GitHub Secret

1. În repository GitHub, mergi la **Settings** (tab-ul din dreapta)
2. Sidebar stânga → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Adaugă secretul:
   - **Name**: `GOOGLE_MAPS_API_KEY`
   - **Secret**: Paste cheia ta de la Google Cloud (începe cu `AIza...`)
5. Click **Add secret**

✅ Verificare: Ar trebui să vezi "GOOGLE_MAPS_API_KEY" în lista de secrets.

### Step 4: Activează GitHub Actions

1. Mergi la tab-ul **Actions** (în top menu)
2. Dacă vezi un mesaj despre workflows, click **I understand my workflows, go ahead and enable them**
3. Ar trebui să vezi workflow-ul "Scrape Auto Services"

### Step 5: Testează GitHub Actions (Rulare Manuală)

**IMPORTANT**: Înainte de prima rulare automată, testează manual!

1. În tab-ul **Actions**, click pe **Scrape Auto Services**
2. Click **Run workflow** (dropdown dreapta) → **Run workflow** (buton verde)
3. Așteaptă ~15-25 minute pentru rulare completă
4. Verifică:
   - ✅ Toate step-urile sunt verzi (✓)
   - ✅ Există un commit nou de la `github-actions[bot]`
   - ✅ Folderul `data/` conține `services.csv` și `services.xml`

**Debugging dacă fail**:
- Click pe run-ul roșu → Click pe job-ul "scrape" → Verifică logs
- Erori comune:
  - `GOOGLE_MAPS_API_KEY not set` → Secretul nu e configurat corect (recheck Step 3)
  - `Permission denied` → Settings → Actions → General → Workflow permissions → "Read and write" → Save

### Step 6: Activează GitHub Pages

1. Repository → **Settings** → **Pages** (sidebar stânga)
2. Configurare:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/ (root)`
3. Click **Save**
4. Așteaptă 2-3 minute
5. Refresh pagina - ar trebui să vezi:
   ```
   Your site is live at https://USERNAME.github.io/auto-service-rca-bot/
   ```

### Step 7: Actualizează URL în Dashboard

După primul scrape reușit (Step 5):

1. Editează `index.html` în GitHub:
   - Click pe fișier `index.html`
   - Click pe icon-ul ✏️ (Edit this file)
   - Găsește linia ~250:
     ```javascript
     const response = await fetch('data/services.xml');
     ```
   - Înlocuiește cu (actualizează USERNAME și REPO):
     ```javascript
     const response = await fetch('https://raw.githubusercontent.com/USERNAME/REPO/main/data/services.xml');
     ```
   - Commit changes

2. Așteaptă 2-3 minute pentru rebuild Pages
3. Vizitează dashboard-ul: `https://USERNAME.github.io/REPO/`

✅ **Success**: Ar trebui să vezi datele încărcate în tabel!

## 🎯 Verificare Finală

### Checklist Post-Deployment

- [ ] Repository GitHub creat și cod pushed
- [ ] Secret `GOOGLE_MAPS_API_KEY` configurat
- [ ] GitHub Actions rulează cu succes (manual test)
- [ ] Commit automat cu `data/services.csv` și `data/services.xml`
- [ ] GitHub Pages activat și funcțional
- [ ] Dashboard afișează datele corect
- [ ] CSV conține 400+ service-uri (după primul run)

### Test End-to-End

1. **API Scraping**:
   ```bash
   # Local test (optional)
   cd /Users/ionut/Desktop/App-scraping-service-auto
   source venv/bin/activate
   export GOOGLE_MAPS_API_KEY="your-key"
   python scrape_services.py
   # Verifică: data/services.csv și data/services.xml create
   ```

2. **GitHub Actions**:
   - Actions → Scrape Auto Services → Run workflow
   - Verifică logs: toate step-urile ✅

3. **Dashboard Web**:
   - Accesează `https://USERNAME.github.io/REPO/`
   - Testează filtre:
     - Oraș: Alege "București" → tabelul se filtrează
     - Size: Deselect "Small" → doar medium/large
     - Search: Scrie "mercedes" → caută în nume
     - Export CSV → descarcă fișier

4. **Google Sheets Import**:
   ```
   URL: https://raw.githubusercontent.com/USERNAME/REPO/main/data/services.csv

   Formula în A1:
   =IMPORTDATA("URL_DE_MAI_SUS")
   ```

## 📅 Programare Automată

Scriptul rulează **automat** în fiecare **luni la 05:00 AM** (ora României).

Pentru a schimba frecvența, editează `.github/workflows/scrape.yml`:

```yaml
schedule:
  - cron: "0 3 * * 1"  # Luni 03:00 UTC = 05:00 RO
```

Alte exemple:
- Daily (zilnic): `"0 3 * * *"`
- Bi-weekly (la 2 săptămâni): `"0 3 1,15 * *"`
- Monthly (lunar): `"0 3 1 * *"`

Tool util: [crontab.guru](https://crontab.guru/)

## 🔧 Troubleshooting

### Problema: Actions fail cu "API quota exceeded"

**Cauză**: Ai depășit 10,000 events/lună din free tier.

**Soluție**:
1. Verifică usage: [Google Cloud Console → APIs & Services → Dashboard](https://console.cloud.google.com/apis/dashboard)
2. Reduce frecvența (săptămânal → lunar)
3. Sau reduce orașe în `scrape_services.py` (SEARCH_QUERIES)

### Problema: Dashboard nu încarcă date ("Eroare: Nu s-au putut încărca datele")

**Cauze posibile**:
1. URL greșit în `index.html` (verifică linia ~250)
2. `data/services.xml` nu există în repo (rulează Actions mai întâi)
3. CORS issue (folosește `raw.githubusercontent.com`, NU `github.com`)

### Problema: Commit-ul automat nu funcționează

**Cauză**: Permisiuni GitHub Actions insuficiente.

**Soluție**:
1. Settings → Actions → General
2. Workflow permissions → **Read and write permissions**
3. ✅ "Allow GitHub Actions to create and approve pull requests"
4. Save

## 📊 Metrici de Monitorizat

După deployment, monitorizează:

1. **GitHub Actions logs**:
   - Success rate (ar trebui 100% după setup)
   - Runtime (15-25 min normal)
   - Număr service-uri găsite

2. **Google Cloud Console**:
   - API usage (ar trebui < 10k events/lună)
   - Errors (ar trebui 0)

3. **Dataset growth**:
   - Git commits săptămânale cu update-uri
   - Track în timp: service-uri noi adăugate

## 🎉 Done!

Sistemul tău de scraping este acum **complet automat** și **100% gratuit**!

### Next Steps

1. **Google Sheets**: Importă CSV-ul pentru analiză
2. **Email campaigns**: Folosește lista pentru outreach B2B
3. **Monitor**: Check GitHub Actions săptămânal pentru erori

### Suport

- Issues tehnice: [GitHub Issues](https://github.com/USERNAME/REPO/issues)
- Google Cloud: [Support Center](https://cloud.google.com/support)

---

**Happy scraping! 🚀**
