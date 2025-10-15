
# Complete Automated Setup Guide for Windows

## 🚀 One-Click Setup

This guide provides a **fully automated setup** that installs everything needed to run the URL to Android App Converter backend on Windows.

---

## 📋 What Gets Installed Automatically

The `setup_complete_windows.bat` script automatically detects and installs:

### 1. **Python 3.11+**
- Downloads official Python installer
- Installs with PATH configuration
- Verifies version compatibility

### 2. **Java JDK 21**
- Downloads from Oracle or Adoptium
- Configures JAVA_HOME
- Adds to system PATH

### 3. **apktool 2.9.3**
- Downloads apktool wrapper script
- Downloads apktool JAR file
- Installs to user directory
- Adds to PATH

### 4. **Android SDK Build Tools**
- Downloads Android Command Line Tools
- Installs build-tools 34.0.0
- Configures apksigner
- Adds to PATH

### 5. **Python Virtual Environment**
- Creates isolated venv
- Activates environment
- Upgrades pip

### 6. **Python Dependencies**
- beautifulsoup4 >= 4.14.2
- flask >= 3.1.2
- flask-cors >= 6.0.1
- pillow >= 11.3.0
- requests >= 2.32.5

### 7. **Project Directories**
- Creates `db/` directory
- Creates `generated/` directory
- Verifies `android_templates_apks/` directory

---

## 🎯 Quick Start (Recommended)

### Step 1: Download the Script
The `setup_complete_windows.bat` file is already in your project root.

### Step 2: Run as Administrator
1. **Right-click** on `setup_complete_windows.bat`
2. Select **"Run as administrator"**
3. Press any key when prompted to start installation

### Step 3: Wait for Completion
The script will:
- Download all required tools
- Install and configure everything
- Start the Flask server automatically

### Step 4: Access the Application
Once setup completes, open your browser to:
```
http://localhost:5000
```

---

## 📊 Installation Process Steps

### **STEP 1/8: Python Installation**
- Checks if Python is installed
- If not found, downloads Python 3.11.9
- Installs silently with PATH configuration
- Verifies version >= 3.11

### **STEP 2/8: Java JDK Installation**
- Checks if Java is installed
- If not found, downloads JDK 21
- Tries Oracle first, then Adoptium
- Configures JAVA_HOME environment variable

### **STEP 3/8: apktool Installation**
- Downloads apktool.bat wrapper
- Downloads apktool_2.9.3.jar
- Installs to `%USERPROFILE%\apktool`
- Adds to system PATH

### **STEP 4/8: Android SDK Build Tools**
- Downloads Android Command Line Tools
- Extracts to `%USERPROFILE%\Android`
- Installs build-tools 34.0.0 via sdkmanager
- Configures apksigner

### **STEP 5/8: Virtual Environment**
- Creates Python venv in project directory
- Isolates dependencies from system Python

### **STEP 6/8: Activate Environment**
- Activates the virtual environment
- All subsequent commands use venv Python

### **STEP 7/8: Install Dependencies**
- Upgrades pip to latest version
- Installs all required Python packages
- Verifies successful installation

### **STEP 8/8: Directory Setup**
- Creates database directory
- Creates generated files directory
- Verifies APK templates directory exists

---

## 🛠️ Manual Installation (Alternative)

If you prefer manual installation, follow these steps:

### 1. Install Python 3.11+
```
https://www.python.org/downloads/
✓ Check "Add Python to PATH" during installation
```

### 2. Install Java JDK 21
```
https://adoptium.net/temurin/releases/
✓ Download Windows x64 MSI installer
✓ Install with default options
```

### 3. Install apktool
```powershell
# Create apktool directory
mkdir C:\apktool

# Download files
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat" -OutFile "C:\apktool\apktool.bat"
Invoke-WebRequest -Uri "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar" -OutFile "C:\apktool\apktool.jar"

# Add to PATH
setx PATH "%PATH%;C:\apktool"
```

### 4. Install Android SDK Build Tools
```powershell
# Download Command Line Tools
Invoke-WebRequest -Uri "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip" -OutFile "cmdtools.zip"

# Extract
Expand-Archive cmdtools.zip -DestinationPath C:\Android\cmdline-tools

# Install build-tools
C:\Android\cmdline-tools\cmdline-tools\bin\sdkmanager.bat --sdk_root=C:\Android "build-tools;34.0.0"

# Add to PATH
setx PATH "%PATH%;C:\Android\build-tools\34.0.0"
```

### 5. Setup Python Environment
```cmd
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install beautifulsoup4>=4.14.2 flask>=3.1.2 flask-cors>=6.0.1 pillow>=11.3.0 requests>=2.32.5
```

### 6. Create Directories
```cmd
mkdir db
mkdir generated
```

### 7. Run Server
```cmd
python backend\app.py
```

---

## 🔍 Verification

After installation, verify all tools are working:

### Check Python
```cmd
python --version
# Should show: Python 3.11.x or higher
```

### Check Java
```cmd
java -version
# Should show: openjdk version "21.x.x"
```

### Check apktool
```cmd
apktool
# Should show: Apktool v2.9.3
```

### Check apksigner
```cmd
apksigner
# Should show: apksigner usage information
```

---

## 📂 Project Structure After Setup

```
project/
├── setup_complete_windows.bat    ← Automated setup script
├── backend/
│   ├── app.py                     ← Flask server
│   ├── api_key_manager.py
│   └── services/
├── apk_builder/
│   ├── builder.py
│   ├── version_detector.py
│   └── config.json
├── android_templates_apks/
│   ├── base_1.apk                 ← Base APK template
│   └── keystore.jks               ← Signing keystore
├── db/                            ← Database directory (auto-created)
├── generated/                     ← Generated files (auto-created)
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
└── venv/                          ← Virtual environment (auto-created)
```

---

## 🚨 Troubleshooting

### Issue: "Python is not recognized"
**Solution:** Run the script as administrator or manually add Python to PATH

### Issue: "Java installation failed"
**Solution:** Manually download from https://adoptium.net/ and install

### Issue: "apksigner not found"
**Solution:** Restart command prompt after installation to refresh PATH

### Issue: "Permission denied" errors
**Solution:** Run the script as administrator

### Issue: "Failed to download"
**Solution:** Check internet connection and firewall settings

### Issue: Port 5000 already in use
**Solution:** Stop other applications using port 5000 or modify `backend/app.py`

---

## 🔄 Updating Dependencies

To update Python packages:
```cmd
venv\Scripts\activate
pip install --upgrade beautifulsoup4 flask flask-cors pillow requests
```

---

## 🎉 Success!

Once setup completes successfully, you'll see:
```
========================================
Setup Complete!
========================================

All required tools and dependencies are installed:
  - Python: Installed and configured
  - Java JDK 21: Installed and configured
  - apktool: Installed and configured
  - apksigner: Installed and configured
  - Python packages: All dependencies installed

========================================
Starting Flask Server...
========================================

Server will be available at: http://localhost:5000
```

Your server is now running and ready to convert URLs to Android APKs!

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all tools are installed: `python`, `java`, `apktool`, `apksigner`
3. Ensure you're running as administrator
4. Check firewall/antivirus settings

---

## 🌐 Replit Deployment (Recommended for Production)

For deployment on Replit, this entire setup is automated - just click Run!
The `.replit` and `replit.nix` files handle all dependencies automatically.
