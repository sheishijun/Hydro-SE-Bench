# GitHub Setup Guide

This guide will help you upload the HydroSEBench project to GitHub.

## Preparation

### 1. Update Project Information

Before uploading, make sure to update placeholders in the following files:

- **`hydrosebench-eval/pyproject.toml`**: GitHub URLs have been updated to `sheishijun/Hydro-SE-Bench`
  ```toml
  [project.urls]
  Homepage = "https://github.com/sheishijun/Hydro-SE-Bench"
  ```

- **`CONTRIBUTING.md`**: GitHub URLs have been updated to `sheishijun/Hydro-SE-Bench`

### 2. Check File Integrity

Ensure the following files exist and are correct:

- ✅ `LICENSE` - MIT License
- ✅ `README.md` - Project documentation
- ✅ `CONTRIBUTING.md` - Contributing guide
- ✅ `.gitignore` - Git ignore configuration
- ✅ `hydrosebench-eval/pyproject.toml` - Python package configuration
- ✅ `hydrosebench-eval/README.md` - Package usage documentation

## Upload Steps

### Method 1: Using Git Command Line

1. **Initialize Git repository** (if not already done)
   ```bash
   cd hydrosebench-package
   git init
   ```

2. **Add all files**
   ```bash
   git add .
   ```

3. **Commit changes**
   ```bash
   git commit -m "Initial commit: HydroSEBench evaluation toolkit"
   ```

4. **Create a new repository on GitHub**
   - Visit https://github.com/new
   - Enter repository name: `Hydro-SE-Bench`
   - Choose Public or Private
   - **Do not** initialize README, .gitignore, or LICENSE (we already have them)

5. **Add remote repository and push**
   ```bash
   git remote add origin https://github.com/sheishijun/Hydro-SE-Bench.git
   git branch -M main
   git push -u origin main
   ```

### Method 2: Using GitHub Desktop

1. Open GitHub Desktop
2. Select File → Add Local Repository
3. Select the `hydrosebench-package` directory
4. Click Publish repository
5. Enter repository name: `Hydro-SE-Bench` and select visibility
6. Click Publish repository

## Upload Python Package to PyPI (Optional)

If you want to publish the `hydrosebench-eval` package to PyPI:

1. **Install build tools**
   ```bash
   pip install build twine
   ```

2. **Build package**
   ```bash
   cd hydrosebench-eval
   python -m build
   ```

3. **Check package**
   ```bash
   python -m twine check dist/*
   ```

4. **Upload to TestPyPI (testing)**
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

5. **Upload to PyPI (official)**
   ```bash
   python -m twine upload dist/*
   ```

For detailed instructions, refer to `hydrosebench-eval/SETUP_API_TOKEN.md`

## Verify Upload

After uploading, please verify:

- ✅ All files have been uploaded
- ✅ README.md displays correctly
- ✅ LICENSE file exists
- ✅ Code is accessible
- ✅ Example code links are correct

## Next Steps

1. **Add project description and tags**
   - Add project description on GitHub repository page
   - Add relevant tags (e.g., python, benchmark, evaluation, nlp)

2. **Set up GitHub Pages** (optional)
   - Enable GitHub Pages if you need to host documentation

3. **Add badges** (optional)
   - Add build status, license, and other badges to README.md

4. **Create Release**
   - Create the first Release (v0.1.0) on GitHub

## Frequently Asked Questions

### Q: File too large when uploading?
A: Check if `.gitignore` is correctly configured, ensure `dist/`, `*.egg-info/`, and other build artifacts are ignored.

### Q: How to update code?
A: 
```bash
git add .
git commit -m "Describe your changes"
git push
```

### Q: How to add collaborators?
A: On the GitHub repository page, Settings → Collaborators → Add people

---

Good luck with your upload! If you have questions, please refer to GitHub official documentation or submit an Issue.
