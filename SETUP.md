# Setup Guide: Getting Started with Static Assets Template

This guide will walk you through setting up this template repository for your own GitHub account and deploying it to GitHub Pages.

## Quick Setup (Recommended)

**Use the interactive setup script** to automate the configuration:

```bash
# Run the interactive setup script
python scripts/setup.py

# Or if you prefer:
python3 scripts/setup.py
```

The script will:
- ✅ Prompt for your GitHub username and repository name
- ✅ Automatically update `config.toml` with the correct base URL
- ✅ Provide step-by-step instructions for the remaining setup
- ✅ Optionally run git commands for you

## Manual Setup

If you prefer to set up manually, follow the steps below.

## Prerequisites

- A GitHub account
- Git installed on your local machine
- Basic familiarity with command line
- Python 3.6+ (for the setup script, optional)

## Step-by-Step Setup

### Step 1: Clone the Template Repository

```bash
# Clone this template repository
git clone https://github.com/youyoubilly/static-assets-template.git my-assets-repo
cd my-assets-repo
```

### Step 2: Remove Template Git History and Initialize New Repository

```bash
# Remove the template's git history
rm -rf .git

# Initialize a new git repository
git init

# Add all files
git add .

# Make your initial commit
git commit -m "Initial commit from static-assets-template"
```

### Step 3: Create a New Repository on GitHub

1. Go to https://github.com/new
2. **Repository name**: Choose a name (e.g., `my-assets`, `static-assets`, `assets-repo`)
   - ⚠️ **Important**: Remember this name, you'll need it for the next step
3. **Description**: (Optional) Add a description
4. **Visibility**: Choose Public (required for free GitHub Pages) or Private
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

### Step 4: Configure Your Local Repository

Update `config.toml` with your GitHub Pages URL:

```bash
# Edit config.toml (use your preferred editor)
# Replace <your-username> with your GitHub username
# Replace <your-repo-name> with the repository name you created in Step 3
```

Edit `config.toml`:

```toml
[repository]
# Base URL for generated asset links
# Format: https://<your-username>.github.io/<your-repo-name>
base_url = "https://<your-username>.github.io/<your-repo-name>"

# GitHub Pages domain (for CNAME)
# Leave empty if using default github.io domain
domain = ""

[build]
# Directories to process (already configured)
image_dirs = ["images"]
css_dirs = ["css"]
js_dirs = ["js"]
data_dirs = ["data"]
md_dirs = ["md"]
```

**Example**: If your GitHub username is `johndoe` and your repo is `my-assets`, it would be:
```toml
base_url = "https://johndoe.github.io/my-assets"
```

### Step 5: Connect Local Repository to GitHub

```bash
# Add your GitHub repository as remote origin
# Replace <your-username> and <your-repo-name> with your actual values
git remote add origin https://github.com/<your-username>/<your-repo-name>.git

# Verify the remote was added
git remote -v
```

### Step 6: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

### Step 7: Enable GitHub Actions

1. Go to your repository on GitHub: `https://github.com/<your-username>/<your-repo-name>`
2. Click on the **"Actions"** tab
3. If you see a message about enabling workflows, click **"I understand my workflows, go ahead and enable them"**
4. GitHub Actions are now enabled

### Step 8: Configure GitHub Pages Settings

1. In your repository, go to **Settings** → **Pages**
2. Under **"Source"**, select **"GitHub Actions"** (NOT "Deploy from a branch")
   - ⚠️ **Important**: This is crucial! The workflow deploys to `gh-pages` branch, so you must use "GitHub Actions" as the source
3. The page will automatically refresh and show your site URL

### Step 9: Wait for First Deployment

1. Go to the **"Actions"** tab in your repository
2. You should see a workflow run called **"Deploy to GitHub Pages"** running or completed
3. Wait for it to complete (usually takes 1-2 minutes)
4. Once completed, you'll see a green checkmark ✓

### Step 10: Test Your Deployment

After the workflow completes, test your URLs:

1. **Base URL**: `https://<your-username>.github.io/<your-repo-name>/`
2. **Sample Image (JPG)**: `https://<your-username>.github.io/<your-repo-name>/images/sample.jpg`
3. **Sample Image (WebP)**: `https://<your-username>.github.io/<your-repo-name>/images/sample.webp`
4. **Minified CSS**: `https://<your-username>.github.io/<your-repo-name>/css/style.min.css`
5. **Minified JS**: `https://<your-username>.github.io/<your-repo-name>/js/app.min.js`

**Note**: It may take a few minutes after the workflow completes for GitHub Pages to propagate. If you get a 404, wait 2-3 minutes and try again.

## Manual Workflow Trigger (Optional)

You can manually trigger the deployment workflow:

1. Go to **Actions** tab
2. Click on **"Deploy to GitHub Pages"** workflow
3. Click **"Run workflow"** button (top right)
4. Select branch: `main`
5. Click **"Run workflow"**

## Troubleshooting

### Images Return 404

- **Check GitHub Pages source**: Make sure it's set to **"GitHub Actions"**, not "Deploy from a branch"
- **Check workflow status**: Go to Actions tab and verify the workflow completed successfully
- **Wait a few minutes**: GitHub Pages can take 2-5 minutes to propagate changes
- **Check the URL**: Make sure you're using the correct format: `https://<username>.github.io/<repo-name>/images/filename.webp`

### Workflow Fails

- **Check Actions logs**: Click on the failed workflow run to see error details
- **Verify dependencies**: Make sure `requirements.txt` dependencies are valid
- **Check file paths**: Ensure files exist in `src/` directories

### Wrong Base URL in Generated Links

- **Update config.toml**: Make sure `base_url` matches your GitHub Pages URL exactly
- **Regenerate links**: After updating config.toml, push changes and the workflow will regenerate links

## Next Steps

1. **Add your own assets**: Place files in the appropriate `src/` directories:
   - `src/images/` - Images (PNG, JPG, JPEG, SVG, GIF, WebP)
   - `src/css/` - CSS stylesheets
   - `src/js/` - JavaScript files
   - `src/data/` - Data files (JSON, CSV, TXT, XML)
   - `src/md/` - Markdown files

2. **Commit and push**: Any push to `main` branch will automatically trigger a new deployment

3. **Use generated links**: After deployment, check the `links/` directory for markdown files with ready-to-use URLs

## Quick Reference

| Item | Value |
|------|-------|
| GitHub Pages URL Format | `https://<username>.github.io/<repo-name>/` |
| Images URL | `https://<username>.github.io/<repo-name>/images/<filename>` |
| CSS URL | `https://<username>.github.io/<repo-name>/css/<filename>.min.css` |
| JS URL | `https://<username>.github.io/<repo-name>/js/<filename>.min.js` |
| GitHub Pages Source | **GitHub Actions** (not "Deploy from a branch") |
| Deployment Branch | `gh-pages` (automatically created by workflow) |
| Source Branch | `main` |

## Summary Checklist

- [ ] Cloned the template repository
- [ ] Removed `.git` and initialized new repository
- [ ] Created new repository on GitHub
- [ ] Updated `config.toml` with your GitHub Pages URL
- [ ] Connected local repo to GitHub remote
- [ ] Pushed code to GitHub
- [ ] Enabled GitHub Actions
- [ ] Configured GitHub Pages to use "GitHub Actions"
- [ ] Waited for workflow to complete
- [ ] Tested URLs and verified they work

## Need Help?

If you encounter issues:

1. Check the workflow logs in the **Actions** tab
2. Verify all settings match this guide
3. Ensure your repository name matches the URL in `config.toml`
4. Make sure GitHub Pages is set to **"GitHub Actions"** source

---

**Congratulations!** 🎉 Your static assets are now deployed and accessible via GitHub Pages!
