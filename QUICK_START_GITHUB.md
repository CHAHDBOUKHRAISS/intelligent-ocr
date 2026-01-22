# Quick Start: Upload to GitHub (5 Simple Steps)

## ✅ Step 1: Open PowerShell in Your Project Folder

```powershell
cd "C:\Users\Chahd Boukhriss\OneDrive\Desktop\OCR_INTELLIGENT"
```

---

## ✅ Step 2: Initialize Git and Make First Commit

Copy and paste these commands **one by one**:

```powershell
git init
```

```powershell
git add .
```

```powershell
git commit -m "Initial commit: Intelligent OCR system"
```

---

## ✅ Step 3: Create GitHub Repository

1. Open your browser
2. Go to: **https://github.com**
3. Log in
4. Click the **"+"** button (top right)
5. Click **"New repository"**
6. Fill in:
   - **Name**: `intelligent-ocr`
   - **Description**: `OCR system for document processing`
   - **Visibility**: Choose **Public** or **Private**
   - **DO NOT** check any boxes (README, .gitignore, license)
7. Click **"Create repository"**
8. **Copy the repository URL** (looks like: `https://github.com/YOUR_USERNAME/intelligent-ocr.git`)

---

## ✅ Step 4: Connect and Push to GitHub

Back in PowerShell, paste these commands (replace `YOUR_USERNAME` with your actual GitHub username):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/intelligent-ocr.git
```

```powershell
git branch -M main
```

```powershell
git push -u origin main
```

**When asked for password:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (see below)

---

## ✅ Step 5: Create Personal Access Token (if needed)

If `git push` asks for a password:

1. Go to: **https://github.com/settings/tokens**
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name it: `Git Upload`
4. Check the box: **`repo`** (full control)
5. Click **"Generate token"**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when `git push` asks

---

## ✅ DONE! 

Go to your GitHub repository page and refresh. You should see all your files! 🎉

---

## Need Help?

**Problem: "Repository not found"**
→ Check your repository URL is correct

**Problem: "Permission denied"**
→ Use Personal Access Token (Step 5)

**Problem: "venv/ is being uploaded"**
→ Make sure `.gitignore` file exists in your project root

---

## That's It!

Your code is now on GitHub! 🚀
