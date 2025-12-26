# Fix Server Issues - Quick Solutions

## Problem Analysis

You have two issues:

1. **Already in frontend directory** - You're already at `/mnt/d/python-learning/Serverless-SPA-CDK/frontend`, so `cd frontend` fails
2. **Port 8080 is in use** - Another process is using port 8080

## Solution Options

### Option 1: Use a Different Port (Easiest)

Since you're already in the frontend directory, just run:

```bash
python3 -m http.server 8000
```

Or if 8000 is also busy, try 3000:

```bash
python3 -m http.server 3000
```

Then open in browser: `http://localhost:8000` or `http://localhost:3000`

---

### Option 2: Find and Kill Process Using Port 8080

**Step 1: Find what's using port 8080**
```bash
sudo lsof -i :8080
```

Or:
```bash
sudo netstat -tulpn | grep 8080
```

**Step 2: Kill the process**
```bash
# Replace PID with the actual process ID from step 1
kill -9 PID
```

**Step 3: Start your server**
```bash
python3 -m http.server 8080
```

---

### Option 3: Check Current Directory and Start Server

**Verify you're in the right place:**
```bash
pwd
ls -la
```

You should see `index.html` in the listing.

**If you're in the right directory, just start server:**
```bash
python3 -m http.server 8000
```

**If you're NOT in frontend directory:**
```bash
cd /mnt/d/python-learning/Serverless-SPA-CDK/frontend
python3 -m http.server 8000
```

---

## Quick Fix Commands (Copy-Paste)

**If you're already in frontend folder (most likely):**
```bash
python3 -m http.server 8000
```

**If you need to navigate first:**
```bash
cd /mnt/d/python-learning/Serverless-SPA-CDK/frontend
python3 -m http.server 8000
```

**To check if server is running:**
```bash
curl http://localhost:8000
```

**To stop the server:**
Press `Ctrl + C` in the terminal where server is running

---

## Verify It's Working

1. Start server: `python3 -m http.server 8000`
2. Open browser: `http://localhost:8000`
3. You should see your website!

---

## Common Port Conflicts

If multiple ports are busy, try these ports in order:
- 8000
- 3000
- 5000
- 9000
- 8888

Example:
```bash
python3 -m http.server 3000
```
Then access: `http://localhost:3000`

