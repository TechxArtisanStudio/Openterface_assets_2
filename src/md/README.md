# Static Assets Template

Welcome to the Static Assets Template repository!

## Overview

This template provides a complete setup for building, optimizing, and deploying static assets to GitHub Pages.

## Features

- **Automated Build Pipeline**: Converts images to WebP, minifies CSS/JS
- **GitHub Actions**: Automatically builds and deploys on push
- **URL Generation**: Generates markdown files with asset URLs
- **Image Optimization**: Automatic WebP conversion for better compression

## Usage

After deployment, your assets will be available at:

- Images: `https://youyoubilly.github.io/static-assets-template/images/`
- CSS: `https://youyoubilly.github.io/static-assets-template/css/`
- JavaScript: `https://youyoubilly.github.io/static-assets-template/js/`
- Data: `https://youyoubilly.github.io/static-assets-template/data/`

## Example Links

- [Sample Image (JPG)](https://youyoubilly.github.io/static-assets-template/images/sample.jpg)
- [Sample Image (WebP)](https://youyoubilly.github.io/static-assets-template/images/sample.webp)
- [Minified CSS](https://youyoubilly.github.io/static-assets-template/css/style.min.css)
- [Minified JS](https://youyoubilly.github.io/static-assets-template/js/app.min.js)

## Build Process

1. Copy files from `src/` to `dist/`
2. Convert PNG/JPG/JPEG images to WebP
3. Minify CSS files (creates `.min.css`)
4. Minify JavaScript files (creates `.min.js`)
5. Generate URL markdown files in `links/` directory

## Contributing

Feel free to customize this template for your needs!
