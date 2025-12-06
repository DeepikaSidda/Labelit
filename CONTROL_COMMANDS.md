# 🎮 Labelit Control Commands

Quick reference for controlling Labelit auto-start on Windows.

---

## ▶️ Start Labelit Now

```powershell
Start-ScheduledTask -TaskName "Labelit Screenshot Renamer"
```

Starts Labelit immediately without rebooting.

---

## 🛑 Stop Labelit Now

```powershell
Stop-ScheduledTask -TaskName "Labelit Screenshot Renamer"
```

Stops Labelit temporarily. It will auto-start again on next boot.

---

## ✅ Enable Auto-Start

```powershell
Enable-ScheduledTask -TaskName "Labelit Screenshot Renamer"
```

Enables auto-start. Labelit will start automatically when you log in.

---

## 🚫 Disable Auto-Start

```powershell
Disable-ScheduledTask -TaskName "Labelit Screenshot Renamer"
```

Disables auto-start. Labelit will NOT start automatically on boot.

---

## 📊 Check Status

```powershell
Get-ScheduledTask -TaskName "Labelit Screenshot Renamer" | Select-Object TaskName, State
```

Shows current status:
- **Ready** = Enabled, not running
- **Running** = Enabled and currently running
- **Disabled** = Auto-start is disabled

---

## ❌ Remove Auto-Start Completely

```powershell
Unregister-ScheduledTask -TaskName "Labelit Screenshot Renamer" -Confirm:$false
```

Removes the scheduled task completely. To set it up again, run:

```powershell
powershell -ExecutionPolicy Bypass -File setup_task_scheduler.ps1
```

---

## 🔄 Quick Reference

| What You Want | Command |
|---------------|---------|
| Start now | `Start-ScheduledTask -TaskName "Labelit Screenshot Renamer"` |
| Stop now | `Stop-ScheduledTask -TaskName "Labelit Screenshot Renamer"` |
| Enable auto-start | `Enable-ScheduledTask -TaskName "Labelit Screenshot Renamer"` |
| Disable auto-start | `Disable-ScheduledTask -TaskName "Labelit Screenshot Renamer"` |
| Check status | `Get-ScheduledTask -TaskName "Labelit Screenshot Renamer"` |
| Remove completely | `Unregister-ScheduledTask -TaskName "Labelit Screenshot Renamer" -Confirm:$false` |

---

## 💡 Understanding Stop vs Disable

### Stop (Temporary)
- Stops Labelit right now
- Will auto-start again on next boot
- Use when: You want to pause it temporarily

### Disable (Permanent)
- Stops Labelit AND prevents auto-start
- Will NOT start on boot until you enable it
- Use when: You want to turn off auto-start completely

---

## 📝 How to Use

1. Open PowerShell
2. Copy and paste the command you need
3. Press Enter

That's it!
