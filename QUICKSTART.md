# ⚡ Quick Start Guide

Get your scraper running in **30 minutes**! ⏱️

## 🎯 Prerequisites (5 min)

✅ Python 3.11+ installed
✅ GitHub account (free)
✅ Google account (for Cloud Console)

---

## 🚀 Setup Steps

### 1️⃣ Google Cloud API Key (10 min)

1. **Creează proiect**: https://console.cloud.google.com
   - Click "Select a project" → "New Project"
   - Name: `auto-services-rca-bot`
   - Click "Create"

2. **Activează Places API**:
   - Meniu ☰ → APIs & Services → Library
   - Search: "Places API" → Click → "Enable"

3. **Generează API Key**:
   - APIs & Services → Credentials → "+ Create Credentials" → "API Key"
   - **Copy key** (începe cu `AIza...`)

4. **Restricționează cheia**:
   - Click pe key-ul creat → "Edit API key"
   - API restrictions: "Restrict key" → Selectează **"Places API"**
   - Save

---

### 2️⃣ Local Test (5 min)

```bash
# Clone proiectul (dacă nu l-ai făcut deja)
cd /Users/ionut/Desktop/App-scraping-service-auto

# Creează virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalează dependințe
pip install -r requirements.txt

# Setează API key (înlocuiește cu al tău!)
export GOOGLE_MAPS_API_KEY="AIzaSy..."

# TEST cu 1 singur oraș (rapid!)
python -c "
import scrape_services as ss
ss.SEARCH_QUERIES = ['service auto Cluj-Napoca']
ss.main()
"
```

**✅ Success**: Ai `data/services.csv` și `data/services.xml` create!

---

### 3️⃣ Deploy pe GitHub (10 min)

1. **Creează repo**: https://github.com/new
   - Name: `auto-service-rca-bot`
   - Visibility: **Public** (pentru Actions gratuit!)
   - Click "Create repository"

2. **Push codul**:
   ```bash
   git remote add origin https://github.com/USERNAME/auto-service-rca-bot.git
   git push -u origin main
   ```

3. **Adaugă Secret**:
   - În GitHub repo → Settings → Secrets and variables → Actions
   - "New repository secret":
     - Name: `GOOGLE_MAPS_API_KEY`
     - Value: (paste cheia ta)
   - Click "Add secret"

4. **Testează Actions**:
   - Tab "Actions" → "Scrape Auto Services"
   - Click "Run workflow" → "Run workflow"
   - Wait ~20 min (ia o cafea ☕)

**✅ Success**: Workflow status = verde (✓), vezi commit de la `github-actions[bot]`!

---

### 4️⃣ GitHub Pages (5 min)

1. **Activează Pages**:
   - Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: `main`, `/root`
   - Save

2. **Editează index.html**:
   - Click pe `index.html` → ✏️ Edit
   - Linia ~250, schimbă:
     ```javascript
     // DE LA:
     const response = await fetch('data/services.xml');

     // LA (înlocuiește USERNAME și REPO):
     const response = await fetch('https://raw.githubusercontent.com/USERNAME/REPO/main/data/services.xml');
     ```
   - Commit changes

3. **Accesează dashboard**:
   - Wait 2 min pentru rebuild
   - Visit: `https://USERNAME.github.io/REPO/`

**✅ Success**: Vezi tabelul cu service-uri, filtre funcționează!

---

## 🎉 You're DONE!

Sistemul tău de scraping este acum **live și automat**!

### Ce se întâmplă acum?

- ⏰ **În fiecare luni la 05:00 AM** (România): Scraping automat
- 📊 **Dataset actualizat**: `data/services.csv` și `data/services.xml`
- 🌐 **Dashboard live**: Actualizat automat cu date noi

---

## 📖 Next Steps

### Imediat (5 min):
- [ ] Importă CSV în Google Sheets:
  ```
  =IMPORTDATA("https://raw.githubusercontent.com/USERNAME/REPO/main/data/services.csv")
  ```

### Astăzi (30 min):
- [ ] Citește [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Template email campaigns
- [ ] Testează filtre în dashboard (oraș, size, search)
- [ ] Export primul batch pentru outreach

### Săptămâna viitoare:
- [ ] Monitorizare: Check GitHub Actions (ar trebui verde ✓)
- [ ] Track conversii: Folosește template din USAGE_EXAMPLES
- [ ] Optimizare: Ajustează query-uri dacă vrei alte orașe

---

## 🐛 Probleme Comune

### "GOOGLE_MAPS_API_KEY not set"
→ Verifică secretul în GitHub: Settings → Secrets → Actions

### Dashboard nu încarcă date
→ Verifică URL în index.html linia ~250 (trebuie raw.githubusercontent.com)

### Actions fail: "Permission denied"
→ Settings → Actions → General → Workflow permissions → "Read and write"

### API Quota Exceeded
→ Verifică Google Cloud Console → APIs & Services → Dashboard

**More help**: [DEPLOYMENT.md](DEPLOYMENT.md) - Troubleshooting section

---

## 📊 Ce să aștepți?

### După primul run (20 min runtime):
- **400-600 service-uri** în dataset
- **40-50% au email** (~200-300 emailuri)
- **15-20% sunt LARGE** (high-value targets)

### După o lună (4 runs):
- **Dataset stabil** (aceleași service-uri, update info)
- **API usage**: ~4,000 events (40% din free tier)
- **Cost**: **$0** 💰

---

## 🎓 Learn More

📚 **Full Documentation**:
- [README.md](README.md) - Comprehensive guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Step-by-step deployment
- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Real-world use cases
- [COSTS_AND_LIMITS.md](COSTS_AND_LIMITS.md) - Scaling & pricing
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Feature checklist

---

**Happy scraping! 🚀**

Questions? Open an issue în repository!
