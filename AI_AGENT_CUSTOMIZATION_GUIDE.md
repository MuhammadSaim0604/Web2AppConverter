# AI Agent Guide: Adding New Customizations to APK Builder System

## 📋 Overview

This guide helps AI agents understand how to add new customizations to the APK builder system. The system automatically detects which base version to use based on user inputs.

---

## 🏗️ System Architecture

```
User Input → Version Detector → APK Builder → Signed APK
                    ↓
            Auto-selects base version
            (base_1, base_2, base_3...)
```

### Current Structure:
- **base_1.apk**: Supports 3 customizations (app_name, url, icon)
- **base_2.apk**: (Future) Will support 5+ customizations
- **base_N.apk**: (Future) More advanced customizations

---

## 🔧 How to Add New Customizations

### Step 1: Build New Base APK in Android Studio

1. **Modify Android Template** in `android_templates/`:
   - Add new features (splash screen, toolbar, notifications, etc.)
   - Keep the template structure intact
   - Use placeholder values like `{{SPLASH_IMAGE}}`, `{{TOOLBAR_COLOR}}`, etc.

2. **Build APK**:
   ```bash
   # In Android Studio
   Build → Build Bundle(s) / APK(s) → Build APK(s)
   ```

3. **Place APK**:
   - Copy built APK to `android_templates_apks/`
   - Name it: `base_2.apk` (or next version number)

---

### Step 2: Update Configuration

Edit `apk_builder/config.json`:

```json
{
  "base_versions": {
    "base_1": {
      "apk_path": "android_templates_apks/base_1.apk",
      "customizations": ["app_name", "url", "icon"],
      "required_fields": ["app_name", "url"],
      "optional_fields": ["icon"]
    },
    "base_2": {
      "apk_path": "android_templates_apks/base_2.apk",
      "customizations": ["app_name", "url", "icon", "splash_screen", "toolbar_color"],
      "required_fields": ["app_name", "url"],
      "optional_fields": ["icon", "splash_screen", "toolbar_color"]
    }
  },
  ...
}
```

**Important Fields:**
- `customizations`: List ALL customizations this base supports
- `required_fields`: Must be provided by user
- `optional_fields`: Can be empty/null

---

### Step 3: Add Modification Logic

Edit `apk_builder/builder.py` and add new methods:

```python
def modify_splash_screen(self, splash_image_path):
    """Add custom splash screen"""
    if not splash_image_path or not os.path.exists(splash_image_path):
        return False
    
    if not self.decompiled_dir:
        raise Exception("APK not decompiled yet")
    
    # Your modification logic here
    splash_dir = self.decompiled_dir / 'res' / 'drawable'
    splash_dir.mkdir(parents=True, exist_ok=True)
    
    # Process and save splash image
    # ... your code ...
    
    return True

def modify_toolbar_color(self, color_hex):
    """Modify toolbar color"""
    if not self.decompiled_dir:
        raise Exception("APK not decompiled yet")
    
    # Find and modify color resources
    colors_xml = self.decompiled_dir / 'res' / 'values' / 'colors.xml'
    
    with open(colors_xml, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace toolbar color
    content = re.sub(
        r'(<color name="toolbar_color">).*?(</color>)',
        rf'\1{color_hex}\2',
        content
    )
    
    with open(colors_xml, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True
```

**Then update the `build()` method:**

```python
def build(self, app_name, url, icon_path=None, splash_screen=None, toolbar_color=None):
    """Complete build process with new customizations"""
    try:
        # ... existing code ...
        
        # New customizations
        if splash_screen:
            print("X. Adding splash screen...")
            self.modify_splash_screen(splash_screen)
        
        if toolbar_color:
            print("Y. Setting toolbar color...")
            self.modify_toolbar_color(toolbar_color)
        
        # ... rest of the code ...
```

---

### Step 4: Update Backend API

Edit `backend/app.py` to accept new fields:

```python
@app.route('/api/build-apk', methods=['POST'])
def build_custom_apk():
    try:
        # Existing fields
        url = request.form.get('url', '').strip()
        app_name = request.form.get('appName', '').strip()
        uploaded_icon = request.files.get('appIcon')
        
        # NEW FIELDS
        toolbar_color = request.form.get('toolbarColor', '').strip()
        splash_screen = request.files.get('splashScreen')
        
        # Add to user_inputs for version detection
        user_inputs = {
            'app_name': app_name,
            'url': url,
            'icon': icon_path if uploaded_icon else None,
            'toolbar_color': toolbar_color if toolbar_color else None,
            'splash_screen': splash_path if splash_screen else None
        }
        
        # Auto-detect will now choose base_2 if these fields are provided!
        base_version = detector.detect_base_version(user_inputs)
        
        # Build with new parameters
        apk_path = build_apk(
            app_name=app_name,
            url=url,
            icon_path=icon_path,
            splash_screen=splash_path,
            toolbar_color=toolbar_color,
            base_version=base_version
        )
        
        # ... rest of code ...
```

---

### Step 5: Update Frontend (if needed)

If frontend needs new input fields, edit `frontend/index.html`:

```html
<!-- Add new form fields -->
<div class="form-group">
  <label>Toolbar Color</label>
  <input type="color" name="toolbarColor" id="toolbarColor">
</div>

<div class="form-group">
  <label>Splash Screen</label>
  <input type="file" name="splashScreen" id="splashScreen" accept="image/*">
</div>
```

And update the form submission to include these fields.

---

## 🧪 Testing New Customizations

1. **Test Version Detection**:
```python
from apk_builder.version_detector import VersionDetector

detector = VersionDetector()

# Test with new fields
inputs = {
    'app_name': 'Test',
    'url': 'https://example.com',
    'icon': '/path/to/icon.png',
    'splash_screen': '/path/to/splash.png',
    'toolbar_color': '#FF5722'
}

version = detector.detect_base_version(inputs)
print(f"Detected version: {version}")  # Should be base_2
```

2. **Test APK Building**:
```python
from apk_builder.builder import build_apk

apk_path = build_apk(
    app_name='My App',
    url='https://example.com',
    icon_path='/path/to/icon.png',
    splash_screen='/path/to/splash.png',
    toolbar_color='#FF5722',
    base_version='base_2'
)

print(f"APK created: {apk_path}")
```

3. **Test via API**:
```bash
curl -X POST http://localhost:5000/api/build-apk \
  -F "appName=My App" \
  -F "url=https://example.com" \
  -F "appIcon=@icon.png" \
  -F "splashScreen=@splash.png" \
  -F "toolbarColor=#FF5722" \
  --output my_app.apk
```

---

## 📝 Version Detection Logic

The `VersionDetector` auto-selects base version by:

1. **Checking required fields**: All required fields must be present
2. **Matching customizations**: Finds base version that supports all provided fields
3. **Fallback**: If no exact match, uses `base_1` as default

### Example Decision Tree:

```
User provides: [app_name, url, icon]
→ Matches base_1 ✓

User provides: [app_name, url, icon, splash_screen]
→ base_1 only has 3 customizations ✗
→ base_2 has 5+ customizations ✓
→ Selects base_2

User provides: [app_name, url, icon, splash_screen, toolbar_color, push_notifications]
→ base_2 only has 5 customizations ✗
→ base_3 has 8+ customizations ✓
→ Selects base_3
```

---

## 🗂️ File Structure Reference

```
project/
├── android_templates/           # Android source templates
│   └── app/src/main/           # Modify here for new features
├── android_templates_apks/      # Base APK storage
│   ├── base_1.apk              # 3 customizations
│   ├── base_2.apk              # (future) 5+ customizations
│   └── keystore.jks            # Signing key
├── apk_builder/
│   ├── config.json             # Version configurations
│   ├── version_detector.py     # Auto-detection logic
│   └── builder.py              # APK modification logic
└── backend/
    └── app.py                  # API endpoints
```

---

## ⚠️ Important Notes

1. **Base Version Naming**: Always use `base_N` format (base_1, base_2, base_3...)

2. **Backward Compatibility**: New base versions should support ALL customizations from previous versions + new ones

3. **Required vs Optional**: 
   - `app_name` and `url` are always required
   - Other fields should be optional

4. **Concurrency**: 
   - Each build uses unique temp directory (`tempfile.mkdtemp()`)
   - Never use shared workspaces
   - Always cleanup after completion

5. **Security**:
   - Use environment variables for keystore credentials in production
   - See `KEYSTORE_SETUP.md` for security best practices
   - Never commit production keystores to git

6. **APK Signing**:
   - Current: v1 + v2 + v3 signatures (apksigner) - full compatibility with all devices
   - Production-ready signing (MT Manager style)
   - See `KEYSTORE_SETUP.md` for security best practices

7. **File Cleanup**: Always cleanup temporary files after APK generation

8. **Error Handling**: Add proper try-catch blocks and meaningful error messages

9. **Testing**: Test each new customization independently before combining

10. **Documentation**: Update this guide when adding new customization types

---

## 🚀 Quick Checklist for Adding Customizations

- [ ] Build new Android template with features
- [ ] Export APK and place in `android_templates_apks/`
- [ ] Update `apk_builder/config.json`
- [ ] Add modification methods in `apk_builder/builder.py`
- [ ] Update `backend/app.py` API endpoint
- [ ] Update frontend forms (if needed)
- [ ] Test version detection
- [ ] Test APK building
- [ ] Test via API
- [ ] Update this documentation

---

## 📞 Support

For questions or issues, refer to:
- `apk_builder/builder.py` - Core modification logic
- `apk_builder/version_detector.py` - Auto-detection algorithm
- `apk_builder/config.json` - Version configurations

---

**Happy Customizing! 🎉**

*Last Updated: October 2025*
*System Version: 1.0*
