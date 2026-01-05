# Windows Setup Guide

## Quick Fix for Your Current Issue

You're encountering build issues because Python 3.14 is very new. Here are **two solutions**:

### Option 1: Use Python Module Syntax (Easiest)

Since Streamlit is already installed, just run it this way:

```powershell
python -m streamlit run app.py
```

Or if that doesn't work:

```powershell
py -m streamlit run app.py
```

### Option 2: Fresh Install with Updated Packages

1. **First, install the missing dependencies:**

```powershell
py -m pip install altair blinker gitpython pillow pydeck toml tornado
```

2. **Then downgrade pyarrow to compatible version:**

```powershell
py -m pip install "pyarrow<22"
```

3. **Run Streamlit:**

```powershell
py -m streamlit run app.py
```

---

## Recommended: Use Python 3.11 or 3.12

Python 3.14 is very new and many packages don't have prebuilt Windows wheels yet. For the best experience:

### Option A: Install Python 3.11 or 3.12

1. **Download Python 3.12** from https://www.python.org/downloads/
2. **During installation, check "Add Python to PATH"**
3. **Create a new virtual environment:**

```powershell
# Navigate to project directory
cd C:\Users\smani\insurance-benefits-opus

# Create virtual environment
py -3.12 -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option B: Use the Current Python 3.14

If you want to stick with Python 3.14, here's the minimal installation:

```powershell
# Install only the essential packages (that have wheels for 3.14)
py -m pip install streamlit anthropic plotly python-dotenv requests pydantic PyPDF2

# Run the app
py -m streamlit run app.py
```

---

## Complete Fresh Setup (Recommended)

### 1. Clean Installation

```powershell
# Navigate to project
cd C:\Users\smani\insurance-benefits-opus

# Create virtual environment (using Python 3.12 if available)
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### 2. Configure API Key

```powershell
# Copy the example file (you already did this)
# Edit .env and add your Anthropic API key
notepad .env
```

In the `.env` file, replace `your_api_key_here` with your actual Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-...your-actual-key...
```

### 3. Run the Application

```powershell
# If in virtual environment
streamlit run app.py

# OR if streamlit not in PATH
python -m streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Troubleshooting

### Error: "streamlit is not recognized"

**Solution:** Use the module syntax:
```powershell
python -m streamlit run app.py
```

### Error: "Failed building wheel for numpy/pandas/pyarrow"

**Solutions:**

1. **Use Python 3.11 or 3.12** (packages have prebuilt wheels)
2. **Install Visual Studio Build Tools** (if you must use 3.14):
   - Download from: https://visualstudio.microsoft.com/downloads/
   - Install "Desktop development with C++"
3. **Install prebuilt packages manually:**
   ```powershell
   py -m pip install --only-binary :all: numpy pandas pyarrow
   ```

### Error: "ModuleNotFoundError: No module named 'anthropic'"

**Solution:** Install missing package:
```powershell
py -m pip install anthropic
```

### Error: PowerShell execution policy prevents script

**Solution:** Allow script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Current Dependencies Status

Based on your system, you have:
- ✅ Python 3.14 installed
- ✅ pandas 2.3.3 already installed
- ✅ streamlit 1.51.0 already installed
- ❌ Missing streamlit dependencies (altair, blinker, etc.)
- ⚠️ pyarrow 22.0.0 (incompatible with streamlit - needs <22)

### Quick Fix Command

Run this single command to fix dependency issues:

```powershell
py -m pip install "pyarrow<22" altair blinker gitpython pillow pydeck toml tornado
```

Then run:

```powershell
py -m streamlit run app.py
```

---

## Features That Require Additional Setup

### PDF Image Processing (Optional)

If you want to process scanned PDF images, install:

**Tesseract OCR:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install (note the installation path)
3. Add to PATH or set in code

**Poppler (for pdf2image):**
1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to PATH

Then install Python packages:
```powershell
pip install pdf2image pytesseract
```

---

## Minimal Test

To test if everything works:

```powershell
# Test Python
python --version

# Test Streamlit is installed
python -m streamlit --version

# Test Anthropic SDK
python -c "import anthropic; print('Anthropic SDK: OK')"

# Run the app
python -m streamlit run app.py
```

---

## Need Help?

If you continue to have issues:

1. **Check Python version:** `python --version` (recommend 3.11 or 3.12)
2. **Check installed packages:** `pip list`
3. **Try the quick fix command above**
4. **Use virtual environment** (cleanest solution)

---

## Summary: What You Need to Do Right Now

```powershell
# Fix dependency conflicts
py -m pip install "pyarrow<22" altair blinker gitpython pillow pydeck toml tornado

# Run the app
py -m streamlit run app.py
```

That's it! The app should open in your browser.
