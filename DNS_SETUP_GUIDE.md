# DNS Records Setup for 247performance.app
## Configure at Porkbun.com → DNS Management

---

## STEP 1: Zoho Verification (Do This First)

1. Go to [Zoho Mail](https://www.zoho.com/mail/) and sign up
2. Add domain: 247performance.app
3. Zoho will give you a verification code
4. Add this record at Porkbun:

**TXT Record - Verification:**
```
Type: TXT
Host: @ (or leave blank)
Value: zoho-verification=zb[YOUR_CODE_HERE].zmverify.zoho.com
TTL: 600
```

Wait for verification (5-30 minutes), then proceed to Step 2.

---

## STEP 2: MX Records (Mail Routing)

Add these THREE records at Porkbun in this exact order:

**MX Record 1:**
```
Type: MX
Host: @ (or leave blank)
Value: mx.zoho.com
Priority: 10
TTL: 600
```

**MX Record 2:**
```
Type: MX
Host: @ (or leave blank)
Value: mx2.zoho.com
Priority: 20
TTL: 600
```

**MX Record 3:**
```
Type: MX
Host: @ (or leave blank)
Value: mx3.zoho.com
Priority: 50
TTL: 600
```

---

## STEP 3: SPF Record (Sender Policy Framework)

Prevents email spoofing. Add this TXT record:

**TXT Record - SPF:**
```
Type: TXT
Host: @ (or leave blank)
Value: v=spf1 include:zoho.com ~all
TTL: 600
```

### SPF Explained:
- `v=spf1` = SPF version 1
- `include:zoho.com` = Allow Zoho servers to send email
- `~all` = Soft fail for other servers (marks as suspicious but doesn't reject)

---

## STEP 4: DKIM Record (Email Authentication)

1. In Zoho Mail, go to **Control Panel** → **Domains** → **247performance.app**
2. Click **Email Configuration** → **DKIM**
3. Zoho will generate a DKIM key - copy the values

**TXT Record - DKIM:**
```
Type: TXT
Host: zmail._domainkey
Value: [COPY FROM ZOHO - looks like:]
        k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC...
TTL: 600
```

### DKIM Explained:
- Cryptographically signs your emails
- Receiving servers verify the signature
- Proves the email wasn't modified in transit

---

## STEP 5: DMARC Record (Email Security Policy)

Tells receiving servers what to do with emails that fail SPF/DKIM:

**TXT Record - DMARC:**
```
Type: TXT
Host: _dmarc
Value: v=DMARC1; p=none; rua=mailto:admin@247performance.app
TTL: 600
```

### DMARC Explained:
- `v=DMARC1` = DMARC version 1
- `p=none` = Monitor mode (don't reject, just report)
- `rua=mailto:admin@247performance.app` = Send reports here

### DMARC Policies (Change p= value later):
- `p=none` = Monitor only (recommended for setup)
- `p=quarantine` = Send suspicious emails to spam
- `p=reject` = Reject failed emails (strictest - use after testing)

---

## STEP 6: Verify Configuration

### Using Command Line:

**Check MX Records:**
```powershell
nslookup -type=MX 247performance.app
```

**Check SPF:**
```powershell
nslookup -type=TXT 247performance.app
```

**Check DKIM:**
```powershell
nslookup -type=TXT zmail._domainkey.247performance.app
```

**Check DMARC:**
```powershell
nslookup -type=TXT _dmarc.247performance.app
```

### Using Online Tools:
- **MX Toolbox**: https://mxtoolbox.com/SuperTool.aspx?action=mx:247performance.app
- **DKIM Check**: https://mxtoolbox.com/dkim.aspx
- **DMARC Check**: https://mxtoolbox.com/DMARC.aspx
- **SPF Check**: https://mxtoolbox.com/spf.aspx

---

## Complete DNS Records Summary

Once configured, your Porkbun DNS should have these records:

| Type | Host | Value | Priority | Purpose |
|------|------|-------|----------|---------|
| TXT | @ | zoho-verification=... | - | Zoho domain verification |
| MX | @ | mx.zoho.com | 10 | Primary mail server |
| MX | @ | mx2.zoho.com | 20 | Backup mail server |
| MX | @ | mx3.zoho.com | 50 | Tertiary mail server |
| TXT | @ | v=spf1 include:zoho.com ~all | - | SPF policy |
| TXT | zmail._domainkey | k=rsa; p=... | - | DKIM signature |
| TXT | _dmarc | v=DMARC1; p=none; rua=mailto:admin@247performance.app | - | DMARC policy |

---

## Propagation Time

- **DNS propagation:** 15 minutes to 48 hours (usually 1-2 hours)
- **Check status:** https://dnschecker.org

---

## Test Email Delivery

After DNS propagates (wait at least 1 hour):

1. In Zoho, create a test email account: test@247performance.app
2. Send an email to your personal email
3. Check email headers to verify SPF/DKIM passed

### Email Header Checks:
```
Received-SPF: pass
DKIM-Signature: verified
DMARC: pass
```

---

## Troubleshooting

### Emails not receiving:
- Check MX records are correct
- Verify DNS propagation completed
- Check Zoho mail server status

### Emails going to spam:
- Verify SPF record is correct
- Ensure DKIM is properly configured
- Start with DMARC p=none, monitor for issues

### DKIM not verifying:
- Copy the entire DKIM value without line breaks
- Some DNS providers require removing quotes
- Wait for full DNS propagation

---

## Next Steps After Setup

1. **Create email accounts in Zoho:**
   - admin@247performance.app
   - support@247performance.app
   - noreply@247performance.app

2. **Configure Django to send emails:**
   Update `.env`:
   ```env
   EMAIL_HOST=smtp.zoho.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=noreply@247performance.app
   EMAIL_HOST_PASSWORD=your_zoho_password
   ```

3. **Monitor DMARC reports:**
   - Check admin@247performance.app for XML reports
   - After 2 weeks of monitoring, change to p=quarantine
   - After another 2 weeks, consider p=reject

---

## Security Tips

- **Never share** DKIM private keys
- **Enable 2FA** on Zoho Mail admin account
- **Use app passwords** for Django email (not main password)
- **Review DMARC reports** monthly
- **Update SPF** if you add new email services (SendGrid, Mailchimp, etc.)

---

## Porkbun Login Steps

1. Go to: https://porkbun.com/account/login
2. Login with your credentials
3. Click on **247performance.app**
4. Click **DNS** tab
5. Add each record using "Add" button
6. Click "Save" after each record

---

*Ready to configure? Start with Step 1 (Zoho signup) and work through each step in order.*
