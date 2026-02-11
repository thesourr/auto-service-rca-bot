# 💰 Costs & Limits Analysis

Analiză detaliată a costurilor și limitărilor pentru sistemul de scraping.

## 📊 Cost Breakdown (FREE TIER)

### Google Maps Places API

**Free Tier (din 1 Martie 2025)**:
- **10,000 billable events/lună** GRATUIT
- Costul după free tier: $17 / 1,000 events

**Events per Scrape Run**:

```
1 Text Search Request = 1 event
1 Place Details Request = 1 event

Estimare per oraș:
- Text Search: ~1-3 events (cu paginare)
- Place Details: ~40-60 events (câte service-uri găsește)
- Total/oraș: ~45-65 events

Pentru 17 query-uri (București + 9 orașe):
17 × 55 events = ~935 events/run
```

**Runs permise/lună în FREE TIER**:
```
10,000 events ÷ 935 events = ~10 runs/lună
```

**Recomandare**: Rulare **săptămânală** (4 runs/lună) → **~3,740 events** → **100% GRATUIT** ✅

### GitHub

**GitHub Actions (Free Tier)**:
- **2,000 minute/lună** pentru repo public
- **UNLIMITED** pentru repo public (din 2024)

**Usage per Run**:
- Runtime: ~15-25 minute
- CPU: Standard Linux runner (2-core)

**Concluzie**: **GRATUIT COMPLET** pentru repo public ✅

**GitHub Pages**:
- **100 GB bandwidth/lună**
- **1 GB storage**

**Usage**:
- Dashboard HTML: ~15 KB
- services.xml: ~200 KB (pentru 500 service-uri)
- Total storage: < 1 MB

**Concluzie**: **GRATUIT** cu marjă enormă ✅

## 🚧 Rate Limits & Restrictions

### Google Maps API Limits

**Requests per Second (QPS)**:
- Text Search: 10 QPS
- Place Details: 10 QPS

**Impact**: Zero, scriptul are sleep(0.3s) = ~3 RPS

**Daily Quota**: None oficial (doar monthly free tier)

**Burst Limits**: 1,000 requests în scurt timp = OK

### GitHub Actions Limits

**Job Execution Time**:
- Max: 6 ore/job
- Typical: 15-25 minute

**Concurrent Jobs**:
- Free tier public repo: 20 concurrent jobs
- Noi folosim: 1 job

**Storage**:
- Artifacts: 500 MB
- Noi folosim: 0 (nu salvăm artifacts)

### GitHub Pages Limits

**Build Time**: ~10 minute
**File Size**: Max 100 MB/fișier
**Total Size**: Max 1 GB

## 💸 Cost Scaling Scenarios

### Scenario 1: CURRENT (Săptămânal, 17 orașe)

```
API Events/lună:     3,740
Google Cost:         $0 (sub free tier)
GitHub Cost:         $0 (repo public)
Total:               $0/lună ✅
```

### Scenario 2: SCALING (Zilnic, 17 orașe)

```
Runs:                30/lună
API Events/lună:     30 × 935 = 28,050
Events over free:    28,050 - 10,000 = 18,050
Google Cost:         18,050/1,000 × $17 = $306.85/lună ❌
GitHub Cost:         $0
Total:               ~$307/lună
```

**Recomandare**: Zilnic e prea scump, rămâi la săptămânal!

### Scenario 3: OPTIMIZARE (Săptămânal, doar service-uri noi)

Implementare differential scraping (vezi USAGE_EXAMPLES.md):

```
Prima rulare:        935 events (full scrape)
Rulări următoare:   ~200 events (doar noi)

Events/lună:         935 + (3 × 200) = 1,535 events
Google Cost:         $0 (sub free tier)
Savings:             59% API calls ✅
```

### Scenario 4: NAȚIONAL (Toate orașele >100k locuitori)

România are ~40 orașe >100k locuitori:

```
Query-uri:           40 orașe × 2 query-uri = 80
Events/oraș:         55 (medie)
Events/run:          80 × 55 = 4,400

Runs săptămânal:     4/lună
Events/lună:         17,600
Over free tier:      7,600
Google Cost:         7,600/1,000 × $17 = $129.20/lună
Total:               ~$130/lună
```

**ROI Analysis**:
- Dataset: ~2,000-3,000 service-uri
- Cost/service: $130 / 2,500 = **$0.052/service**
- Dacă 1 conversie = 1 client nou → **Worth it!**

## 🎯 Cost Optimization Strategies

### 1. Differential Scraping ⭐ BEST

**Idea**: Update doar service-uri noi, skip existente

**Implementare**:
```python
# Load existing place_ids
existing = load_csv_ids('data/services.csv')

# În loop:
if place_id in existing:
    continue  # Skip Place Details call
```

**Savings**: 60-80% API calls după prima rulare

### 2. Targeted Scraping

**Idea**: Focusează doar pe orașe high-value

```python
# În loc de 17 query-uri, doar:
SEARCH_QUERIES = [
    "service auto București",
    "service auto Cluj-Napoca",
    "service auto Timișoara",
]
```

**Savings**: 65% API calls (17 → 6 orașe)
**Tradeoff**: Mai puține leads, dar costuri zero

### 3. Batch Place Details

**Idea**: Google permite 1 request cu multiple places (în unele API-uri)

**Status**: ❌ **NU funcționează** pentru Place Details
- Trebuie 1 request/place_id

**Alternative**: None, e single-threaded by design

### 4. Caching & Stale Data Tolerance

**Idea**: Unele date (address, phone) nu se schimbă des

**Implementare**:
```python
# Re-scrape doar dacă last_updated > 30 zile
if (today - last_updated).days < 30:
    skip_details = True
```

**Savings**: ~40% API calls
**Tradeoff**: Emailuri/website-uri noi missed pentru 1 lună

### 5. Reduce Query Specificity

**Current**:
```python
"service auto sector 1 București"  # Specific
```

**Optimized**:
```python
"service auto București"  # Generic, mai multe rezultate/query
```

**Savings**: Mai puține query-uri, dar:
- ⚠️ Risc: Duplicate results între query-uri
- ✅ Filter cu `seen_places` previne duplicates

## 📈 Scaling Decision Matrix

| Dataset Size | Frequency | Orașul Count | Events/lună | Cost/lună | Recomandare |
|--------------|-----------|--------------|-------------|-----------|-------------|
| 500          | Weekly    | 10           | 3,000       | $0        | ✅ Perfect  |
| 1,000        | Weekly    | 20           | 6,000       | $0        | ✅ OK       |
| 2,000        | Weekly    | 40           | 12,000      | $34       | ⚠️ Decide  |
| 500          | Daily     | 10           | 12,000      | $34       | ❌ Prea mult|
| 3,000        | Weekly    | All RO       | 20,000      | $170      | ⚠️ ROI?    |

**Regula de aur**: Stay < 10,000 events/lună pentru $0 cost!

## 🔍 Free Tier Monitoring

### Verificare Usage Google Cloud

1. [Google Cloud Console](https://console.cloud.google.com)
2. Navigation menu → **APIs & Services** → **Dashboard**
3. Selectează proiectul tău
4. Click pe **Places API**
5. Tab **Metrics**

**Red flags**:
- Usage aproape de 10,000/lună → Reduce frecvența
- Sudden spike → Bug în script (infinite loop?)

### Setup Budget Alert (Recommended!)

1. Google Cloud Console → **Billing** → **Budgets & alerts**
2. **Create Budget**:
   - Name: "Places API Budget"
   - Budget amount: $10/lună
   - Alert thresholds: 50%, 90%, 100%
   - Email notification: your-email@domain.com

**Beneficiu**: Notificare automată dacă depășești free tier

### GitHub Actions Usage

1. GitHub → Settings → **Billing and plans**
2. **Plans and usage** → **Actions**
3. Verifică: Minutes used (ar trebui < 100 min/lună)

## 🚨 Common Cost Pitfalls

### Pitfall 1: Infinite Loop în Scraper

**Cauză**: Bug în paginare (`next_page_token` logic greșită)

**Impact**: 10,000+ API calls în 1 run → $170 cost

**Prevenție**:
```python
max_pages = 5  # Safety limit
page_count = 0

while next_page_token and page_count < max_pages:
    # ...
    page_count += 1
```

### Pitfall 2: Rulare Manuală Repetată

**Cauză**: Debug în Actions, apăși "Run workflow" de 10 ori/zi

**Impact**: 10 × 935 = 9,350 events → Aproape limita free tier

**Prevenție**: Test local mai întâi, apoi 1 test în Actions

### Pitfall 3: Duplicate Scraping

**Cauză**: Uiți să verifici `seen_places`, scrapezi același service de 3 ori

**Impact**: 3× API usage inutil

**Prevenție**: Verifică logs după run - "Found X NEW places" (nu "Found X places total")

## 💡 Alternative Free Data Sources

Dacă vrei să extinzi fără cost:

### 1. **Facebook Places API**

- **Free Tier**: 200 calls/oră, 5,000/zi
- **Data**: Nume, locație, reviews, mesaje (dacă au Messenger)
- **Setup**: Complex (app review), dar gratuit

### 2. **Web Scraping Direct (fără API)**

⚠️ **ATENȚIE**: Verifică ToS!

- **Pagini Aurii** (paginiaurii.ro): robots.txt permite scraping
- **Extrage**: Nume, telefon, categorie
- **Limitare**: Nu au reviews/rating

### 3. **OpenStreetMap Overpass API**

- **Free**: Complet gratuit, no rate limit (rezonabil usage)
- **Data**: Locații POI cu `amenity=car_repair`
- **Limitare**: Date incomplete (multe fără contact)

**Exemplu query**:
```
[out:json];
node["amenity"="car_repair"]["addr:city"="București"];
out;
```

### 4. **User Contributed (Crowdsourcing)**

- Creează formular: "Adaugă service-ul tău"
- Oferă incentive: "Primii 50 = discount 20%"
- **Cost**: $0, dar necesită marketing

## 📊 ROI Calculator

### Input-uri:

```
Cost scraping/lună:        $0 (free tier)
Timp setup:                3 ore (one-time)
Timp mentenanță:           1 oră/lună

Service-uri în DB:         500
Email availability rate:   40% → 200 emailuri
Email campaign cost:       $0 (Gmail) sau $15/lună (SendGrid)

Conversion rate:           2% → 4 clienți noi/lună
Revenue/client:            €500 (medie contract RCA recovery)
```

### Output:

```
Revenue/lună:              4 × €500 = €2,000
Costs/lună:                $0 scraping + $15 email = €14
Profit/lună:               €1,986
ROI:                       14,000% 🚀

Breakeven:                 Immediate (cost ≈ 0)
```

**Concluzie**: Chiar și cu conversion rate 1%, sistemul e **extremely profitable**!

## 🎓 Key Takeaways

✅ **FREE pentru usage rezonabil** (săptămânal, 10-20 orașe)
✅ **Scalabil până la $130/lună** pentru coverage național complet
✅ **ROI enorm** chiar cu costuri (14,000%+ dacă optimizat)
✅ **Predictabil** - poți calcula exact costurile înainte

⚠️ **Watch out pentru**:
- Infinite loops (safety limits în cod)
- Manual re-runs în Actions (test local)
- Scaling prea rapid fără monitoring

📈 **Best practice**: Start free (săptămânal), measure conversions, apoi decide dacă merită scaling cu cost.

---

**Bottom line**: Sistemul poate rămâne **100% gratuit indefinit** dacă respecți limitele recomandate!
