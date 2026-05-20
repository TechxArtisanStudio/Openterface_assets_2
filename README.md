# Openterface Assets (static-assets-template)

A template repository for managing static assets with automated GitHub Actions workflows. This template provides a complete setup for building, optimizing, and deploying static assets (images, CSS, JavaScript, data files) to GitHub Pages with automatic WebP conversion and URL generation.

**Live asset browser:** [https://assets2.openterface.com/](https://assets2.openterface.com/) — search, filter by category, copy CDN links, and preview images.

## Overview

This template is designed to be cloned and customized for multiple projects. It includes:

- **Automated Build Pipeline**: Converts images to WebP, minifies CSS/JS, and prepares assets for deployment
- **GitHub Actions Workflow**: Automatically builds and deploys to GitHub Pages on push to main
- **URL Generation**: Automatically generates markdown files with asset URLs
- **Asset Browser**: Static gallery at the site root with search, categories, and copy-to-clipboard actions
- **Configurable Base URL**: Easy configuration via `config.toml`
- **Image Optimization**: Converts PNG/JPG/JPEG images to WebP format for better compression

## Quick Start

> 📖 **New to this template?** Check out the detailed [**SETUP.md**](SETUP.md) guide for step-by-step instructions on setting up this template for your own GitHub account.
> 
> 🚀 **Quick Setup**: Run `python scripts/setup.py` for an interactive setup wizard that automates the configuration process!

### 1. Clone and Customize

```bash
# Clone this template repository
git clone <your-template-repo-url> my-assets-repo
cd my-assets-repo

# Remove the template's git history and initialize your own
rm -rf .git
git init
git add .
git commit -m "Initial commit from static-assets-template"
```

### 2. Configure Your Repository

Edit `config.toml` with your settings:

```toml
[repository]
base_url = "https://assets.yourdomain.com"  # Your actual domain
domain = "assets.yourdomain.com"            # For CNAME

[build]
# Directories to process (already configured)
image_dirs = ["images"]
css_dirs = ["css"]
js_dirs = ["js"]
data_dirs = ["data"]
md_dirs = ["md"]
```

### 3. Configure Custom Domain (Optional)

If using a custom domain, edit `src/CNAME`:

```
assets.yourdomain.com
```

If using the default GitHub Pages domain (`username.github.io`), delete or leave `src/CNAME` empty.

### 4. Add Your Assets

Add your files to the appropriate directories:

- `src/images/` - Image files (PNG, JPG, JPEG, SVG, GIF, WebP)
- `src/css/` - CSS stylesheets
- `src/js/` - JavaScript files
- `src/data/` - Data files (CSV, JSON, TXT, XML)
- `src/md/` - Markdown files (optional)

### 5. Set Up GitHub Pages

1. Push your repository to GitHub
2. Go to repository Settings → Pages
3. Under "Source", select "GitHub Actions"
4. The workflow will automatically deploy on push to `main` branch

## Project Structure

```
static-assets-template/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── src/
│   ├── images/                 # Image assets
│   ├── css/                    # CSS stylesheets
│   ├── js/                     # JavaScript files
│   ├── data/                   # Data files
│   └── md/                     # Markdown files (optional)
├── src/site/                   # Static asset browser (index.html, styles.css, app.js)
├── scripts/
│   ├── setup.py                # Interactive setup script (run this first!)
│   ├── generate_url.py         # URL generation script
│   ├── generate_manifest.py    # Builds dist/assets.json for the browser
│   └── image_resizer.py        # Image resizing utility
├── links/                      # Generated markdown files with URLs
├── build.sh                    # Build script
├── config.toml                 # Configuration file
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── SETUP.md                    # Detailed setup guide for new users
└── README.md                   # This file
```

## Configuration

### config.toml

The `config.toml` file contains repository-specific settings:

- **base_url**: The base URL for generated asset links (used in `links/` markdown files)
- **domain**: Your custom domain for GitHub Pages (used in CNAME)

### CNAME File

The `src/CNAME` file specifies your custom domain for GitHub Pages. If you're using the default GitHub Pages domain (`username.github.io`), you can delete this file or leave it empty.

## Workflow

### Build Process

When you push to the `main` branch, GitHub Actions automatically:

1. **Checks out** your repository
2. **Installs** dependencies (Node.js tools, Python packages)
3. **Builds** assets:
   - Copies files from `src/` to `dist/`
   - Converts PNG/JPG/JPEG images to WebP format
   - Minifies CSS files (creates `.min.css` files)
   - Minifies JavaScript files (creates `.min.js` files)
4. **Generates** URL markdown files in `links/` directory
5. **Builds** `dist/assets.json` catalog for the asset browser
6. **Deploys** `dist/` directory to GitHub Pages (CDN + browser homepage)

### Manual Build

You can also build locally:

```bash
# Install dependencies
pip install -r requirements.txt
npm install -g uglify-js csso-cli

# On macOS, install webp tools
brew install webp

# Run build script
./build.sh

# Generate URL links
python scripts/generate_url.py

# Generate browser catalog (requires dist/ from build)
python scripts/generate_manifest.py

# Preview the asset browser locally
python -m http.server 8080 --directory dist
# Open http://localhost:8080/
```

## Asset Browser

The site at the repository root URL (`https://assets2.openterface.com/` when deployed) is a read-only browser for everything in `dist/`:

- **Search** by filename, path, or folder (press `/` to focus the search box)
- **Filter** by category: Images, Data (including APKs), CSS, JavaScript, Markdown
- **Copy** raw URL, markdown link, or markdown image syntax
- **Preview** images in a lightbox
- **View toggle** — **Comfortable** (default grid), **Compact** (denser grid), or **Masonry** (Pinterest-style columns sized by each image’s aspect ratio; preference saved in your browser)
- **Lazy loading** — thumbnails load as you scroll (all three views) via `IntersectionObserver`, with shimmer placeholders sized from manifest dimensions
- **Sort** — Name A–Z, **Newest first**, or **Oldest first** (uses last Git commit date per file in `src/` as the upload/update time)

The catalog is generated from built files (not `links/*.md`), so it always matches what GitHub Pages serves. Raster images with both JPEG/PNG and WebP variants appear once (WebP preferred).

## Access (password gate)

The asset browser homepage is protected by a **lightweight frontend gate** (shared team password). This only hides the browse UI from casual visitors—it is **not** strong security.

- **Remember on this device** is enabled by default: after entering the password once, your browser keeps access for **30 days** (`localStorage`).
- Uncheck “Remember on this device” to require the password again when the browser session ends (`sessionStorage` only).
- Use **Log out** in the header to clear stored access on shared machines.

**Still public without the password:**

- Direct CDN URLs (`/images/...`, `/data/...`, etc.)
- `https://assets2.openterface.com/assets.json`
- All files in this public GitHub repository

Do not rely on this gate to protect confidential assets; use private hosting if you need real access control.

## Adding Assets

### Images

Place images in `src/images/`:

- **PNG, JPG, JPEG**: Automatically converted to WebP during build
- **SVG, GIF, WebP**: Copied as-is (no conversion)

Example:
```bash
src/images/
  ├── logo.png          → dist/images/logo.png + logo.webp
  ├── banner.jpg        → dist/images/banner.jpg + banner.webp
  └── icon.svg          → dist/images/icon.svg
```

### CSS Files

Place CSS files in `src/css/`:

- Original files are copied to `dist/css/`
- Minified versions (`.min.css`) are created automatically

Example:
```bash
src/css/
  └── style.css         → dist/css/style.css + style.min.css
```

### JavaScript Files

Place JS files in `src/js/`:

- Original files are copied to `dist/js/`
- Minified versions (`.min.js`) are created automatically

Example:
```bash
src/js/
  └── app.js            → dist/js/app.js + app.min.js
```

### Data Files

Place data files in `src/data/`:

- Files are copied as-is to `dist/data/`

Supported formats: CSV, JSON, TXT, XML, APK

## URL Generation

The `scripts/generate_url.py` script automatically generates markdown files with asset URLs in the `links/` directory.

### Usage

```bash
# Generate URLs from source files (predicts final URLs)
python scripts/generate_url.py

# Generate URLs from built files (actual URLs after build)
python scripts/generate_url.py --dist

# Override base URL
python scripts/generate_url.py --base-url https://custom-domain.com
```

### Generated Files

The script creates markdown files in `links/`:

- `webp.md` - WebP image links
- `svg.md` - SVG image links
- `gif.md` - GIF image links
- `css.md` - CSS file links
- `js.md` - JavaScript file links
- `data.md` - Data file links
- `md.md` - Markdown file links

Each file contains markdown links that you can copy and paste into your documentation or markdown files.

## Image Conversion

### WebP Conversion

PNG, JPG, and JPEG images are automatically converted to WebP format during the build process. Both the original and WebP versions are available:

- Original: `https://your-domain.com/images/photo.jpg`
- WebP: `https://your-domain.com/images/photo.webp`

### Image Resizing

Use the included `image_resizer.py` script to resize images:

```bash
# Interactive mode - select image from menu
python scripts/image_resizer.py

# Direct mode - specify image path
python scripts/image_resizer.py src/images/photo.jpg
```

## Dependencies

### Build Tools

- **cwebp** - WebP image converter (install via `brew install webp` on macOS)
- **csso** - CSS minifier (install via `npm install -g csso-cli`)
- **uglifyjs** - JavaScript minifier (install via `npm install -g uglify-js`)
- **rsync** - File synchronization (usually pre-installed)

### Python Dependencies

- **Pillow** - Image processing (for `image_resizer.py`)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Examples

### Example Asset URLs

After deployment, your assets will be available at:

```
https://your-domain.com/images/logo.webp
https://your-domain.com/css/style.min.css
https://your-domain.com/js/app.min.js
https://your-domain.com/data/config.json
```

### Example Markdown Links

The generated `links/` files contain ready-to-use markdown links:

```markdown
[logo-webp](https://your-domain.com/images/logo.webp)
[style-min-css](https://your-domain.com/css/style.min.css)
[app-min-js](https://your-domain.com/js/app.min.js)
```

## Troubleshooting

### Build Fails

- Ensure all dependencies are installed
- Check that `build.sh` is executable: `chmod +x build.sh`
- Verify file paths in `src/` directories exist

### Images Not Converting

- Ensure `cwebp` is installed: `brew install webp` (macOS) or `apt-get install webp` (Linux)
- Check that images are in `src/images/` directory
- Verify image formats are PNG, JPG, or JPEG

### GitHub Pages Not Deploying

- Check GitHub Actions workflow runs successfully
- Verify repository Settings → Pages → Source is set to "GitHub Actions"
- Ensure `dist/` directory is generated (check Actions logs)

### URLs Not Generating

- Run `python scripts/generate_url.py` manually to check for errors
- Verify `config.toml` has correct `base_url` setting
- Check that files exist in `src/` directories

## Customization

### Adding New File Types

To add support for new file types, edit `scripts/generate_url.py`:

1. Add entry to `FILE_TYPE_MAPPING` dictionary
2. Specify extensions, directories, and transformations
3. Update `build.sh` if special processing is needed

### Modifying Build Process

Edit `build.sh` to customize the build process:

- Add new directories to process
- Modify conversion settings
- Add additional optimization steps

## License

MIT License - see LICENSE file for details

## Contributing

This is a template repository. Feel free to fork and customize for your needs!

## Support

For issues or questions, please open an issue on the repository.
