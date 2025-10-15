# APK Builder API Documentation

## 🚀 Overview

The APK Builder API allows you to programmatically convert any website URL into a fully functional Android APK. Integrate this service into your platform to offer instant APK generation to your users.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Code Examples](#code-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Support](#support)

---

## 🎯 Getting Started

### Base URL
```
https://your-domain.com/api/v1
```

### Requirements
- API Key (generate from the dashboard)
- HTTP client capable of multipart/form-data requests

### Quick Start

1. **Generate API Key**: Visit the web interface and click "Generate API Key"
2. **Save Your Key**: Copy and securely store your API key (you won't see it again!)
3. **Make Your First Request**: Use the API key in the `X-API-Key` header

---

## 🔐 Authentication

All API requests require authentication using an API key.

### Methods

#### Option 1: Header Authentication (Recommended)
```http
X-API-Key: apk_your_api_key_here
```

#### Option 2: Query Parameter
```http
?api_key=apk_your_api_key_here
```

### Example Request
```bash
curl -X POST https://your-domain.com/api/v1/build-apk \
  -H "X-API-Key: apk_your_api_key_here" \
  -F "appName=My Awesome App" \
  -F "url=https://example.com"
```

---

## 📡 API Endpoints

### 1. Build APK

**Endpoint:** `POST /api/v1/build-apk`

**Description:** Generate a custom Android APK from a website URL.

**Authentication:** Required

**Request Format:** `multipart/form-data`

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `appName` | string | Yes | Name of the Android application |
| `url` | string | Yes | Website URL to convert (with or without protocol) |
| `appIcon` | file | No | Custom app icon (PNG/JPG, square recommended) |

#### Response

**Success (200 OK):**
- Content-Type: `application/vnd.android.package-archive`
- Body: Binary APK file

**Error (400 Bad Request):**
```json
{
  "error": "URL is required"
}
```

**Error (401 Unauthorized):**
```json
{
  "error": "API key is required",
  "message": "Please provide your API key via X-API-Key header or api_key query parameter"
}
```

**Error (403 Forbidden):**
```json
{
  "error": "Invalid or inactive API key",
  "message": "The provided API key is not valid or has been revoked"
}
```

#### Example Request (cURL)

```bash
# Basic request
curl -X POST https://your-domain.com/api/v1/build-apk \
  -H "X-API-Key: apk_your_api_key_here" \
  -F "appName=My App" \
  -F "url=https://example.com" \
  -o myapp.apk

# With custom icon
curl -X POST https://your-domain.com/api/v1/build-apk \
  -H "X-API-Key: apk_your_api_key_here" \
  -F "appName=My App" \
  -F "url=https://example.com" \
  -F "appIcon=@/path/to/icon.png" \
  -o myapp.apk
```

---

## 💻 Code Examples

### JavaScript (Node.js)

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function buildAPK() {
  const form = new FormData();
  form.append('appName', 'My Awesome App');
  form.append('url', 'https://example.com');
  
  // Optional: Add custom icon
  // form.append('appIcon', fs.createReadStream('./icon.png'));

  try {
    const response = await axios({
      method: 'post',
      url: 'https://your-domain.com/api/v1/build-apk',
      headers: {
        'X-API-Key': 'apk_your_api_key_here',
        ...form.getHeaders()
      },
      data: form,
      responseType: 'arraybuffer'
    });

    // Save APK file
    fs.writeFileSync('myapp.apk', response.data);
    console.log('APK built successfully!');
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

buildAPK();
```

### Python

```python
import requests

def build_apk():
    url = "https://your-domain.com/api/v1/build-apk"
    
    headers = {
        "X-API-Key": "apk_your_api_key_here"
    }
    
    data = {
        "appName": "My Awesome App",
        "url": "https://example.com"
    }
    
    # Optional: Add custom icon
    # files = {"appIcon": open("icon.png", "rb")}
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        with open("myapp.apk", "wb") as f:
            f.write(response.content)
        print("APK built successfully!")
    else:
        print(f"Error: {response.json()}")

build_apk()
```

### PHP

```php
<?php

function buildAPK() {
    $url = "https://your-domain.com/api/v1/build-apk";
    
    $ch = curl_init();
    
    $data = [
        'appName' => 'My Awesome App',
        'url' => 'https://example.com',
        // Optional: Add custom icon
        // 'appIcon' => new CURLFile('/path/to/icon.png')
    ];
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'X-API-Key: apk_your_api_key_here'
    ]);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    curl_close($ch);
    
    if ($httpCode === 200) {
        file_put_contents('myapp.apk', $response);
        echo "APK built successfully!";
    } else {
        echo "Error: " . $response;
    }
}

buildAPK();
?>
```

### Ruby

```ruby
require 'httparty'

def build_apk
  url = "https://your-domain.com/api/v1/build-apk"
  
  response = HTTParty.post(url,
    headers: {
      'X-API-Key' => 'apk_your_api_key_here'
    },
    body: {
      appName: 'My Awesome App',
      url: 'https://example.com'
      # Optional: appIcon: File.new('icon.png')
    }
  )
  
  if response.code == 200
    File.open('myapp.apk', 'wb') { |file| file.write(response.body) }
    puts "APK built successfully!"
  else
    puts "Error: #{response.body}"
  end
end

build_apk
```

### Go

```go
package main

import (
    "bytes"
    "fmt"
    "io"
    "mime/multipart"
    "net/http"
    "os"
)

func buildAPK() error {
    url := "https://your-domain.com/api/v1/build-apk"
    
    var b bytes.Buffer
    w := multipart.NewWriter(&b)
    
    // Add form fields
    w.WriteField("appName", "My Awesome App")
    w.WriteField("url", "https://example.com")
    
    // Optional: Add custom icon
    // fw, _ := w.CreateFormFile("appIcon", "icon.png")
    // file, _ := os.Open("icon.png")
    // io.Copy(fw, file)
    
    w.Close()
    
    req, _ := http.NewRequest("POST", url, &b)
    req.Header.Set("X-API-Key", "apk_your_api_key_here")
    req.Header.Set("Content-Type", w.FormDataContentType())
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    if resp.StatusCode == 200 {
        out, _ := os.Create("myapp.apk")
        defer out.Close()
        io.Copy(out, resp.Body)
        fmt.Println("APK built successfully!")
    } else {
        body, _ := io.ReadAll(resp.Body)
        fmt.Printf("Error: %s\n", body)
    }
    
    return nil
}

func main() {
    buildAPK()
}
```

---

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success - APK file returned |
| 400 | Bad Request - Missing or invalid parameters |
| 401 | Unauthorized - Missing API key |
| 403 | Forbidden - Invalid or revoked API key |
| 500 | Internal Server Error - Server-side issue |

### Error Response Format

```json
{
  "error": "Error type",
  "message": "Detailed error description"
}
```

### Common Errors

#### Missing API Key
```json
{
  "error": "API key is required",
  "message": "Please provide your API key via X-API-Key header or api_key query parameter"
}
```

#### Invalid API Key
```json
{
  "error": "Invalid or inactive API key",
  "message": "The provided API key is not valid or has been revoked"
}
```

#### Missing Required Field
```json
{
  "error": "URL is required"
}
```

---

## 📋 Best Practices

### 1. **Secure Your API Key**
- Never expose API keys in client-side code
- Store keys in environment variables or secure vaults
- Use server-side proxies for client applications

### 2. **Handle Errors Gracefully**
- Implement proper error handling for all API calls
- Provide user-friendly error messages
- Log errors for debugging

### 3. **Optimize Icon Files**
- Use square images (1:1 aspect ratio)
- Recommended size: 512x512 pixels
- Supported formats: PNG, JPG
- Keep file size under 2MB

### 4. **URL Format**
- Include protocol (https:// or http://)
- Ensure URL is accessible and valid
- Test URLs before sending to API

### 5. **Rate Limiting**
- Be mindful of API usage
- Implement caching where appropriate
- Contact support for high-volume needs

---

## 🔧 APK Features

Generated APKs include:

- ✅ **WebView Integration** - Full JavaScript support
- ✅ **Pull to Refresh** - Swipe down to reload
- ✅ **Camera Access** - File upload and camera permissions
- ✅ **Geolocation** - Location permissions included
- ✅ **Cookies & Storage** - Persistent data and cookies
- ✅ **Custom Splash Screen** - Branded app launch
- ✅ **v1 + v2 + v3 Signatures** - Full Android compatibility

**Compatibility:** Android 6.0+ (API 23) | Target: Android 14 (API 34)

---

## 📞 Support

### Documentation
- Web Interface: [https://your-domain.com](https://your-domain.com)
- API Docs: [https://your-domain.com/API_DOCUMENTATION.md](https://your-domain.com/API_DOCUMENTATION.md)

### Getting Help
- Review this documentation thoroughly
- Check error responses for specific issues
- Ensure all required parameters are provided

### API Key Management
- Generate new keys from the web interface
- Revoke compromised keys immediately
- Monitor usage in the dashboard

---

## 🎉 Quick Integration Checklist

- [ ] Generate API key from dashboard
- [ ] Securely store API key
- [ ] Test API with simple request
- [ ] Implement error handling
- [ ] Add custom icon support (optional)
- [ ] Deploy to production

---

**Last Updated:** October 2025  
**API Version:** 1.0

---

## Example Integration Flow

```
1. User enters website URL in your app
       ↓
2. Your backend calls APK Builder API
       ↓
3. API validates request and builds APK
       ↓
4. APK file returned to your backend
       ↓
5. You deliver APK to user
```

---

*Built with ❤️ for developers who want to convert websites to Android apps instantly.*
