# {{APP_NAME}} - Android App

This is an automatically generated Android application that wraps **{{URL}}** in a native WebView.

## Quick Start

### Option 1: Build with Android Studio (Recommended)
1. Download and install [Android Studio](https://developer.android.com/studio)
2. Open this project folder in Android Studio
3. Wait for Gradle sync to complete
4. Click the green ▶ **Run** button to test on emulator or device
5. Go to **Build → Build Bundle(s) / APK(s) → Build APK(s)** to generate the APK
6. Find your APK in `app/build/outputs/apk/debug/`

### Option 2: Build from Command Line (Advanced)
**Windows:**
```bash
gradlew.bat assembleDebug
```

**Mac/Linux:**
```bash
chmod +x gradlew
./gradlew assembleDebug
```

The APK will be generated in: `app/build/outputs/apk/debug/app-debug.apk`

## Features Included

✅ **WebView Integration** - Loads {{URL}} with full JavaScript support  
✅ **Pull to Refresh** - Swipe down to reload  
✅ **Camera Access** - Permission for camera usage  
✅ **Geolocation** - Location permission included  
✅ **File Uploads/Downloads** - Full file handling support  
✅ **Cookies & Storage** - Persistent data storage  
✅ **Splash Screen** - Branded loading screen  
✅ **Custom Theme** - Themed with your chosen color  

## App Configuration

- **Package Name:** {{PACKAGE_NAME}}
- **App Name:** {{APP_NAME}}
- **URL:** {{URL}}
- **Theme Color:** {{THEME_COLOR}}
- **Min SDK:** Android 6.0 (API 23)
- **Target SDK:** Android 14 (API 34)

## Customization

### Change the URL
Edit `app/src/main/java/.../MainActivity.kt` and update:
```kotlin
webView.loadUrl("{{URL}}")
```

### Change App Name
Edit `app/src/main/res/values/strings.xml`:
```xml
<string name="app_name">Your New Name</string>
```

### Change Theme Color
Edit `app/src/main/res/values/colors.xml`:
```xml
<color name="primary">#YourColor</color>
```

### Change App Icon
Replace the icon files in `app/src/main/res/mipmap-*/ic_launcher.png`

## Testing on Real Device

1. Enable **Developer Options** on your phone:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
2. Enable **USB Debugging** in Developer Options
3. Connect your phone via USB
4. Select your device in Android Studio and click Run

## Building Release APK

For a signed release APK:

1. Generate a keystore:
```bash
keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-alias
```

2. Add to `app/build.gradle.kts`:
```kotlin
signingConfigs {
    create("release") {
        storeFile = file("my-release-key.jks")
        storePassword = "your-password"
        keyAlias = "my-alias"
        keyPassword = "your-password"
    }
}
```

3. Build:
```bash
./gradlew assembleRelease
```

## Troubleshooting

**Gradle sync failed?**
- Make sure you have an internet connection
- Check that Java 11 or higher is installed
- Try: File → Invalidate Caches → Restart

**App crashes on startup?**
- Check LogCat in Android Studio for errors
- Ensure the URL is accessible
- Verify permissions are granted on device

## Support

For Android development help:
- [Android Developers Guide](https://developer.android.com/guide)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/android)

---

Generated with ❤️ by URL to Android App Converter
