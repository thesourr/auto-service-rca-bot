# 🚗 Service-uri Auto România - Scraper Automat

Sistem automat de colectare și clasificare a service-urilor auto din România pentru promovarea serviciilor RCA de recuperare creanțe.

## 📋 Descriere

Această aplicație colectează **legal** date publice despre service-uri auto din România folosind:
- **Google Maps Places API** (sursa oficială, respectă ToS)
- **Web scraping** din website-uri publice (doar pentru emailuri de contact business)

### Funcționalități

✅ Caută service-uri auto în top 10 orașe din România
✅ Clasificare automată: SMALL / MEDIUM / LARGE (după număr review-uri)
✅ Extragere date contact: email, telefon, website, adresă
✅ Output în CSV (Google Sheets) și XML
✅ Actualizare automată săptămânală cu GitHub Actions
✅ Dashboard web interactiv cu filtre și căutare
✅ **100% gratuit** (free tier Google + GitHub)

## 🏗️ Arhitectură

```
┌─────────────────┐
│ Google Maps API │
│  (Text Search + │
│ Place Details)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│ scrape_services │─────▶│ data/        │
│     .py         │      │ services.csv │
└────────┬────────┘      │ services.xml │
         │               └──────┬───────┘
         │                      │
         ▼                      ▼
┌─────────────────┐      ┌──────────────┐
│ GitHub Actions  │      │ index.html   │
│ (cron weekly)   │      │ (Dashboard)  │
└─────────────────┘      └──────────────┘
```

## 🚀 Setup Rapid

### 1. Prerequisites

- **Python 3.11+**
- **Cont Google Cloud** (pentru API key)
- **Cont GitHub** (pentru automatizare și hosting)

### 2. Google Cloud Setup

1. Accesează [Google Cloud Console](https://console.cloud.google.com)
2. Creează un proiect nou: `auto-services-rca-bot`
3. Activează **Places API**:
   - Meniu → APIs & Services → Library
   - Caută "Places API" → Enable
4. Creează API Key:
   - APIs & Services → Credentials → Create Credentials → API Key
   - Restricționează cheia:
     - **API restrictions**: doar Places API
     - **Application restrictions**: None (pentru GitHub Actions)
5. Notează cheia - o vei folosi mai jos

**Cost**: ~$0/lună în free tier (10,000 billable events/lună incluse)

### 3. Instalare Locală

```bash
# Clone repository
git clone https://github.com/USERNAME/auto-service-rca-bot.git
cd auto-service-rca-bot

# Creează virtual environment
python -m venv venv
source venv/bin/activate  # Pe Windows: venv\Scripts\activate

# Instalează dependințe
pip install -r requirements.txt

# Setează API key (înlocuiește cu cheia ta)
export GOOGLE_MAPS_API_KEY="AIza..."

# Rulează scraper
python scrape_services.py
```

După rulare, vei avea:
- `data/services.csv` - pentru Google Sheets
- `data/services.xml` - pentru dashboard

### 4. GitHub Actions Setup (Automatizare)

1. **Creează repository GitHub** (public pentru Actions gratuit)

2. **Adaugă secretul API**:
   - Settings → Secrets and variables → Actions
   - New repository secret:
     - Name: `GOOGLE_MAPS_API_KEY`
     - Value: cheia ta de la Google Cloud

3. **Push codul**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/USERNAME/REPO.git
   git push -u origin main
   ```

4. **Activează GitHub Actions**:
   - Mergi la tab-ul **Actions**
   - Permite workflows
   - Rulare manuală: Actions → Scrape Auto Services → Run workflow

**Programare**: Automatizat în fiecare **luni la 05:00 AM** (ora României)

### 5. GitHub Pages Setup (Dashboard Web)

1. **Activează Pages**:
   - Settings → Pages
   - Source: **Deploy from a branch**
   - Branch: `main`, `/root`
   - Save

2. **Actualizează URL în `index.html`**:
   - Deschide `index.html`
   - Găsește linia ~250: `const response = await fetch('data/services.xml');`
   - Înlocuiește cu:
     ```javascript
     const response = await fetch('https://raw.githubusercontent.com/USERNAME/REPO/main/data/services.xml');
     ```

3. **Accesează dashboard-ul**:
   - `https://USERNAME.github.io/REPO/`

## 📊 Structura Datelor

### CSV (`data/services.csv`)

| Coloană | Descriere | Exemplu |
|---------|-----------|---------|
| `id` | Google Place ID | `ChIJ...` |
| `name` | Nume service | `Service Auto Exemplu SRL` |
| `size` | Clasificare | `small`, `medium`, `large` |
| `email` | Email contact | `contact@service.ro` |
| `phone` | Telefon | `+40 721 000 000` |
| `website` | Website | `https://service.ro` |
| `address` | Adresă completă | `Str. Exemplu 1, București, România` |
| `city` | Oraș | `București` |
| `rating` | Rating Google | `4.6` |
| `reviews` | Număr review-uri | `123` |
| `source` | Sursă date | `google_places` |
| `last_updated` | Timestamp | `2026-02-11T10:30:00Z` |

### Clasificare Dimensiune

- **SMALL**: < 50 review-uri Google
- **MEDIUM**: 50-199 review-uri
- **LARGE**: ≥ 200 review-uri
- **UNKNOWN**: fără review-uri

## 📈 Import în Google Sheets

### Opțiunea 1: Import Manual

1. Download `data/services.csv` din GitHub
2. Google Sheets → File → Import → Upload
3. Alege "Insert new sheet"

### Opțiunea 2: Import Dinamic (Auto-refresh)

1. Obține URL raw CSV:
   ```
   https://raw.githubusercontent.com/USERNAME/REPO/main/data/services.csv
   ```

2. În Google Sheets, celula A1:
   ```
   =IMPORTDATA("URL_DE_MAI_SUS")
   ```

3. Datele se actualizează automat când GitHub Actions rulează!

## 🎯 Orașe Acoperite

### București (8 query-uri)
- București general + 6 sectoare + Ilfov

### Top 9 Orașe
1. Cluj-Napoca
2. Timișoara
3. Iași
4. Constanța
5. Craiova
6. Brașov
7. Galați
8. Ploiești
9. Oradea

**Total estimat**: 400-600 service-uri

## 🔐 Considerații GDPR & Legale

### Date Colectate

- **Tip**: Business contact data (nu date personale consumatori)
- **Surse**:
  - Google Maps Places API (date publice disponibile oricui)
  - Website-uri publice (secțiune Contact/Footer)

### Bază Legală

- **Art. 6(1)(f) GDPR**: Interes legitim
- **Scop**: Oferire servicii B2B (recuperare creanțe RCA către service-uri auto)
- **Minimizare**: Doar date strict necesare pentru contact business
- **Transparență**: În emailurile trimise, menționează:
  - Sursa: "Datele au fost preluate din Google Maps și site-ul public al companiei"
  - Opt-out: "Pentru dezabonare, răspundeți cu STOP"

### Best Practices

✅ Rate limiting (0.3s între requesturi)
✅ User-Agent clar în HTTP requests
✅ Respectă cererile de dezabonare
✅ Re-scraping lunar pentru date fresh
✅ Nu trimite spam - targetare inteligentă pe size

## 🛠️ Dezvoltare

### Structura Proiectului

```
auto-service-rca-bot/
├── scrape_services.py       # Script principal Python
├── requirements.txt          # Dependințe
├── index.html               # Dashboard web
├── README.md                # Această documentație
├── .gitignore              # Git ignore rules
├── data/
│   ├── services.csv        # Output CSV (generat)
│   └── services.xml        # Output XML (generat)
└── .github/
    └── workflows/
        └── scrape.yml      # GitHub Actions workflow
```

### Modificare Listă Orașe

Editează `scrape_services.py`, linia ~13:

```python
SEARCH_QUERIES = [
    "service auto București",
    "service auto Tău Oraș",  # Adaugă aici
    # ...
]
```

### Rulare Teste Locale

```bash
# Test cu un singur oraș (pentru a economisi API calls)
python -c "
import scrape_services as ss
ss.SEARCH_QUERIES = ['service auto Cluj-Napoca']
ss.main()
"
```

## 📊 Metrici Așteptate

| Metric | Valoare Estimată |
|--------|------------------|
| Total service-uri | 400-600 |
| % cu email | 30-50% |
| % Large size | 15-20% |
| API calls/run | ~2,000-3,000 |
| Cost/lună | $0 (free tier) |
| Runtime/scrape | ~15-25 min |

## 🚨 Troubleshooting

### Eroare: "GOOGLE_MAPS_API_KEY nu este setat"

```bash
# Verifică dacă e setat
echo $GOOGLE_MAPS_API_KEY

# Setează din nou
export GOOGLE_MAPS_API_KEY="cheia-ta"
```

### GitHub Actions fail: "Permission denied"

1. Settings → Actions → General
2. Workflow permissions → **Read and write permissions**
3. Save

### Dashboard nu încarcă date

1. Verifică URL în `index.html` (linia ~250)
2. Asigură-te că `data/services.xml` există în repo
3. Verifică că GitHub Pages este activat (Settings → Pages)
4. Wait 2-3 minute pentru deploy

### API Quota Exceeded

- Free tier: 10,000 events/lună
- Un scrape complet = ~2,500 events
- Soluție: Rulează mai rar (de la săptămânal la lunar)

## 🔮 Extensii Viitoare

### Phase 2 (Post-MVP)
- [ ] Email sending automation (SendGrid/Mailgun)
- [ ] CRM integration (HubSpot/Salesforce export)
- [ ] Advanced scraping (pagină Contact dedicată)
- [ ] Analytics dashboard (grafice evoluție)

### Phase 3
- [ ] Multi-source (Facebook Pages API, Pagini Aurii)
- [ ] AI classification (detectare specializări: Mercedes, BMW, etc.)
- [ ] Lead scoring (probabilitate conversie)

## 📝 Licență

MIT License - free to use pentru scopuri comerciale și personale.

## 🤝 Contact & Suport

Pentru întrebări sau îmbunătățiri, deschide un [GitHub Issue](https://github.com/USERNAME/REPO/issues).

---

**Made with ❤️ for RCA recovery services**

*Ultima actualizare: Februarie 2026*
