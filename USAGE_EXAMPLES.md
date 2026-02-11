# 📚 Usage Examples & Best Practices

Exemple concrete de utilizare a datelor colectate pentru promovarea serviciilor RCA.

## 🎯 Cazuri de Utilizare

### 1. Email Campaign pentru Service-uri Mari

**Obiectiv**: Targetare service-uri cu volum mare de lucru (potențial mai multe cazuri RCA)

**Filtrare în Google Sheets**:
```
=FILTER(A2:L1000, C2:C1000="large", D2:D1000<>"")
```
- Coloana C = size
- Coloana D = email
- Rezultat: Doar service-uri LARGE care au email

**Template Email Recomandat**:
```
Subiect: Recuperare RCA - Creșteți veniturile service-ului

Bună ziua,

Numele meu este [NUME] și reprezint [COMPANIA], specializată în
recuperarea creanțelor RCA pentru service-uri auto.

Am observat pe Google Maps că [NUME_SERVICE] are un rating excelent
de [RATING] stele cu [REVIEWS] recenzii - felicitări pentru munca
de calitate!

Colaborăm cu service-uri auto pentru recuperarea banilor de la
asigurători în cazuri RCA. În medie, service-urile partenere
recuperează cu 15-25% mai mulți bani decât singure.

Putem programa un apel scurt de 15 minute săptămâna viitoare pentru
a discuta cum vă putem ajuta?

Cu respect,
[SEMNATURA]

---
P.S. Datele de contact au fost preluate din Google Maps și site-ul
public al companiei. Dacă nu doriți să primiți astfel de propuneri,
răspundeți cu "STOP".
```

### 2. Cold Calling - Prioritizare pe Oraș

**Obiectiv**: Vizite fizice la service-uri din București

**Filtrare**:
```
=FILTER(A2:L1000, H2:H1000="București", E2:E1000<>"")
```
- Coloana H = city
- Coloana E = phone

**Script Telefon**:
```
Bună ziua, numele meu este [NUME] de la [COMPANIA].

Suntem specializați în recuperarea creanțelor RCA pentru service-uri
auto și am vrea să discutăm despre cum putem colabora.

Aveți 5 minute acum sau preferați să vă sun săptămâna viitoare?

[Dacă NU]
Perfect, când ar fi un moment mai potrivit? Marți la 10:00?

[Dacă DA]
Excelent! Să vă spun pe scurt...
```

### 3. Segmentare Multi-Criteriu

**Obiectiv**: Medium/Large service-uri din top 5 orașe cu email

**Google Sheets Formula**:
```
=QUERY(A2:L1000,
  "SELECT * WHERE
   (C='medium' OR C='large') AND
   D<>'' AND
   (H='București' OR H='Cluj-Napoca' OR H='Timișoara' OR H='Iași' OR H='Constanța')",
  1)
```

**Rezultat**: Lista optimă pentru campanii high-value

### 4. A/B Testing pe Orașe

**Setup**:
- **Grupa A (București)**: Email cu discount 10% primul contract
- **Grupa B (Cluj)**: Email fără discount, focus pe case studies

**Tracking în Google Sheets**:
```
| Service | City | Email Sent | Opened | Replied | Converted | Group |
|---------|------|------------|--------|---------|-----------|-------|
| Service1| BCU  | 2026-02-15 | Yes    | Yes     | No        | A     |
| Service2| CLJ  | 2026-02-15 | Yes    | No      | No        | B     |
```

**Analiza după 2 săptămâni**:
```
=COUNTIFS(G:G, "A", E:E, "Yes") / COUNTIFS(G:G, "A")  // Open rate A
=COUNTIFS(G:G, "B", E:E, "Yes") / COUNTIFS(G:G, "B")  // Open rate B
```

## 🔍 Filtrare Avansată în Dashboard Web

### Exemplu 1: Service-uri noi (rating mic, potențial underserved)

1. Accesează dashboard: `https://USERNAME.github.io/REPO/`
2. Filtre:
   - **Size**: Bifează doar "Small" și "Medium"
   - **Oraș**: Alege "București"
   - **Doar cu email**: ✅
3. Sortare: Click pe "Reviews" (↑ ascending)
4. Rezultat: Service-uri mici/medii cu puține review-uri = posibil să fie noi sau subevaluate

### Exemplu 2: Top performers pe oraș

1. **Oraș**: "Cluj-Napoca"
2. **Size**: Toate
3. Sortare: Click pe "Rating" (↓ descending)
4. Export filtered CSV
5. Top 20 = potențiali early adopters (dacă au rating mare, au standarde înalte)

## 📊 Analiză Date în Google Sheets

### Dashboard Analytics

Creează un sheet separat cu formule:

```
// Sheet: Analytics

Total service-uri:
=COUNTA(Data!B2:B1000)

% cu email:
=COUNTIF(Data!D2:D1000, "<>") / COUNTA(Data!B2:B1000)

Top 5 orașe (count):
=QUERY(Data!H2:H1000, "SELECT H, COUNT(H) GROUP BY H ORDER BY COUNT(H) DESC LIMIT 5", 1)

Average rating per city:
=QUERY(Data!H2:I1000, "SELECT H, AVG(I) GROUP BY H ORDER BY AVG(I) DESC", 1)

Size distribution:
Small:  =COUNTIF(Data!C2:C1000, "small")
Medium: =COUNTIF(Data!C2:C1000, "medium")
Large:  =COUNTIF(Data!C2:C1000, "large")
```

### Pivot Table pentru Strategie

1. Data → Pivot table
2. Configurare:
   - **Rows**: City
   - **Columns**: Size
   - **Values**: COUNT of Name
   - **Filter**: Email is not empty

Rezultat: Matrix oraș × dimensiune pentru prioritizare

```
         | Small | Medium | Large | Total |
---------|-------|--------|-------|-------|
București|   45  |   32   |   18  |  95   |
Cluj     |   28  |   19   |   12  |  59   |
...
```

**Insight**: București LARGE (18) = highest priority targets

## 🚀 Automatizare Email (Post-MVP)

### Opțiune 1: Google Sheets + Gmail Script

**Apps Script** (Tools → Script editor):

```javascript
function sendEmails() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Data');
  const data = sheet.getDataRange().getValues();

  // Skip header
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    const name = row[1];    // Coloana B
    const email = row[3];   // Coloana D
    const city = row[7];    // Coloana H
    const rating = row[8];  // Coloana I

    // Skip dacă nu are email sau deja trimis
    if (!email || row[12]) continue;  // Coloana M = "Email Sent"

    const subject = `Recuperare RCA - Parteneriat ${city}`;
    const body = `
      Bună ziua,

      Am observat că ${name} are un rating excelent de ${rating} stele.

      [REST OF TEMPLATE]
    `;

    GmailApp.sendEmail(email, subject, body);

    // Marchează ca trimis
    sheet.getRange(i + 1, 13).setValue('Sent ' + new Date().toISOString());

    // Rate limiting
    Utilities.sleep(2000);  // 2s între emailuri
  }
}
```

**Trigger**: Tools → Script editor → Triggers → Add trigger → Time-driven

### Opțiune 2: Python + SendGrid

```python
import csv
import sendgrid
from sendgrid.helpers.mail import Mail

sg = sendgrid.SendGridAPIClient(api_key='YOUR_API_KEY')

with open('data/services.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['email'] or row['size'] != 'large':
            continue

        message = Mail(
            from_email='your@email.com',
            to_emails=row['email'],
            subject=f"Recuperare RCA - Parteneriat {row['city']}",
            html_content=f"""
                <p>Bună ziua,</p>
                <p>Am observat că {row['name']} are un rating excelent...</p>
            """
        )

        response = sg.send(message)
        print(f"Sent to {row['name']}: {response.status_code}")
```

## 📈 Tracking Conversii

### Google Sheets Tracker

Adaugă coloane în dreapta CSV-ului importat:

```
| ... | Email Sent | Opened | Replied | Meeting Scheduled | Converted | Notes |
|-----|------------|--------|---------|-------------------|-----------|-------|
```

**Formule utile**:

```
// Conversion rate
=COUNTIF(P:P, "Yes") / COUNTIF(M:M, "Sent*")

// Average time to reply
=AVERAGEIF(O:O, "Yes", Q:Q)  // Coloana Q = days since sent

// Best performing city
=QUERY(H2:P1000, "SELECT H, COUNT(P) WHERE P='Yes' GROUP BY H ORDER BY COUNT(P) DESC LIMIT 1", 0)
```

## 🎯 Best Practices

### DO ✅

1. **Personalizează emailurile**:
   - Folosește numele service-ului
   - Menționează rating-ul/reviews (dacă e mare)
   - Referă orașul pentru relevață locală

2. **Segmentare inteligentă**:
   - LARGE = pitch premium service
   - MEDIUM = pitch value pentru growth
   - SMALL = pitch entry-level cu onboarding simplificat

3. **Rate limiting**:
   - Max 50 emailuri/zi pentru început
   - Crește treptat dacă reply rate e bun (>5%)

4. **Tracking**:
   - UTM parameters în linkuri: `?utm_source=scraper&utm_medium=email&utm_campaign=feb2026`
   - Track open/click cu tool (SendGrid, Mailchimp)

5. **Follow-up**:
   - +3 zile: Reminder dacă nu a răspuns
   - +7 zile: Ultimul follow-up cu scarcity ("ultima săptămână discount")

### DON'T ❌

1. **Mass spam**: Nu trimite 500 emailuri odată
   - Risc: Gmail/Outlook te blochează ca spam
   - Soluție: 50/zi max, warm-up gradual

2. **Generic templates**: Nu folosi "Bună ziua, Stimată echipă"
   - Personalizează cu nume service

3. **Ignore opt-outs**: Respectă ÎNTOTDEAUNA cereri STOP
   - Legal requirement + reputație

4. **Neglijează GDPR**:
   - Include sursa datelor în email
   - Oferă opțiune dezabonare

5. **Target greșit**:
   - Nu trimite la service-uri fără review-uri (posibil închise/inactive)

## 📞 Cold Calling Script Avansat

### Opening (primele 10 secunde)

```
"Bună ziua, [NUMELE CONTACTULUI - dacă știi] / echipa de la [SERVICE]!

Numele meu este [NUME] de la [COMPANIA]. Suntem specializați în
recuperarea creanțelor RCA și colaborăm cu service-uri auto din
[ORAȘ] pentru a crește veniturile lor cu 15-25%.

Aveți 2 minute acum sau preferați să vă sun mâine la o oră convenabilă?"
```

### Qualification Questions

```
1. "Câte dosare RCA aproximativ aveți lunar?"
   → Evaluare volum potențial

2. "Momentan cum gestionați procesul de recuperare? Intern sau externalizat?"
   → Identifică competiție

3. "Cât timp în medie vă ia să recuperați banii de la asigurător?"
   → Pain point: dacă > 30 zile, ai leverage
```

### Objection Handling

**"Nu ne interesează"**
→ "Înțeleg perfect. Pot să vă întreb totuși - este pentru că aveți deja
un sistem care funcționează bine sau pentru că nu e o prioritate acum?"

**"Trimiteți un email"**
→ "Cu plăcere! Ca să fie relevant pentru dumneavoastră, puteți să-mi
spuneți pe scurt care e principala provocare cu dosarele RCA acum?"

**"Nu avem buget"**
→ "Exact de aceea am sunat - lucrăm pe bază de success fee, adică plătiți
doar dacă recuperăm banii. Zero risc pentru dumneavoastră."

## 🔄 Re-scraping Strategy

### Când să re-scrapezi

- **Lunar**: Pentru dataset complet fresh
- **Săptămânal**: Pentru tracking service-uri noi (compară id-uri)
- **On-demand**: După campanii (remove converted ones)

### Differential Scraping

```python
# În scrape_services.py, adaugă:

def load_existing_ids():
    if not os.path.exists('data/services.csv'):
        return set()
    with open('data/services.csv', 'r') as f:
        reader = csv.DictReader(f)
        return {row['id'] for row in reader}

def main():
    existing_ids = load_existing_ids()

    # ... în loop:
    if place_id in existing_ids:
        print(f"  [SKIP] {name} - already in database")
        continue
```

**Beneficiu**: Update doar cu service-uri noi = economisești API calls

---

**Pro tip**: Începe cu 1 oraș (București), testează procesul end-to-end
(scrape → email → track conversii), apoi scalează la toate orașele!
