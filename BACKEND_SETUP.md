
# Backend Setup Documentation

## 📋 Overview

This document provides complete instructions for setting up and running the URL to Android App Converter backend. The backend is built with Flask and provides both a web interface and a REST API for converting websites into Android APKs.

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python**: 3.11 or higher
- **Java**: OpenJDK 21 (for APK signing)
- **apktool**: 2.11.1 (pre-installed in Replit environment)
- **Replit Account**: For deployment

### 2. Installation

The project uses `pyproject.toml` for dependency management. All dependencies are automatically installed in the Replit environment.

**Core Dependencies:**
```toml
beautifulsoup4>=4.14.2
flask>=3.1.2
flask-cors>=6.0.1
pillow>=11.3.0
requests>=2.32.5
```

### 3. Running the Server

#### On Replit (Recommended)

Simply click the **Run** button. The workflow is pre-configured to start the Flask server on port 5000.

#### Manual Start

```bash
python3 backend/app.py
```

The server will start on `http://0.0.0.0:5000` and be accessible via your Replit domain.

---

## 📁 Project Structure

```
backend/
├── app.py                  # Main Flask application
├── api_key_manager.py      # API key management system
└── services/
    ├── url_metadata.py     # URL metadata extraction
    ├── android_generator.py # Android project generation
    └── zipper.py           # ZIP file creation

apk_builder/
├── builder.py              # APK modification system
├── version_detector.py     # Base version auto-detection
└── config.json            # APK builder configuration

android_templates_apks/
├── base_1.apk             # Base APK template
└── keystore.jks           # Signing keystore

db/
└── api_keys.json          # API keys database
```

---

## 🔧 Configuration

### Environment Setup

The backend automatically configures itself based on the environment. No `.env` file is required for basic operation.

### Keystore Configuration (Production)

For production deployment, configure secure keystore credentials:

**Option 1: Environment Variables (Recommended)**

```bash
export KEYSTORE_PATH="/path/to/your/keystore.jks"
export KEYSTORE_ALIAS="your-key-alias"
export KEYSTORE_PASS="your-store-password"
export KEY_PASS="your-key-password"
```

**Option 2: Update config.json**

Edit `apk_builder/config.json`:
```json
{
  "keystore": {
    "path": "android_templates_apks/keystore.jks",
    "alias": "your-alias",
    "store_pass": "your-password",
    "key_pass": "your-password"
  }
}
```

⚠️ **Security Note**: Never commit production keystores to version control. See `KEYSTORE_SETUP.md` for details.

---

## 🌐 API Endpoints

### Public Endpoints (No Authentication)

#### 1. **Web Interface**
- **GET** `/` - Main web interface
- **GET** `/API_DOCUMENTATION.md` - API documentation

#### 2. **APK Generation (Web)**
```http
POST /api/build-apk
Content-Type: multipart/form-data

appName: "My App"
url: "https://example.com"
appIcon: [file] (optional)
```

#### 3. **API Key Management**

**Generate API Key:**
```http
POST /api/generate-key
Content-Type: application/json

{
  "name": "My API Key"
}
```

**Verify API Key:**
```http
POST /api/keys/verify
Content-Type: application/json

{
  "api_key": "apk_your_api_key_here"
}
```

**Revoke API Key:**
```http
POST /api/keys/revoke
Content-Type: application/json

{
  "api_key": "apk_your_api_key_here"
}
```

### Protected Endpoints (Require API Key)

#### APK Generation (API)
```http
POST /api/v1/build-apk
X-API-Key: apk_your_api_key_here
Content-Type: multipart/form-data

appName: "My App"
url: "https://example.com"
appIcon: [file] (optional)
```

**Authentication Methods:**
- Header: `X-API-Key: apk_your_api_key_here`
- Query Parameter: `?api_key=apk_your_api_key_here`

---

## 🔐 API Key System

### How It Works

1. **Generation**: Users generate API keys via the web interface
2. **Storage**: Keys are hashed with SHA-256 and stored in `db/api_keys.json`
3. **Validation**: Each request validates the key hash
4. **Tracking**: Tracks usage count and last used timestamp
5. **Revocation**: Users can revoke their own keys

### API Key Format

```
apk_[64 character hex string]
```

Example: `apk_a1b2c3d4e5f6...`

### Database Schema

```json
{
  "api_keys": [
    {
      "key_id": "unique_id",
      "key_hash": "sha256_hash",
      "name": "Key Name",
      "created_at": "ISO timestamp",
      "last_used": "ISO timestamp",
      "request_count": 0,
      "active": true
    }
  ]
}
```

---

## 🏗️ APK Building System

### Architecture

The APK builder uses a template-based approach:

1. **Base APKs**: Pre-built APK templates in `android_templates_apks/`
2. **Auto-Detection**: Automatically selects base version based on customizations
3. **Modification**: Decompiles, modifies resources, recompiles
4. **Signing**: Signs APK with v1+v2+v3 signatures

### Build Process

```python
# 1. Auto-detect base version
detector = VersionDetector()
base_version = detector.detect_base_version(user_inputs)

# 2. Build APK
builder = APKBuilder(base_version=base_version)
apk_path = builder.build(
    app_name="My App",
    url="https://example.com",
    icon_path="/path/to/icon.png"  # Optional
)

# 3. Cleanup
builder.cleanup()
```

### Supported Customizations

- **App Name**: Custom application name
- **URL**: Target website URL
- **Icon**: Custom app icon (PNG/JPG, recommended 512x512)

---

## 🛠️ Development

### Running in Debug Mode

The server runs in debug mode by default:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Adding New Endpoints

```python
@app.route('/api/your-endpoint', methods=['POST'])
def your_endpoint():
    try:
        data = request.get_json()
        # Your logic here
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Error Handling

All endpoints use try-except blocks with JSON error responses:

```python
return jsonify({'error': 'Error message'}), status_code
```

---

## 📊 Monitoring & Logs

### Console Logs

The server logs all activities to console:

```
Starting APK build process...
1. Cleaning up workspace...
2. Decompiling base APK...
3. Setting app name to: My App
4. Setting URL to: https://example.com
5. Skipping icon replacement (not provided)
6. Recompiling APK...
7. Signing APK (v1 + v2 + v3 signatures)...
✓ APK build complete: /tmp/apk_build_xxx/signed.apk
```

### API Key Usage

Track API key usage in `db/api_keys.json`:
- `request_count`: Total requests made
- `last_used`: Last request timestamp

---

## 🔒 Security Best Practices

### 1. Keystore Security
- Use environment variables for production credentials
- Never commit `config.json` with production passwords
- Rotate keys periodically

### 2. API Key Management
- Keys are stored as SHA-256 hashes, never in plain text
- Implement rate limiting for production (not included by default)
- Monitor suspicious activity via `request_count`

### 3. File Upload Security
- Validates file types (PNG/JPG for icons)
- Uses `secure_filename()` for uploaded files
- Automatic cleanup of temporary files

---

## 🚀 Deployment on Replit

### 1. Deployment Configuration

The deployment is configured in `.replit`:

```toml
[deployment]
run = ["python3", "backend/app.py"]

[[ports]]
localPort = 5000
externalPort = 80
```

### 2. Publishing Your App

1. Click **Deploy** in the Replit workspace
2. Choose **Autoscale** deployment
3. Configure:
   - **Machine**: 1vCPU, 2GB RAM (default)
   - **Run Command**: `python3 backend/app.py`
   - **Primary Domain**: Choose your domain

4. Click **Deploy**

### 3. Environment Variables (Production)

Add environment variables in Replit Secrets:

```
KEYSTORE_PATH=/path/to/keystore.jks
KEYSTORE_ALIAS=production-key
KEYSTORE_PASS=secure_password
KEY_PASS=secure_password
```

---

## 🧪 Testing

### Test API Key Generation

```bash
curl -X POST http://localhost:5000/api/generate-key \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Key"}'
```

### Test APK Building

```bash
curl -X POST http://localhost:5000/api/v1/build-apk \
  -H "X-API-Key: apk_your_key_here" \
  -F "appName=Test App" \
  -F "url=https://example.com" \
  -o test.apk
```

### Test Frontend

Visit `http://localhost:5000` in your browser and use the web interface.

---

## 📚 Additional Resources

- **API Documentation**: `/API_DOCUMENTATION.md`
- **Keystore Setup**: `KEYSTORE_SETUP.md`
- **AI Agent Guide**: `AI_AGENT_CUSTOMIZATION_GUIDE.md`
- **Service Status**: Check logs in Replit console

---

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Kill process on port 5000
kill -9 $(lsof -ti:5000)
```

**2. APK Build Fails**
- Check Java is installed: `java -version`
- Verify apktool: `apktool --version`
- Check keystore exists: `ls android_templates_apks/keystore.jks`

**3. API Key Not Working**
- Verify key format starts with `apk_`
- Check key is active in `db/api_keys.json`
- Ensure header is `X-API-Key` (case-sensitive)

**4. Icon Upload Issues**
- Use PNG or JPG format
- Recommended size: 512x512 pixels
- Maximum file size: 2MB

---

## 💡 Tips

1. **Development**: Use the web interface at `/` for quick testing
2. **Production**: Always use environment variables for sensitive data
3. **Scaling**: Monitor `db/api_keys.json` size, consider database migration for high volume
4. **Backup**: Regularly backup `db/api_keys.json` and keystores

---

## 📞 Support

For issues or questions:
1. Check console logs in Replit
2. Review error messages in API responses
3. Consult `API_DOCUMENTATION.md` for endpoint details
4. Refer to `KEYSTORE_SETUP.md` for signing issues

---

**Last Updated**: October 2025  
**Version**: 1.0  
**Status**: Production Ready ✅
