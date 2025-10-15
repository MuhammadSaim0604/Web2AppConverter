# Keystore Configuration and Security

## ⚠️ Security Notice

The keystore credentials in `apk_builder/config.json` are **default development credentials** and should be replaced for production use.

## Production Setup

### Option 1: Environment Variables (Recommended)

Set these environment variables in your production environment:

```bash
export KEYSTORE_PATH="/path/to/your/keystore.jks"
export KEYSTORE_ALIAS="your-key-alias"
export KEYSTORE_PASS="your-store-password"
export KEY_PASS="your-key-password"
```

The system will automatically use environment variables if available, falling back to config.json values for development.

### Option 2: Replace Keystore File

1. Generate your own production keystore:
```bash
keytool -genkeypair -v \
  -keystore android_templates_apks/keystore.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias your-alias \
  -storepass your-store-pass \
  -keypass your-key-pass \
  -dname "CN=YourName, OU=YourUnit, O=YourOrg, L=City, ST=State, C=US"
```

2. Update `apk_builder/config.json` with your credentials

3. **Important**: Add `apk_builder/config.json` to `.gitignore` if credentials are sensitive

## Current Default Credentials (Development Only)

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

⚠️ **DO NOT USE THESE IN PRODUCTION!**

## APK Signing Information

### Current Implementation
- Uses **apksigner** with v1, v2, and v3 signing schemes enabled
- Full compatibility with all Android devices (v1) and modern Android versions (v2/v3)
- Production-ready signing (similar to MT Manager)

### Additional Production Recommendations
For enhanced security in production:
1. Using Google Play App Signing
2. Using a hardware security module (HSM) for key storage

## Verification

Check current keystore:
```bash
keytool -list -v -keystore android_templates_apks/keystore.jks -storepass android123
```

Verify APK signature:
```bash
apksigner verify --verbose your_app.apk
```

## Best Practices

1. ✅ Use environment variables for production
2. ✅ Rotate keys periodically
3. ✅ Keep keystore backups in secure location
4. ✅ Use different keystores for dev/staging/prod
5. ❌ Never commit production keystores to git
6. ❌ Never share keystore passwords in plain text

---

*Last Updated: October 2025*
