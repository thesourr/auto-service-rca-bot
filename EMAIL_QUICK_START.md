# 📧 Email Quick Start - Start în 5 Minute

## 🎯 Pași Rapizi

### 1. Creează GitHub Token (2 min)

**Link**: https://github.com/settings/tokens

1. Click **"Generate new token (classic)"**
2. **Note**: `Email Bot`
3. **Scopes**: Bifează doar `repo`
4. Click **"Generate token"**
5. **COPIAZĂ token-ul** (începe cu `ghp_...`)

---

### 2. Adaugă Token în Browser (1 min)

1. **Deschide dashboard**: https://thesourr.github.io/auto-service-rca-bot/

2. **Apasă F12** (deschide console)

3. **Rulează** (înlocuiește `YOUR_TOKEN` cu token-ul tău):
   ```javascript
   localStorage.setItem('github_token', 'ghp_YOUR_TOKEN_HERE')
   ```

4. **Refresh pagina** (F5)

---

### 3. Test Email (2 min)

1. **Click** butonul verde: 🧪 **Trimite Email de Test**

2. **Confirmă** în dialog

3. **Așteaptă 2-3 minute**

4. **Verifică inbox**: ionescuionut18@gmail.com

5. **Verifică logs**: https://github.com/thesourr/auto-service-rca-bot/actions

---

## ✅ După Setup

### Cum Trimiți Email-uri:

1. **Selectează service-uri** (checkboxes în tabel)
2. **Click** 📨 **"Trimite Email la Selected"**
3. **Confirmă**
4. **Așteaptă 2-3 minute**
5. **Vezi rezultate** în GitHub Actions

---

## 📊 Detalii Email

**Subiect**: Propunere Colaborare - Recuperare Costuri Reparații Auto RCA

**De la**: Ionuț Ionescu <ionut@ionesculaw.ro>

**Template**: Email HTML profesional cu propunere de colaborare

**Rate Limit**: 20 email-uri per rulare (cu delay 2 sec între fiecare)

---

## 🔗 Link-uri Utile

| Link | Descriere |
|------|-----------|
| [Dashboard](https://thesourr.github.io/auto-service-rca-bot/) | Dashboard principal |
| [GitHub Tokens](https://github.com/settings/tokens) | Creează token |
| [Actions](https://github.com/thesourr/auto-service-rca-bot/actions) | Vezi logs email-uri |
| [EMAIL_SETUP.md](EMAIL_SETUP.md) | Ghid complet detaliat |

---

**Gata în 5 minute!** 🚀
