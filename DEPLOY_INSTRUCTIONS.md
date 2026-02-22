# Deploy ESPP Modeler to GitHub Pages

## Option A: Drag-and-Drop (Fastest — ~60 seconds)

1. Go to **https://github.com/new** and create a new repository
   - Name: `espp-modeler` (or whatever you prefer)
   - Set to **Public** (required for free GitHub Pages)
   - Click **Create repository**

2. On the empty repo page, click **"uploading an existing file"**

3. Drag both files from the `espp-modeler-site` folder:
   - `index.html`
   - `README.md`

4. Click **Commit changes**

5. Go to **Settings → Pages** (left sidebar)
   - Source: **Deploy from a branch**
   - Branch: **main** / **/ (root)**
   - Click **Save**

6. Wait ~1 minute. Your site will be live at:
   **https://YOUR-USERNAME.github.io/espp-modeler/**

---

## Option B: Command Line (if you have git + gh CLI)

```bash
cd espp-modeler-site
git init
git add .
git commit -m "Initial commit: ESPP Plan Modeler"
gh repo create espp-modeler --public --source=. --push
gh api repos/{owner}/espp-modeler/pages -f source.branch=main -f source.path=/
```

Your site will be live within ~1 minute at:
**https://YOUR-USERNAME.github.io/espp-modeler/**
