# URL to Android App Converter

## Overview
A public web application that converts any website URL into a fully functional Android application. Users can input a URL and receive a complete, ready-to-build Android Studio project that wraps the website in a secure WebView.

## Project Architecture

### Backend (Flask + Python)
- **Framework**: Flask with CORS support
- **Structure**:
  - `backend/app.py` - Main Flask application with API endpoints
  - `backend/services/url_metadata.py` - Fetches website metadata (title, favicon)
  - `backend/services/android_generator.py` - Generates Android project from template
  - `backend/services/zipper.py` - Creates ZIP files for download

### Frontend (HTML/CSS/JavaScript)
- **Location**: `frontend/` directory
- **Files**:
  - `index.html` - Main UI with form and feature display
  - `style.css` - Modern gradient styling with responsive design
  - `script.js` - Form handling and file download logic

### Android Template
- **Location**: `android_templates/` directory
- **Features**:
  - WebView with JavaScript enabled
  - Camera and geolocation permissions
  - File upload/download support
  - Pull-to-refresh functionality
  - Splash screen with app icon
  - Progress bar for loading
  - Cookie and storage support
  - Compatible with Android 6.0+ (API 23), targeting Android 14 (API 34)

## Key Features

### Generated Android Apps Include:
1. **WebView Integration**: Secure WebView with full JavaScript support
2. **Permissions**: Camera, location, file access, notifications
3. **UI Components**: Progress bar, pull-to-refresh, splash screen
4. **Customization**: Theme color, offline support
5. **Auto-configuration**: Package name auto-generated as `com.web2app.<sitename>`
6. **Favicon Integration**: Downloads and converts website favicon to app icon

## API Endpoints

### POST `/api/generate`
Generates an Android app from a URL
- **Request Body**:
  ```json
  {
    "url": "https://example.com",
    "appName": "Optional App Name",
    "themeColor": "#2196F3",
    "enableOffline": false
  }
  ```
- **Response**: ZIP file download of Android Studio project

### GET `/api/cleanup/<job_id>`
Cleans up generated files (optional cleanup endpoint)

## Technology Stack

### Backend Dependencies
- Flask - Web framework
- Flask-CORS - Cross-origin resource sharing
- Requests - HTTP library for URL fetching
- BeautifulSoup4 - HTML parsing for metadata
- Pillow - Image processing for favicon conversion

### Android Technologies
- Kotlin - Programming language
- Gradle 8.2 - Build system
- Android SDK 34 - Target platform
- AndroidX libraries - Modern Android components
- WebView - Web content rendering
- SwipeRefreshLayout - Pull-to-refresh

## Development

### Running Locally
The Flask server runs on port 5000 and serves both the API and frontend:
```bash
cd backend && python app.py
```

### Project Structure
```
.
├── backend/
│   ├── app.py
│   └── services/
│       ├── url_metadata.py
│       ├── android_generator.py
│       └── zipper.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── android_templates/
│   ├── app/
│   │   ├── build.gradle.kts
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/web2app/template/
│   │       │   ├── MainActivity.kt
│   │       │   └── SplashActivity.kt
│   │       └── res/
│   ├── build.gradle.kts
│   └── settings.gradle.kts
└── generated/ (temporary build directory)
```

## APK Builder System (NEW - October 14, 2025)

### Overview
Revolutionary APK modification system that builds custom Android APKs directly without Android SDK compilation. Users get instant APK downloads instead of ZIP files.

### Architecture
- **Base Versions**: Pre-built APK templates (`base_1.apk`, `base_2.apk`...) stored in `android_templates_apks/`
- **Auto-Detection**: Intelligently selects base version based on user's customization needs
- **Direct Modification**: Decompiles, modifies, recompiles, and signs APKs on-the-fly
- **Resource Efficient**: No heavy Android SDK builds, only lightweight APK modifications

### Components
1. **APK Builder** (`apk_builder/builder.py`)
   - Decompiles APK using apktool
   - Modifies app name, URL, icon, and other resources
   - Recompiles and signs APK with jarsigner
   
2. **Version Detector** (`apk_builder/version_detector.py`)
   - Auto-detects appropriate base version from user inputs
   - Matches customizations to base capabilities
   - Future-proof for multiple base versions

3. **Configuration** (`apk_builder/config.json`)
   - Defines base version capabilities
   - Maps customizations to base versions
   - Configures keystore for APK signing

### Base Version System
- **base_1**: Supports 3 customizations (app_name, url, icon)
- **base_2+**: Future versions with additional features (splash, toolbar, etc.)
- Automatic selection based on provided fields

### API Endpoints

#### POST `/api/build-apk` (NEW)
Builds custom APK with auto base-version detection
- **Request**: FormData with `appName`, `url`, optional `appIcon`
- **Response**: Signed APK file ready for installation
- **Features**: 
  - Auto-detects base version
  - Modifies app resources
  - Signs with keystore
  - Returns installable APK

#### POST `/api/generate` (Legacy)
Generates Android Studio project ZIP (still available)

### Tools & Dependencies
- **apktool 2.11.1**: APK decompilation/recompilation
- **Java 21 (OpenJDK)**: Required for apksigner
- **apksigner**: APK signing (v1 + v2 + v3 signatures)
- **Pillow**: Icon processing and resizing
- **Keystore**: Pre-generated signing key (`android_templates_apks/keystore.jks`)

### Security & Production Notes
- **Keystore Credentials**: Development credentials in config.json should be replaced with environment variables for production (see `KEYSTORE_SETUP.md`)
- **APK Signatures**: Uses apksigner with v1, v2, and v3 signing schemes enabled (MT Manager style)
- **Concurrency**: Each build uses unique temp directory to handle concurrent requests safely
- **Cleanup**: Automatic cleanup of temporary files after APK delivery

### For Future AI Agents
See `AI_AGENT_CUSTOMIZATION_GUIDE.md` for comprehensive guide on:
- Adding new base versions
- Adding new customizations
- Testing and deployment
- Version detection logic

## API System (NEW - October 14, 2025)

### Overview
Complete API key management system allowing external developers to integrate APK building service into their platforms.

### Features
- **API Key Generation**: Users can generate secure API keys from the web interface
- **Client-Side Storage**: API keys stored in browser localStorage for user convenience
- **Secure Authentication**: All external API endpoints protected with API key validation
- **Self-Service Revocation**: Users can revoke their own keys using the actual key
- **SHA-256 Hashing**: Keys stored as hashes, never in plain text
- **Request Tracking**: Monitors usage count and last used timestamp

### API Endpoints

#### Public Endpoints (No Auth Required)
- `POST /api/generate-key` - Generate new API key
- `POST /api/keys/verify` - Verify own API key (requires key)
- `POST /api/keys/revoke` - Revoke own API key (requires key)

#### Protected Endpoints (Require API Key)
- `POST /api/v1/build-apk` - Build custom APK (requires X-API-Key header)

#### Frontend Endpoints (No Auth Required)
- `POST /api/build-apk` - Build APK from web interface
- `POST /api/generate` - Legacy project ZIP generation

### Security Model
- **No Global Key Listing**: Prevents enumeration attacks
- **Self-Service Only**: Users can only manage their own keys
- **Key Verification**: Requires actual key to perform any operations
- **Hash Storage**: Only SHA-256 hashes stored in database
- **File-Based DB**: Simple JSON file storage in `db/api_keys.json`

### Documentation
- Full API documentation available at `/API_DOCUMENTATION.md`
- Includes code examples for Node.js, Python, PHP, Ruby, and Go
- Complete error handling and best practices guide

## Windows Automated Setup (NEW - October 15, 2025)

### Overview
Complete automated setup system for Windows users with zero manual configuration required.

### Files Created
1. **setup_windows.py** - Main Python setup script
   - Checks and installs Python 3.11+
   - Checks and installs Java JDK 21
   - Installs apktool 2.9.3
   - Installs Android SDK Build Tools 34.0.0
   - Creates virtual environment
   - Installs all dependencies
   - Creates required directories
   - Verifies all installations
   - Optionally starts server

2. **setup_windows.bat** - Batch file wrapper
   - Checks administrator privileges
   - Ensures Python is available
   - Runs the Python setup script
   - User-friendly error handling

3. **run_server.bat** - Quick server launcher
   - Activates virtual environment
   - Starts Flask server on port 5000
   - Easy stop/restart

4. **WINDOWS_SETUP_GUIDE.md** - Comprehensive documentation
   - Complete setup instructions
   - Troubleshooting guide
   - Verification commands
   - Security best practices

5. **README.md** - Main project documentation
   - Quick start for all platforms
   - Feature overview
   - API usage examples
   - Complete documentation index

### Features
- ✅ **Fully Automated**: One-click installation of all dependencies
- ✅ **Isolated Environment**: Python virtual environment prevents conflicts
- ✅ **Administrator Detection**: Warns if not running with admin privileges
- ✅ **Automatic Downloads**: Fetches all required tools (Python, Java, apktool, Android SDK)
- ✅ **PATH Configuration**: Automatically adds tools to system PATH
- ✅ **Verification System**: Checks all installations are working
- ✅ **Error Handling**: Clear error messages and troubleshooting guidance

### Usage
```bash
# Windows automated setup
Right-click setup_windows.bat → "Run as administrator"

# Or use Python script directly
python setup_windows.py
```

## Recent Changes (October 14-15, 2025)
- Initial project creation
- Implemented Flask backend with URL metadata fetching
- Created Android template with WebView and all required features
- Built responsive frontend with modern UI
- Added support for customization options (theme, offline)
- Configured workflow to run on port 5000
- **Fix**: Implemented offline support with cache mode based on enableOffline option
- **Feature**: Added custom icon upload functionality - users can upload their own app icon
- **Feature**: Added README.md and build scripts (build-apk.sh/.bat) to generated projects for easy APK building
- **Removal**: Removed all toolbar logic from frontend, backend, and Android templates
- **MAJOR**: Implemented APK Builder System for direct APK generation (no Android SDK needed!)
- **Feature**: Auto base-version detection based on user customizations
- **Optimization**: Cleaned up workspace (removed android-sdk, saved 405MB)
- **Security**: Upgraded APK signing from v1-only to v1+v2+v3 signing schemes (MT Manager style)
- **MAJOR**: Implemented complete API key management system for external developers
- **Security**: Fixed API key management with secure self-service revocation model
- **MAJOR**: Created comprehensive Windows automated setup system with Python and batch scripts
- **Documentation**: Added WINDOWS_SETUP_GUIDE.md and README.md with complete setup instructions

## User Preferences
- No authentication required (public website)
- Clean, modern UI with gradient design
- Automatic app naming from website domain
- Support for custom theme colors and preferences
