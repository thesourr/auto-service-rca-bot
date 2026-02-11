# 🔒 Security Update - ACTION REQUIRED

**Date**: 2026-02-11
**Status**: ⚠️ URGENT - API Key Compromised

---

## ⚠️ PROBLEMA

API key-ul tău Google Maps a fost expus accidental în git history:
```
Key exposed: YOUR_GOOGLE_MAPS_API_KEY
```

Chiar dacă am șters key-ul din fișierele actuale, oricine poate vedea commit-urile vechi:
```bash
git log --all --patch | grep "AIza"
```

**Repository este PUBLIC** → Key-ul poate fi folosit de oricine!

---

## ✅ CE AM FĂCUT DEJA

1. ✅ Șters API key din START_HERE.md (commit actual)
2. ✅ Adăugat `.claude/` în `.gitignore`
3. ✅ Repository făcut PUBLIC (pentru dashboard gratuit)
4. ✅ API key în GitHub Secrets (sigur)

---

## 🚨 CE TREBUIE SĂ FACI TU (URGENT!)

### Step 1: Invalidate Old API Key (5 min)

1. **Mergi la Google Cloud Console**:
   https://console.cloud.google.com/apis/credentials

2. **Găsește API key-ul expus**:
   - Caută în listă: key care începe cu `AIzaSyDNzr7V...`
   - Sau click pe toate key-urile până găsești pe cel potrivit

3. **DELETE key-ul**:
   - Click pe key → Action menu (⋮) → **Delete**
   - Confirmă ștergerea

### Step 2: Generează API Key NOU (5 min)

1. **În același Google Cloud Console**:
   - Click **+ CREATE CREDENTIALS**
   - Select **API key**

2. **Restricționează noul key** (IMPORTANT!):
   - Click pe noul key → **Edit API key**
   - **API restrictions**: Select APIs → **Places API** (DOAR asta!)
   - **Application restrictions**: None (pentru GitHub Actions)
   - **Save**

3. **COPIAZĂ noul key** (începe cu `AIza...`)

### Step 3: Actualizează GitHub Secret (2 min)

**Opțiunea A - CLI (rapid)**:
```bash
gh secret set GOOGLE_MAPS_API_KEY --body "NEW_KEY_HERE" --repo thesourr/auto-service-rca-bot
```

**Opțiunea B - Web UI**:
1. https://github.com/thesourr/auto-service-rca-bot/settings/secrets/actions
2. Click pe `GOOGLE_MAPS_API_KEY` → **Update secret**
3. Paste noul key
4. **Update secret**

### Step 4: Verificare (1 min)

1. **Trigger manual GitHub Actions** (pentru a testa noul key):
   ```bash
   gh workflow run scrape.yml --repo thesourr/auto-service-rca-bot
   ```

2. **Check status**:
   ```bash
   gh run watch --repo thesourr/auto-service-rca-bot
   ```

3. **Ar trebui să fie SUCCESS** ✅

---

## 🔐 SIGURANȚA NOULUI KEY

După ce actualizezi:

✅ Noul API key este DOAR în GitHub Secrets (encrypted)
✅ NU este în git history
✅ NU este în fișiere publice
✅ .claude/ este ignorat (nu se mai push-uie)

---

## 📊 STATUS ACTUAL

### Repository
- **Visibility**: PUBLIC ✅
- **URL**: https://github.com/thesourr/auto-service-rca-bot
- **Dashboard**: https://thesourr.github.io/auto-service-rca-bot/

### Dashboard Status
- ✅ FUNCȚIONEAZĂ acum (repository public + XML disponibil)
- ✅ Afișează 20 service-uri din Cluj-Napoca (date test)
- 🟡 Va fi actualizat cu dataset complet când Actions se termină (~10 min)

### GitHub Actions
- 🟡 IN PROGRESS (7 minute până acum, mai are ~8-13 min)
- ✅ Va scrape toate cele 17 orașe
- ✅ Va crea dataset complet (400-600 service-uri)

### API Key
- ⚠️ VECHI: Expus în git history → TREBUIE INVALIDAT!
- ✅ NOU: După ce îl generezi, va fi 100% sigur

---

## ⏰ TIMELINE

**ACUM (URGENT - 10 min)**:
1. Invalidate old key (Google Cloud)
2. Generate new key
3. Update GitHub Secret

**APOI (15 min)**:
1. Așteaptă ca GitHub Actions să se termine
2. Verifică dashboard: https://thesourr.github.io/auto-service-rca-bot/
3. Confirmă că datele noi sunt încărcate

**DUPĂ**:
1. Importă CSV în Google Sheets
2. Folosește datele pentru campanii email
3. Profită de sistemul automat! 🎉

---

## 🛡️ PREVENȚIE VIITOARE

Pentru a evita expunerea key-urilor în viitor:

1. **NICIODATĂ** nu pune API keys în fișiere tracked de git
2. Folosește DOAR environment variables:
   ```bash
   export API_KEY="secret"
   ```
3. Verifică `.gitignore` ÎNAINTE de commit:
   - `.env` files
   - `.claude/` directory
   - `*.local.json` files

4. Tool util pentru check:
   ```bash
   git diff --cached | grep -i "api.*key"
   ```

---

## 📞 SUPORT

**Probleme cu invalidarea key-ului?**
- Google Cloud Support: https://cloud.google.com/support

**GitHub Actions fail după update?**
- Verifică că noul key are Places API enabled
- Verifică că key-ul e corect copiat (fără spații)

**Dashboard încă nu funcționează?**
- Wait 2-3 minute pentru cache refresh
- Hard refresh browser: Ctrl+Shift+R (Windows) sau Cmd+Shift+R (Mac)

---

## ✅ CHECKLIST

- [ ] Delete old API key (Google Cloud Console)
- [ ] Generate new API key
- [ ] Restrict new key (Places API only)
- [ ] Update GitHub Secret
- [ ] Test new key (trigger Actions)
- [ ] Verify dashboard works
- [ ] Confirm scraping succeeds

**Timp estimat**: ~12 minute

---

**Status**: ⚠️ AȘTEAPTĂ ACȚIUNE

**Next step**: Invalidate old API key NOW!

---

Built: 2026-02-11
Security priority: CRITICAL
Repository: https://github.com/thesourr/auto-service-rca-bot
