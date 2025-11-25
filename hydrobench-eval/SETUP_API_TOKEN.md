# TestPyPI API Token Setup Guide

## Step 1: Get TestPyPI API Token

1. **Register TestPyPI Account** (if you don't have one yet)
   - Visit: https://test.pypi.org/account/register/
   - Note: TestPyPI and official PyPI accounts are **separate** and need to be registered separately

2. **Login to TestPyPI**
   - Visit: https://test.pypi.org/account/login/

3. **Create API Token**
   - After logging in, visit: https://test.pypi.org/manage/account/token/
   - Click "Add API token"
   - Enter Token name (e.g., "hydrobench-upload")
   - Select Scope:
     - **Entire account**: Can upload all projects
     - **Specific project**: Can only upload specified project (more secure)
   - Click "Add token"
   - **Important**: Copy the generated Token (format similar to `pypi-xxxxxxxxxxxxx`), **only displayed once**, please save it securely

## Step 2: Configure Authentication File

### Windows System

1. **Find User Home Directory**
   - Usually: `C:\Users\YourUsername\`

2. **Create or Edit `.pypirc` File**
   - File path: `C:\Users\YourUsername\.pypirc`
   - Note: Filename starts with a dot and has no extension

3. **File Content**:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YourTestPyPI-API-Token

[pypi]
username = __token__
password = pypi-YourOfficialPyPI-API-Token (if available)
```

### Linux/Mac System

1. **Create or Edit `~/.pypirc` File**

```bash
nano ~/.pypirc
# or
vim ~/.pypirc
```

2. **File Content** (same as above)

## Step 3: Verify Configuration

Run the upload script. If configured correctly, it should upload successfully:

```bash
python upload_to_testpypi.py
```

## Security Tips

1. **Do not commit `.pypirc` file to Git**
   - Ensure `.pypirc` is in `.gitignore`
   - Or use environment variables (see below)

2. **Using Environment Variables (More Secure Method)**

If you don't want to use the `.pypirc` file, you can set environment variables in the command line:

**Windows (PowerShell):**
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-Your-API-Token"
python upload_to_testpypi.py
```

**Windows (CMD):**
```cmd
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=pypi-Your-API-Token
python upload_to_testpypi.py
```

**Linux/Mac:**
```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-Your-API-Token"
python upload_to_testpypi.py
```

## Common Issues

### Q: Cannot find `.pypirc` file?
A: 
- Windows: File may be hidden, need to enable "Show hidden files" in File Explorer
- Or create directly in command line:
  ```cmd
  echo. > C:\Users\YourUsername\.pypirc
  ```

### Q: What is the API Token format?
A: TestPyPI Token format: Starts with `pypi-`, followed by a string of characters, for example:
```
pypi-AgEIcHlwaS5vcmcCJGI5YjU2YjY3Yi04NmI4LTRkYmEtYWRjNC1kZWUwMGNiMmE3ZGUAAAYsY2xhc3NpYy1yZWxlYXNlLWFwaQ
```

### Q: Authentication failed when uploading?
A: Check:
1. Token is correctly copied (including `pypi-` prefix)
2. `.pypirc` file path is correct
3. File format is correct (INI format)
4. Token has not expired (can be recreated)

### Q: Can I configure both TestPyPI and official PyPI?
A: Yes, configure both in `.pypirc`, and the script will automatically use the `testpypi` configuration.
