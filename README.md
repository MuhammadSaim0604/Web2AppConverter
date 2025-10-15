# URL to Android App Converter

A powerful web application that converts any website URL into a fully functional, signed Android APK with just a few clicks.

## 🚀 Quick Start

### Windows Users (Simple Setup)

**Quick Installation - No Android SDK Needed!**

1. **Download the project**
2. **Run setup**: `python setup.py`
3. **Start using** at http://localhost:5000

✅ **Installs automatically:**
- Python virtual environment (isolated)
- All Python dependencies
- Creates required directories

⏭️ **Skips Android SDK** (not needed for basic server operation)

### Replit Users

Simply click the **Run** button - everything is pre-configured!

### Manual Installation (All Platforms)

See [BACKEND_SETUP.md](BACKEND_SETUP.md) for manual setup instructions.

---

## 📋 Features

### 🎨 Web Interface
- Clean, modern UI for easy APK generation
- Custom app name and icon support
- Real-time APK download
- API key management dashboard

### 🔧 APK Generation
- **Convert any website** to Android app
- **Custom branding** (app name, icon)
- **Automatic signing** with v1+v2+v3 signatures
- **Production-ready** APKs
- **WebView-based** with full JavaScript support

### 🔐 API Access
- RESTful API for programmatic APK generation
- API key authentication system
- Usage tracking and management
- Rate limiting support

### 📱 Generated Apps Include
- Full WebView with JavaScript
- Camera and location permissions
- File upload/download support
- Pull-to-refresh functionality
- Splash screen with app icon
- Progress bar for loading
- Cookie and storage support
- Compatible with Android 6.0+ (API 23)

---

## 📁 Project Structure

```
project/
├── setup_windows.py              # Automated Windows setup script
├── setup_windows.bat             # Batch wrapper for setup
├── run_server.bat                # Quick server launcher (Windows)
│
├── backend/                      # Flask application
│   ├── app.py                   # Main Flask server
│   ├── api_key_manager.py       # API key management
│   └── services/                # Business logic
│       ├── url_metadata.py      # URL metadata extraction
│       ├── android_generator.py # Android project generation
│       └── zipper.py            # ZIP file creation
│
├── apk_builder/                 # APK building system
│   ├── builder.py               # APK modification engine
│   ├── version_detector.py      # Auto-detect base version
│   └── config.json             # Builder configuration
│
├── android_templates_apks/      # Base APK templates
│   ├── base_1.apk              # Template APK
│   └── keystore.jks            # Signing keystore
│
├── frontend/                    # Web interface
│   ├── index.html              # Main UI
│   ├── script.js               # Client-side logic
│   └── style.css               # Styling
│
├── db/                          # Database (auto-created)
│   └── api_keys.json           # API keys storage
│
├── generated/                   # Generated files (auto-created)
│
└── venv/                        # Virtual environment (auto-created)
```

---

## 🎯 Quick Usage

### Web Interface

1. **Start the server**:
   ```bash
   # Windows
   run_server.bat
   
   # Linux/Mac
   python3 backend/app.py
   ```

2. **Open browser** to http://localhost:5000

3. **Enter details**:
   - App Name: Your app name
   - Website URL: https://example.com
   - App Icon: (optional) Upload PNG/JPG

4. **Click "Generate APK"** and download your app!

### API Usage

1. **Generate API Key** (via web interface or API):
   ```bash
   curl -X POST http://localhost:5000/api/generate-key \
     -H "Content-Type: application/json" \
     -d '{"name": "My API Key"}'
   ```

2. **Build APK** using API:
   ```bash
   curl -X POST http://localhost:5000/api/v1/build-apk \
     -H "X-API-Key: apk_your_api_key_here" \
     -F "appName=My Awesome App" \
     -F "url=https://example.com" \
     -o myapp.apk
   ```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md) | Automated Windows setup guide |
| [BACKEND_SETUP.md](BACKEND_SETUP.md) | Backend setup and manual installation |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference |
| [KEYSTORE_SETUP.md](KEYSTORE_SETUP.md) | APK signing and keystore security |
| [AI_AGENT_CUSTOMIZATION_GUIDE.md](AI_AGENT_CUSTOMIZATION_GUIDE.md) | Adding new APK customizations |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11+** - Core language
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin support
- **BeautifulSoup4** - HTML parsing
- **Pillow** - Image processing
- **Requests** - HTTP client

### Android Tools
- **apktool 2.9.3** - APK decompilation/recompilation
- **Java JDK 21** - APK signing
- **Android SDK Build Tools 34.0.0** - apksigner

### Frontend
- **HTML5/CSS3/JavaScript** - Modern web interface
- **Responsive design** - Mobile-friendly UI

---

## 🔒 Security

### Development (Default)
- Uses default keystore for testing
- **NOT for production use**

### Production (Recommended)
Configure secure credentials via environment variables:

```bash
export KEYSTORE_PATH="/path/to/keystore.jks"
export KEYSTORE_ALIAS="production-key"
export KEYSTORE_PASS="secure-password"
export KEY_PASS="secure-password"
```

See [KEYSTORE_SETUP.md](KEYSTORE_SETUP.md) for complete security guide.

---

## 📊 System Requirements

### Windows (Automated Setup)
- Windows 10/11
- 4GB RAM minimum
- 2GB free disk space
- Internet connection for downloads
- Administrator privileges (recommended)

### Manual Setup (All Platforms)
- Python 3.11 or higher
- Java JDK 21
- apktool 2.9.3+
- Android SDK Build Tools 34.0.0
- 2GB free disk space

---

## 🚨 Troubleshooting

### Windows Setup Issues

**Problem**: Setup fails with "Permission denied"  
**Solution**: Run `setup_windows.bat` as Administrator

**Problem**: "Port 5000 already in use"  
**Solution**: 
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Problem**: Tools not recognized after installation  
**Solution**: Restart Command Prompt or reboot computer

### APK Build Issues

**Problem**: APK signing fails  
**Solution**: 
- Verify Java is installed: `java -version`
- Check apksigner: `apksigner`
- Verify keystore exists

**Problem**: Icon upload fails  
**Solution**: 
- Use PNG or JPG format
- Recommended size: 512x512 pixels
- Max file size: 2MB

See documentation for more troubleshooting guides.

---

## 🔄 Updating

### Update Python Dependencies
```bash
# Windows
venv\Scripts\activate
pip install --upgrade beautifulsoup4 flask flask-cors pillow requests

# Linux/Mac
source venv/bin/activate
pip install --upgrade beautifulsoup4 flask flask-cors pillow requests
```

### Update System Tools
Re-run the setup script to update all components:
```bash
# Windows
setup_windows.bat

# Or update manually as needed
```

---

## 🌟 Features Roadmap

- [ ] Multiple APK templates (splash screens, toolbars, etc.)
- [ ] Advanced customization options
- [ ] Batch APK generation
- [ ] APK analytics dashboard
- [ ] Rate limiting for API
- [ ] Database migration for high volume

---

## 📝 License

This project is designed for educational and development purposes. Make sure to:
- Use your own production keystore for distribution
- Follow Android signing best practices
- Respect website terms of service when converting

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional APK templates
- Enhanced customization options
- Performance optimizations
- Documentation improvements

---

## 📞 Support

### For Setup Issues
1. Check [WINDOWS_SETUP_GUIDE.md](WINDOWS_SETUP_GUIDE.md)
2. Review [BACKEND_SETUP.md](BACKEND_SETUP.md)
3. Verify all prerequisites are installed
4. Check firewall/antivirus settings

### For API Issues
1. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. Verify API key format and validity
3. Check server logs for errors
4. Test with curl examples

### For APK Issues
1. See [KEYSTORE_SETUP.md](KEYSTORE_SETUP.md)
2. Verify Java and apktool installation
3. Check Android compatibility
4. Review apksigner output

---

## 🎉 Quick Start Summary

### Windows (Simple Setup - Recommended)
```bash
1. python setup.py
2. Press Y to start server
3. Open http://localhost:5000
4. Generate your first APK!
```

### Manual (All Platforms)
```bash
1. Install Python 3.11+, Java 21, apktool, Android SDK
2. python -m venv venv
3. source venv/bin/activate  # or venv\Scripts\activate on Windows
4. pip install beautifulsoup4 flask flask-cors pillow requests
5. python backend/app.py
6. Open http://localhost:5000
```

### Replit (Easiest)
```bash
1. Click "Run" button
2. That's it! 🎉
```

---

**Built with ❤️ for easy Android app generation**

**Version**: 1.0  
**Last Updated**: October 2025  
**Status**: Production Ready ✅
