# ⚡ Labelit - Quick Setup (5 Minutes)

**For people who want to get started FAST!**

---

## 1️⃣ Install (2 minutes)

```bash
# Clone or download the project
cd labelit

# Install
pip install -e .
```

---

## 2️⃣ AWS Setup (2 minutes)

### Get AWS Credentials:
1. Go to: https://console.aws.amazon.com/iam/
2. Security Credentials → Create access key
3. Save your Access Key ID and Secret Access Key

### Enable Bedrock:
1. Go to: https://console.aws.amazon.com/bedrock/
2. Region: **us-east-1**
3. Model access → Manage → Enable **Amazon Nova Lite**

### Configure:
```bash
aws configure
# Access Key ID: [paste]
# Secret Access Key: [paste]
# Region: us-east-1
# Format: json
```

---

## 3️⃣ Configure Labelit (1 minute)

```bash
# Create config
labelit setup

# Edit config (Windows)
notepad C:\Users\%USERNAME%\.labelit\config.yaml

# Edit config (Mac/Linux)
nano ~/.labelit/config.yaml
```

**Change this line:**
```yaml
monitored_folder: C:/Users/YourName/Pictures/Screenshots
```

**To YOUR screenshots folder:**
```yaml
monitored_folder: C:/Users/sidda/OneDrive/Pictures/Screenshots
```

Save and close.

---

## 4️⃣ Test It!

```bash
labelit start
```

Take a screenshot → Watch it get renamed!

Press `Ctrl + C` to stop.

---

## 5️⃣ Auto-Start (Windows Only)

```powershell
powershell -ExecutionPolicy Bypass -File setup_task_scheduler.ps1
```

Done! Labelit will now start automatically.

---

## 📝 Files to Change

### Only 1 file needs editing:

**File:** `~/.labelit/config.yaml`

**Line to change:**
```yaml
monitored_folder: YOUR_SCREENSHOTS_FOLDER_HERE
```

**Common paths:**
- Windows: `C:/Users/YourName/OneDrive/Pictures/Screenshots`
- Mac: `/Users/YourName/Desktop`
- Linux: `/home/YourName/Pictures`

---

## 🔍 Find Your Screenshots Folder

**Windows:**
1. Press `Win + Shift + S`
2. Take a screenshot
3. Right-click file → Properties
4. Copy the "Location" path

**Mac:**
1. Press `Cmd + Shift + 4`
2. Take a screenshot
3. Right-click file → Get Info
4. Copy the "Where" path

**Linux:**
1. Take a screenshot
2. Check where it saved
3. Use that path

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Labelit installed (`pip install -e .`)
- [ ] AWS credentials configured (`aws configure`)
- [ ] Bedrock model access enabled (Amazon Nova Lite)
- [ ] Config file edited (`~/.labelit/config.yaml`)
- [ ] `monitored_folder` points to YOUR screenshots folder
- [ ] Tested with `labelit start`
- [ ] Auto-start configured (Windows)

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "AWS credentials not found" | Run `aws configure` |
| "Monitored folder does not exist" | Check path in `config.yaml` |
| "Cannot connect to AWS" | Enable Bedrock model access |
| Screenshots not renamed | Check if Labelit is running |
| Auto-start not working | Run `setup_task_scheduler.ps1` again |

---

## 📞 Need Help?

**Check logs:**
```bash
# Windows
type C:\Users\%USERNAME%\.labelit\labelit.log

# Mac/Linux
cat ~/.labelit/labelit.log
```

**Full guide:** See `INSTALLATION_GUIDE.md`

---

## 🎉 That's It!

You're done! Every screenshot will now be automatically renamed.

**Cost:** ~$0.0002 per screenshot (less than 1 cent per 50 screenshots)

**Enjoy!** 📸✨
