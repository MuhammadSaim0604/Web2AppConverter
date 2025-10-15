# Windows Automated Setup Guide

## 🚀 Quick Start - Automated Installation

This guide provides **fully automated setup scripts** for Windows that handle everything from installation to running the server.

---

## 📦 What You Get

Three automated scripts for complete Windows setup:

### 1. **setup_windows.py** (Main Setup Script)
Complete Python-based setup automation that:
- ✅ Checks and installs Python 3.11+
- ✅ Checks and installs Java JDK 21
- ✅ Installs apktool 2.9.3
- ✅ Installs Android SDK Build Tools 34.0.0
- ✅ Creates isolated Python virtual environment
- ✅ Installs all project dependencies
- ✅ Creates required directories
- ✅ Verifies all installations
- ✅ Optionally starts the server

### 2. **setup_windows.bat** (Batch File Wrapper)
Simple batch file that:
- ✅ Checks for administrator privileges
- ✅ Ensures Python is available
- ✅ Runs the Python setup script
- ✅ Provides user-friendly error messages

### 3. **run_server.bat** (Server Start Script)
Quick server launcher that:
- ✅ Activates virtual environment
- ✅ Starts Flask server on port 5000
- ✅ Provides easy stop/restart

---

## 🎯 Installation Steps

### Option 1: One-Click Setup (Recommended)

1. **Download the Project**
   ```
   All scripts are included in the project root
   ```

2. **Run Setup as Administrator**
   - Right-click `setup_windows.bat`
   - Select **"Run as administrator"**
   - Follow the on-screen prompts

3. **Wait for Completion**
   - The script will automatically download and install everything
   - Total time: 5-15 minutes (depending on internet speed)

4. **Start Using**
   - Server starts automatically at http://localhost:5000
   - Or use `run_server.bat` to start later

### Option 2: Python Script Directly

If you already have Python installed:

```cmd
python setup_windows.py
```

---

## 📋 What Gets Installed

### System Requirements (Auto-Installed)

| Component | Version | Download Size | Installation |
|-----------|---------|---------------|--------------|
| Python | 3.11.9 | ~30 MB | Automated |
| Java JDK | 21 (Adoptium) | ~180 MB | Automated |
| apktool | 2.9.3 | ~10 MB | Automated |
| Android SDK Build Tools | 34.0.0 | ~60 MB | Automated |

### Python Dependencies (Auto-Installed)

```
beautifulsoup4 >= 4.14.2
flask >= 3.1.2
flask-cors >= 6.0.1
pillow >= 11.3.0
requests >= 2.32.5
```

### Directory Structure (Auto-Created)

```
project/
├── venv/                          ← Virtual environment (isolated)
├── db/                            ← Database directory
├── generated/                     ← Generated APK files
├── backend/                       ← Flask application
├── apk_builder/                   ← APK building system
├── android_templates_apks/        ← Base APK templates
├── setup_windows.py              ← Main setup script
├── setup_windows.bat             ← Batch wrapper
└── run_server.bat                ← Server launcher
```

---

## 🔧 Installation Process Details

### Step 1: Python 3.11+ Installation
- Checks if Python is already installed
- Downloads official Python 3.11.9 installer if needed
- Installs with PATH configuration
- Verifies version compatibility

### Step 2: Java JDK 21 Installation
- Checks if Java is already installed
- Downloads Adoptium OpenJDK 21 if needed
- Configures JAVA_HOME environment variable
- Adds Java to system PATH

### Step 3: apktool Installation
- Downloads apktool wrapper script (apktool.bat)
- Downloads apktool JAR file (version 2.9.3)
- Installs to `%USERPROFILE%\apktool`
- Adds to system PATH

### Step 4: Android SDK Build Tools
- Downloads Android Command Line Tools
- Extracts to `%USERPROFILE%\Android`
- Installs build-tools 34.0.0 via sdkmanager
- Configures apksigner for APK signing
- Adds build-tools to PATH

### Step 5: Virtual Environment
- Creates isolated Python venv in project directory
- Ensures dependencies don't conflict with system Python
- Uses project-specific Python and packages

### Step 6: Dependencies Installation
- Activates virtual environment
- Upgrades pip to latest version
- Installs all required Python packages
- Verifies successful installation

### Step 7: Directory Setup
- Creates `db/` for API keys database
- Creates `generated/` for generated APK files
- Verifies `android_templates_apks/` exists

### Step 8: Verification
- Checks all tools are accessible
- Verifies versions are correct
- Confirms PATH configurations
- Reports any issues

---

## ✅ Verification Commands

After installation, verify everything works:

### Check Python (in venv)
```cmd
venv\Scripts\python.exe --version
# Should show: Python 3.11.x
```

### Check Java
```cmd
java -version
# Should show: openjdk version "21.x.x"
```

### Check apktool
```cmd
apktool --version
# Should show: 2.9.3
```

### Check apksigner
```cmd
apksigner
# Should show: usage information
```

### Check Server
```cmd
run_server.bat
# Should start server on http://localhost:5000
```

---

## 🚀 Starting the Server

### Method 1: After Setup
During setup, you'll be prompted:
```
Do you want to start the server now? (Y/n):
```
Type `Y` or press Enter to start immediately.

### Method 2: Using run_server.bat
Double-click `run_server.bat` or run:
```cmd
run_server.bat
```

### Method 3: Manual Start
```cmd
venv\Scripts\activate
python backend\app.py
```

The server will be available at:
```
http://localhost:5000
```

---

## 🚨 Troubleshooting

### Issue: "Not running as Administrator"
**Solution:** Right-click the batch file and select "Run as administrator"

### Issue: "Python installation failed"
**Solution:** 
1. Download manually from https://www.python.org/downloads/
2. Install with "Add Python to PATH" checked
3. Run setup script again

### Issue: "Java installation failed"
**Solution:**
1. Download manually from https://adoptium.net/
2. Install the Windows x64 MSI installer
3. Run setup script again

### Issue: "Download failed" errors
**Solution:**
- Check internet connection
- Check firewall/antivirus settings
- Ensure no proxy blocking downloads
- Try running as administrator

### Issue: "Path not recognized" after installation
**Solution:**
- Close and reopen Command Prompt/PowerShell
- Restart your computer
- Manually add to PATH if needed

### Issue: Port 5000 already in use
**Solution:**
```cmd
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or modify port in backend\app.py
```

### Issue: Virtual environment activation fails
**Solution:**
```cmd
# Delete and recreate venv
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔄 Updating Dependencies

To update Python packages:

```cmd
# Activate virtual environment
venv\Scripts\activate

# Update all packages
pip install --upgrade beautifulsoup4 flask flask-cors pillow requests

# Or update individually
pip install --upgrade flask
```

---

## 🎉 Success Indicators

After successful setup, you should see:

```
========================================
Setup Complete!
========================================

All required tools and dependencies are installed:
  ✓ Python 3.11+ with virtual environment
  ✓ Java JDK 21
  ✓ apktool 2.9.3
  ✓ Android SDK Build Tools 34.0.0
  ✓ All Python dependencies

Do you want to start the server now? (Y/n):
```

---

## 📊 Features After Setup

Once setup is complete, you can:

1. **Convert URLs to APKs** via web interface
2. **Generate API keys** for programmatic access
3. **Build custom Android apps** with:
   - Custom app names
   - Custom icons
   - Website URL integration
   - Signed APKs ready for distribution

---

## 🔒 Security Notes

### Keystore Configuration
The default keystore credentials are for **development only**:
```json
{
  "keystore": {
    "path": "android_templates_apks/keystore.jks",
    "alias": "app-key",
    "store_pass": "android123",
    "key_pass": "android123"
  }
}
```

⚠️ **For production, configure secure credentials:**

```cmd
# Using environment variables (recommended)
set KEYSTORE_PATH=C:\path\to\your\keystore.jks
set KEYSTORE_ALIAS=your-key-alias
set KEYSTORE_PASS=your-secure-password
set KEY_PASS=your-secure-password

# Then start server
run_server.bat
```

See `KEYSTORE_SETUP.md` for detailed security instructions.

---

## 📚 Additional Resources

- **Backend Setup**: See `BACKEND_SETUP.md`
- **API Documentation**: See `API_DOCUMENTATION.md`
- **Keystore Security**: See `KEYSTORE_SETUP.md`
- **Customization Guide**: See `AI_AGENT_CUSTOMIZATION_GUIDE.md`

---

## 🆘 Getting Help

1. **Check logs** for error messages
2. **Verify installations** using verification commands
3. **Review troubleshooting** section above
4. **Check file permissions** and admin rights
5. **Ensure all dependencies** are installed

---

## 🌟 Key Advantages

✅ **Fully Isolated Environment**
- Virtual environment prevents conflicts
- Project-specific dependencies
- Clean uninstallation (just delete venv folder)

✅ **Automated Everything**
- No manual downloads
- No manual PATH configuration
- No manual installations
- One-click setup

✅ **Production Ready**
- Secure APK signing
- API key management
- Professional APK generation
- Full Android compatibility

✅ **Easy Maintenance**
- Simple dependency updates
- Easy server start/stop
- Clear error messages
- Comprehensive logging

---

**Last Updated**: October 2025  
**Compatibility**: Windows 10/11  
**Status**: Production Ready ✅
