# 📧 Email Setup - Configurare Trimitere Email-uri

**Status**: ⚠️ NECESITĂ SETUP FINAL (5 minute)
**Data**: 2026-02-11

---

## ✅ Ce Am Implementat Deja

### 1. ✅ Script Python pentru Trimitere Email-uri
- **Fișier**: `send_emails.py`
- **Funcționalitate**:
  - Citește din `data/email_queue.json`
  - Trimite 20 email-uri per rulare
  - Salvează istoric în `data/email_sent.json`
  - Read receipts activate (header-e email)
  - Template profesional (HTML + Plain Text)

### 2. ✅ GitHub Actions Workflow
- **Fișier**: `.github/workflows/send_emails.yml`
- **Trigger**: Automat când se modifică `data/email_queue.json`
- **Proces**:
  1. Detectează commit nou în `email_queue.json`
  2. Rulează `send_emails.py`
  3. Trimite maximum 20 email-uri
  4. Salvează rezultatele
  5. Commit automat cu status

### 3. ✅ Dashboard Updates
- **Checkboxes**: Pe fiecare rând (doar pentru service-uri cu email)
- **Select All**: Checkbox în header pentru selecție rapidă
- **Butoane**:
  - 🧪 **Trimite Email de Test** → trimite la ionescuionut18@gmail.com
  - 📨 **Trimite Email la Selected** → trimite la service-uri selectate
  - ✖ **Deselectează Tot** → resetează selecția
- **Counter**: Afișează câte service-uri sunt selectate

### 4. ✅ SMTP Configuration
- **Provider**: Hostinger
- **Host**: smtp.hostinger.com
- **Port**: 465 (SSL)
- **Email**: ionut@ionesculaw.ro
- **Password**: [Salvat în GitHub Secrets] ✅

---

## 🚨 CE TREBUIE SĂ FACI TU (5 MINUTE)

### Pas 1: Creează GitHub Personal Access Token (3 min)

Dashboard-ul trebuie să poată face commit pe GitHub pentru a adăuga email-urile în queue.

**1. Deschide GitHub Settings**:
```
https://github.com/settings/tokens
```

**2. Click "Generate new token" → "Generate new token (classic)"**

**3. Setări token**:
- **Note**: `Auto Service Email Bot`
- **Expiration**: `No expiration` (sau 90 days)
- **Scopes** (bifează DOAR acestea):
  - ☑️ `repo` (Full control of private repositories)
    - Asta include: repo:status, repo_deployment, public_repo, repo:invite, security_events

**4. Click "Generate token"**

**5. COPIAZĂ token-ul** (începe cu `ghp_...`)
   - ⚠️ **IMPORTANT**: Salvează-l undeva sigur, nu vei mai putea să-l vezi!

---

### Pas 2: Adaugă Token în Browser (1 min)

**1. Deschide Dashboard-ul**:
```
https://thesourr.github.io/auto-service-rca-bot/
```

**2. Deschide Browser Console**:
- **Chrome/Edge**: `F12` sau `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
- **Firefox**: `F12`
- Click pe tab-ul **Console**

**3. Rulează comanda** (înlocuiește `YOUR_TOKEN_HERE` cu token-ul tău):
```javascript
localStorage.setItem('github_token', 'ghp_YOUR_TOKEN_HERE')
```

**Exemplu**:
```javascript
localStorage.setItem('github_token', 'ghp_1A2B3C4D5E6F7G8H9I0J')
```

**4. Verifică că s-a salvat**:
```javascript
localStorage.getItem('github_token')
```

Ar trebui să vezi token-ul afișat.

---

### Pas 3: Test Email de Test (1 min)

**1. Refresh dashboard-ul** (F5)

**2. Click pe butonul verde**: 🧪 **Trimite Email de Test**

**3. Confirmă** în dialog

**4. Așteaptă 2-3 minute**

**5. Verifică inbox-ul**: `ionescuionut18@gmail.com`
   - Ar trebui să primești un email cu subiectul:
     **"Propunere Colaborare - Recuperare Costuri Reparații Auto RCA"**

**6. Verifică GitHub Actions**:
```
https://github.com/thesourr/auto-service-rca-bot/actions
```
- Ar trebui să vezi un workflow "Send Emails" în progres sau completat

---

## 📧 Template Email Implementat

### Subiect
```
Propunere Colaborare - Recuperare Costuri Reparații Auto RCA
```

### Conținut (HTML + Plain Text)

```
Bună ziua,

Vă contactez în numele firmei noastre de consultanță juridică specializată în
recuperarea costurilor de reparații auto pentru autovehiculele asigurate RCA.

Înțelegem că service-ul dumneavoastră deservește zilnic clienți care au fost
implicați în accidente auto cauzate de terți. În multe cazuri, acești clienți
nu știu că au dreptul legal de a recupera integral costurile reparațiilor
direct de la asigurătorul RCA al celui vinovat, fără a-și folosi propria
asigurare CASCO.

Propunem o colaborare prin care firma noastră se ocupă de:
• Recuperarea integrală a costurilor reparațiilor de la asigurătorul RCA
• Gestionarea completă a dosarului (fără efort din partea service-ului)
• Suport juridic complet pe toată durata procesului
• Comision atractiv pentru service-ul dumneavoastră la fiecare caz soluționat

Acest parteneriat vă oferă posibilitatea de a aduce un serviciu suplimentar
clienților dumneavoastră, crescând satisfacția acestora și generând venituri
adiționale pentru business-ul dumneavoastră.

Dacă sunteți interesat să discutăm detaliile acestei colaborări, vă rog să
răspundeți la acest email sau să mă contactați telefonic.

Cu stimă,
Ionuț Ionescu
Consultant Juridic
Email: ionut@ionesculaw.ro
Website: ionesculaw.ro
```

---

## 🎯 Cum Funcționează Sistemul

### Flow Complet:

1. **În Dashboard**:
   - Bifezi service-urile la care vrei să trimiți email
   - Click "Trimite Email la Selected"
   - Confirmi

2. **În Browser** (JavaScript):
   - Dashboard-ul creează `data/email_queue.json` cu lista de recipients
   - Face commit + push pe GitHub folosind Personal Access Token

3. **GitHub Actions** (automat, 10-30 secunde):
   - Detectează commit-ul în `email_queue.json`
   - Pornește workflow-ul `send_emails.yml`

4. **Script Python** (`send_emails.py`):
   - Citește queue-ul
   - Conectează la SMTP Hostinger
   - Trimite 20 email-uri (cu delay 2 sec între fiecare)
   - Salvează rezultatele în `email_sent.json`
   - Actualizează queue-ul (scoate primele 20)

5. **Rezultate**:
   - Email-uri trimise ✅
   - Istoric salvat în `data/email_sent.json`
   - Vezi logs în GitHub Actions

---

## 📊 Limite și Rate Limiting

### Email-uri per Rulare
- **Maximum**: 20 email-uri per rulare
- **Motivație**: Evită spam filters și protejează reputația email-ului

### Exemplu:
- Selectezi 50 service-uri
- Primul run: 20 email-uri trimise
- Ai rămas: 30 în queue
- Trigger manual al doilea run: încă 20 email-uri
- Ai rămas: 10 în queue
- Trigger manual al treilea run: ultimele 10 email-uri
- **Total**: 50 email-uri trimise în ~6-9 minute

### Delay între Email-uri
- **2 secunde** între fiecare email
- **Motivație**: Respectă best practices SMTP și evită throttling

---

## 🔧 Troubleshooting

### Eroare: "GitHub token lipsește!"
**Soluție**: Repetă Pasul 2 - adaugă token-ul în browser console

---

### Email-urile nu se trimit
**Verificări**:
1. Check GitHub Actions logs:
   ```
   https://github.com/thesourr/auto-service-rca-bot/actions
   ```
2. Verifică dacă workflow-ul "Send Emails" a rulat
3. Citește logs pentru erori SMTP

---

### Eroare SMTP authentication
**Cauză**: Parola email-ului Hostinger este greșită sau a expirat

**Soluție**:
1. Verifică parola în Hostinger panel
2. Actualizează secret în GitHub:
   ```bash
   gh secret set SMTP_PASSWORD --body "NEW_PASSWORD" --repo thesourr/auto-service-rca-bot
   ```

---

### Read Receipts nu funcționează
**Cauză**: Majoritatea clienților de email (Gmail, Outlook) ignoră header-ele de read receipt

**Soluție**: Read receipts sunt best-effort. Nu te baza 100% pe ele.

**Alternative**:
- Așteaptă răspunsuri la email
- Urmărește câte răspunsuri primești

---

## 📈 Monitoring

### Verifică Email-uri Trimise

**Fișier**: `data/email_sent.json`
```
https://raw.githubusercontent.com/thesourr/auto-service-rca-bot/main/data/email_sent.json
```

**Structură**:
```json
{
  "campaigns": [
    {
      "timestamp": "2026-02-11T12:00:00Z",
      "is_test": false,
      "total_sent": 20,
      "total_failed": 0,
      "results": [
        {
          "service_id": "ChIJ...",
          "email": "service@example.com",
          "name": "Service Auto XYZ",
          "status": "sent",
          "timestamp": "2026-02-11T12:01:23Z",
          "error": null
        },
        ...
      ]
    }
  ]
}
```

---

### GitHub Actions Logs

**URL**: https://github.com/thesourr/auto-service-rca-bot/actions

**Ce să cauți**:
- ✅ Workflow "Send Emails" cu status SUCCESS
- ❌ Dacă e FAILED, citește logs pentru erori

---

## ✅ Checklist Setup

- [ ] Generate GitHub Personal Access Token
- [ ] Adaugă token în browser console
- [ ] Test email de test (trimite la ionescuionut18@gmail.com)
- [ ] Verifică inbox pentru email de test
- [ ] Verifică GitHub Actions logs (success)
- [ ] Trimite email-uri reale la service-uri selectate
- [ ] Monitorizează `email_sent.json` pentru rezultate

---

## 🎉 După Setup

Când totul funcționează:

1. **Selectează service-uri** din dashboard (checkboxes)
2. **Click "Trimite Email la Selected"**
3. **Așteaptă 2-3 minute**
4. **Verifică logs** în GitHub Actions
5. **Vezi rezultate** în `email_sent.json`

**Succes!** 🚀

---

Built: 2026-02-11
Repository: https://github.com/thesourr/auto-service-rca-bot
Dashboard: https://thesourr.github.io/auto-service-rca-bot/
