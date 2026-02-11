# 🔧 Fix REQUEST_DENIED Errors - Ghid Pas cu Pas

**Status**: ⚠️ NECESITĂ ACȚIUNE MANUALĂ
**Timp estimat**: 5-10 minute

---

## 🎯 Problema

Când GitHub Actions rulează, vezi erori de tipul:
```
[WARNING] Place details error for ChIJ...: REQUEST_DENIED
```

Aceasta înseamnă că **API key-ul nu are permisiunile necesare** pentru Place Details API.

---

## ✅ Soluție - 3 Pași Simpli

### Pasul 1: Verifică Google Cloud Console

1. **Deschide Google Cloud Console**:
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. **Selectează proiectul** (dacă ai mai multe):
   - Click pe dropdown-ul proiectului (sus, în navbar)
   - Selectează proiectul unde ai creat API key-ul

---

### Pasul 2: Activează Place Details API

⚠️ **IMPORTANT**: Ai nevoie de DOUĂ API-uri activate:

1. **Mergi la API Library**:
   ```
   https://console.cloud.google.com/apis/library
   ```

2. **Activează Places API (New)**:
   - Caută: "Places API (New)"
   - Click pe rezultat
   - Click **ENABLE** (dacă nu e deja activat)
   - **SAU** caută "Places API" (versiunea veche funcționează și ea)

3. **Verifică că sunt activate AMBELE**:
   - **Places API** ✅
   - **Geocoding API** ✅ (opțional, dar recomandat)

---

### Pasul 3: Verifică Restricțiile API Key

1. **Mergi la Credentials**:
   ```
   https://console.cloud.google.com/apis/credentials
   ```

2. **Găsește API key-ul tău**:
   - Caută în listă key-ul care începe cu `AIzaSyA...`
   - Click pe numele key-ului pentru a-l edita

3. **Verifică "API restrictions"**:

   **Opțiunea A - Fără restricții (RECOMANDAT pentru testare)**:
   - Selectează: **"Don't restrict key"**
   - ⚠️ Temporar pentru testare, apoi restrânge la Places API

   **Opțiunea B - Cu restricții**:
   - Selectează: **"Restrict key"**
   - Bifează AMBELE:
     - ☑️ Places API (New) SAU Places API
     - ☑️ Geocoding API (opțional)

4. **Application restrictions**:
   - Lasă: **None** (pentru GitHub Actions)

5. **Click SAVE**

---

### Pasul 4: Activează Billing (Dacă e necesar)

⚠️ **Place Details API necesită billing activat** (dar rămâi în free tier!)

1. **Verifică dacă ai billing activat**:
   ```
   https://console.cloud.google.com/billing
   ```

2. **Dacă NU ai billing**:
   - Click **"Link a billing account"**
   - Adaugă card (NU vei fi taxat dacă rămâi sub 10,000 requests/lună)
   - Google oferă $300 credit gratuit pentru new accounts!

3. **Free Tier limits** (NU plătești nimic dacă rămâi sub):
   ```
   Places API Text Search:  1,000 requests/lună FREE
   Place Details:           SKU-uri gratis în first-tier
   Total billable events:   10,000/lună în $200 monthly credit
   ```

**Estimare pentru acest proiect**:
- 1 rulare completă = ~2,500 billable events
- 4 rulări/lună (weekly) = ~10,000 events
- **Cost estimat**: $0/lună (sub free tier) ✅

---

## 🧪 Testare

După ce ai făcut modificările:

### Test 1: Rulare Manuală Locală

```bash
cd /Users/ionut/Desktop/App-scraping-service-auto
source venv/bin/activate

# Setează API key-ul NOU
export GOOGLE_MAPS_API_KEY="YOUR_GOOGLE_MAPS_API_KEY"

# Testează cu UN SINGUR oraș (economisește API calls)
python -c "
import scrape_services as ss
ss.SEARCH_QUERIES = ['service auto Cluj-Napoca']
ss.main()
"
```

**Verifică output-ul**:
- ✅ **NU ar trebui** să vezi `[WARNING] Place details error`
- ✅ Ar trebui să vezi: `Found X new places`
- ✅ Fișierele `data/services.csv` și `data/services.xml` se creează

---

### Test 2: GitHub Actions

```bash
# Trigger manual workflow
gh workflow run scrape.yml --repo thesourr/auto-service-rca-bot

# Așteaptă ~2 minute, apoi verifică
gh run list --repo thesourr/auto-service-rca-bot --limit 1
```

**Verifică logs**:
```bash
gh run view --repo thesourr/auto-service-rca-bot --log
```

**Așteptat**:
- ✅ NU mai apar erori `REQUEST_DENIED`
- ✅ `Total services in database: XXX`
- ✅ `NEW services added this run: YYY`

---

## 📊 Verificare Finală

### 1. Dashboard Funcțional

Vizitează: https://thesourr.github.io/auto-service-rca-bot/

**Verifică**:
- ✅ Tabelul se încarcă cu service-uri
- ✅ Statistici corecte (total, % email)
- ✅ Filtre funcționează (oraș, size)

### 2. CSV în Google Sheets

```
=IMPORTDATA("https://raw.githubusercontent.com/thesourr/auto-service-rca-bot/main/data/services.csv")
```

---

## 🚨 Troubleshooting

### Încă primesc REQUEST_DENIED

**Cauză 1: Key restrictions prea stricte**
- Soluție: Setează "Don't restrict key" temporar

**Cauză 2: Place Details API nu e activat**
- Soluție: Activează din API Library (Pasul 2)

**Cauză 3: Billing nu e activat**
- Soluție: Activează billing (Pasul 4)

**Cauză 4: Key-ul greșit în GitHub Secrets**
- Soluție: Verifică că secret-ul `GOOGLE_MAPS_API_KEY` e corect:
  ```bash
  gh secret set GOOGLE_MAPS_API_KEY --body "YOUR_GOOGLE_MAPS_API_KEY" --repo thesourr/auto-service-rca-bot
  ```

---

### Erori INVALID_REQUEST

**Cauză**: Query-ul nu returnează rezultate
**Soluție**: Normal, unele orașe au mai puține service-uri

---

### Billing Alert (dacă activezi billing)

**Setup alertă** pentru a fi notificat dacă depășești free tier:

1. https://console.cloud.google.com/billing/budgets
2. **Create Budget**:
   - Amount: $5
   - Email alerts: at 50%, 90%, 100%

---

## ✅ Checklist Final

- [ ] Places API (New) SAU Places API activat în API Library
- [ ] API Key restricții verificate (None sau Places API explicit)
- [ ] Billing activat (dacă e necesar)
- [ ] Test local rulează fără `REQUEST_DENIED`
- [ ] GitHub Actions rulează fără erori
- [ ] Dashboard afișează date noi
- [ ] CSV poate fi importat în Google Sheets

---

## 📞 Link-uri Utile

| Resursă | URL |
|---------|-----|
| Google Cloud Console | https://console.cloud.google.com |
| API Credentials | https://console.cloud.google.com/apis/credentials |
| API Library | https://console.cloud.google.com/apis/library |
| Billing | https://console.cloud.google.com/billing |
| GitHub Actions | https://github.com/thesourr/auto-service-rca-bot/actions |
| Dashboard | https://thesourr.github.io/auto-service-rca-bot/ |

---

**Status**: ⏳ AȘTEAPTĂ ACȚIUNE

**Next Step**: Urmează Pasul 1 → Verifică Google Cloud Console

---

Built: 2026-02-11
Repository: https://github.com/thesourr/auto-service-rca-bot
