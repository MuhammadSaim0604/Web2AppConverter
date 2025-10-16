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

### How It Works (Async Workflow)

The API uses an **asynchronous job-based system** to handle APK builds:

1. **Create Job** → Call `/api/v1/build-apk` to create a build job
2. **Get Links** → Receive `job_id`, `download_url`, and `status_url` immediately
3. **Monitor Progress** → Poll `/api/v1/status/{job_id}` to check build status
4. **Download APK** → Use `/api/v1/download/{job_id}` to get APK when ready

**Why Async?** APK building can take 10-20 minutes on free tier (0.1 CPU), so you get the download link immediately and check when it's ready!

### Quick Start

1. **Generate API Key**: Visit the web interface and click "Generate API Key"
2. **Save Your Key**: Copy and securely store your API key (you won't see it again!)
3. **Create Build Job**: POST to `/api/v1/build-apk` with your API key
4. **Get Download Link**: Response includes `download_url` - save it!
5. **Check Status**: Poll the `status_url` or try downloading directly
6. **Download APK**: When ready, the `download_url` will return your APK file

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

### 1. Build APK (Async)

**Endpoint:** `POST /api/v1/build-apk`

**Description:** Create an APK build job and get download link immediately. The APK builds in background.

**Authentication:** Required

**Request Format:** `multipart/form-data`

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `appName` | string | Yes | Name of the Android application |
| `url` | string | Yes | Website URL to convert (with or without protocol) |
| `appIcon` | file | No | Custom app icon (PNG/JPG, square recommended) |

#### Response

**Success (202 Accepted):**
```json
{
  "success": true,
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "download_url": "https://your-domain.com/api/v1/download/550e8400-e29b-41d4-a716-446655440000",
  "status_url": "https://your-domain.com/api/v1/status/550e8400-e29b-41d4-a716-446655440000",
  "message": "APK build job created successfully. Use the download_url to get your APK.",
  "app_name": "My App",
  "url": "https://example.com"
}
```

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
# Create APK build job
curl -X POST https://your-domain.com/api/v1/build-apk \
  -H "X-API-Key: apk_your_api_key_here" \
  -F "appName=My App" \
  -F "url=https://example.com"

# Response will include download_url - use it to download APK when ready
```

---

### 2. Check Build Status

**Endpoint:** `GET /api/v1/status/{job_id}`

**Description:** Get current status of APK build job.

**Authentication:** Not required

#### Response

**Success (200 OK):**
```json
{
  "success": true,
  "job": {
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "app_name": "My App",
    "url": "https://example.com",
    "status": "processing",
    "progress": 45,
    "message": "Building APK...",
    "error": null,
    "created_at": "2025-10-15T12:00:00",
    "completed_at": null
  }
}
```

**Possible Status Values:**
- `pending` - Job created, waiting to start
- `processing` - APK is being built
- `completed` - APK ready for download
- `failed` - Build failed

**Error (404 Not Found):**
```json
{
  "success": false,
  "error": "Job not found",
  "message": "Invalid job ID or job may have expired"
}
```

#### Example Request (cURL)

```bash
curl https://your-domain.com/api/v1/status/550e8400-e29b-41d4-a716-446655440000
```

---

### 3. Download APK

**Endpoint:** `GET /api/v1/download/{job_id}`

**Description:** Download APK if ready, or get status if still building.

**Authentication:** Not required

#### Response

**APK Ready (200 OK):**
- Content-Type: `application/vnd.android.package-archive`
- Body: Binary APK file

**Still Building (202 Accepted):**
```json
{
  "success": false,
  "status": "processing",
  "message": "Your APK is being built... Decompiling base APK...",
  "progress": 20,
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "tip": "APK building can take 10-20 minutes on free tier. Please be patient."
}
```

**Build Failed (500 Internal Server Error):**
```json
{
  "success": false,
  "status": "failed",
  "message": "APK build failed",
  "error": "Error details here",
  "job_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Error (404 Not Found):**
```json
{
  "success": false,
  "error": "Job not found",
  "message": "Invalid job ID. Please check your job ID or the job may have expired."
}
```

#### Example Request (cURL)

```bash
# Try to download APK
curl https://your-domain.com/api/v1/download/550e8400-e29b-41d4-a716-446655440000 \
  -o myapp.apk

# If not ready, you'll get JSON status. If ready, APK downloads.
```

---

## 💻 Code Examples

### JavaScript (Node.js) - Complete Workflow

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function buildAndDownloadAPK() {
  const form = new FormData();
  form.append('appName', 'My Awesome App');
  form.append('url', 'https://example.com');
  
  // Optional: Add custom icon
  // form.append('appIcon', fs.createReadStream('./icon.png'));

  try {
    // Step 1: Create build job
    console.log('Creating APK build job...');
    const buildResponse = await axios({
      method: 'post',
      url: 'https://your-domain.com/api/v1/build-apk',
      headers: {
        'X-API-Key': 'apk_your_api_key_here',
        ...form.getHeaders()
      },
      data: form
    });

    const { job_id, download_url, status_url } = buildResponse.data;
    console.log(`Job created: ${job_id}`);
    console.log(`Download URL: ${download_url}`);

    // Step 2: Poll for completion (check every 30 seconds)
    let isComplete = false;
    while (!isComplete) {
      await new Promise(resolve => setTimeout(resolve, 30000)); // Wait 30 seconds
      
      console.log('Checking build status...');
      const statusResponse = await axios.get(status_url);
      const { status, progress, message } = statusResponse.data.job;
      
      console.log(`Status: ${status} (${progress}%) - ${message}`);
      
      if (status === 'completed') {
        isComplete = true;
      } else if (status === 'failed') {
        throw new Error('Build failed: ' + statusResponse.data.job.error);
      }
    }

    // Step 3: Download APK
    console.log('Downloading APK...');
    const downloadResponse = await axios({
      method: 'get',
      url: download_url,
      responseType: 'arraybuffer'
    });

    fs.writeFileSync('myapp.apk', downloadResponse.data);
    console.log('APK downloaded successfully!');
    
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
}

buildAndDownloadAPK();
```

### Python - Complete Workflow

```python
import requests
import time

def build_and_download_apk():
    # Step 1: Create build job
    print("Creating APK build job...")
    build_url = "https://your-domain.com/api/v1/build-apk"
    
    headers = {"X-API-Key": "apk_your_api_key_here"}
    data = {
        "appName": "My Awesome App",
        "url": "https://example.com"
    }
    
    # Optional: Add custom icon
    # files = {"appIcon": open("icon.png", "rb")}
    # response = requests.post(build_url, headers=headers, data=data, files=files)
    
    response = requests.post(build_url, headers=headers, data=data)
    
    if response.status_code != 202:
        print(f"Error creating job: {response.json()}")
        return
    
    job_data = response.json()
    job_id = job_data['job_id']
    download_url = job_data['download_url']
    status_url = job_data['status_url']
    
    print(f"Job created: {job_id}")
    print(f"Download URL: {download_url}")
    
    # Step 2: Poll for completion (check every 30 seconds)
    while True:
        time.sleep(30)  # Wait 30 seconds
        
        print("Checking build status...")
        status_response = requests.get(status_url)
        job_info = status_response.json()['job']
        
        status = job_info['status']
        progress = job_info['progress']
        message = job_info['message']
        
        print(f"Status: {status} ({progress}%) - {message}")
        
        if status == 'completed':
            break
        elif status == 'failed':
            print(f"Build failed: {job_info.get('error')}")
            return
    
    # Step 3: Download APK
    print("Downloading APK...")
    download_response = requests.get(download_url)
    
    if download_response.status_code == 200:
        with open("myapp.apk", "wb") as f:
            f.write(download_response.content)
        print("APK downloaded successfully!")
    else:
        print(f"Download error: {download_response.json()}")

build_and_download_apk()
```

### PHP - Complete Workflow

```php
<?php

function buildAndDownloadAPK() {
    // Step 1: Create build job
    echo "Creating APK build job...\n";
    $buildUrl = "https://your-domain.com/api/v1/build-apk";
    
    $ch = curl_init();
    
    $data = [
        'appName' => 'My Awesome App',
        'url' => 'https://example.com',
        // Optional: Add custom icon
        // 'appIcon' => new CURLFile('/path/to/icon.png')
    ];
    
    curl_setopt($ch, CURLOPT_URL, $buildUrl);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'X-API-Key: apk_your_api_key_here'
    ]);
    
    $response = curl_exec($ch);
    curl_close($ch);
    
    $jobData = json_decode($response, true);
    
    if (!isset($jobData['job_id'])) {
        echo "Error: " . $response . "\n";
        return;
    }
    
    $jobId = $jobData['job_id'];
    $downloadUrl = $jobData['download_url'];
    $statusUrl = $jobData['status_url'];
    
    echo "Job created: {$jobId}\n";
    echo "Download URL: {$downloadUrl}\n";
    
    // Step 2: Poll for completion (check every 30 seconds)
    while (true) {
        sleep(30);
        
        echo "Checking build status...\n";
        $statusResponse = file_get_contents($statusUrl);
        $statusData = json_decode($statusResponse, true);
        $job = $statusData['job'];
        
        echo "Status: {$job['status']} ({$job['progress']}%) - {$job['message']}\n";
        
        if ($job['status'] === 'completed') {
            break;
        }
        
        if ($job['status'] === 'failed') {
            echo "Build failed: {$job['error']}\n";
            return;
        }
    }
    
    // Step 3: Download APK
    echo "Downloading APK...\n";
    $apkData = file_get_contents($downloadUrl);
    
    if ($apkData) {
        file_put_contents('myapp.apk', $apkData);
        echo "APK downloaded successfully!\n";
    } else {
        echo "Download error\n";
    }
}

buildAndDownloadAPK();
?>
```

### Ruby - Complete Workflow

```ruby
require 'httparty'
require 'json'

def build_and_download_apk
  # Step 1: Create build job
  puts "Creating APK build job..."
  build_url = "https://your-domain.com/api/v1/build-apk"
  
  response = HTTParty.post(build_url,
    headers: {
      'X-API-Key' => 'apk_your_api_key_here'
    },
    body: {
      appName: 'My Awesome App',
      url: 'https://example.com'
      # Optional: appIcon: File.new('icon.png')
    }
  )
  
  if response.code != 202
    puts "Error: #{response.body}"
    return
  end
  
  job_data = JSON.parse(response.body)
  job_id = job_data['job_id']
  download_url = job_data['download_url']
  status_url = job_data['status_url']
  
  puts "Job created: #{job_id}"
  puts "Download URL: #{download_url}"
  
  # Step 2: Poll for completion (check every 30 seconds)
  loop do
    sleep(30)
    
    puts "Checking build status..."
    status_response = HTTParty.get(status_url)
    job_info = JSON.parse(status_response.body)['job']
    
    status = job_info['status']
    progress = job_info['progress']
    message = job_info['message']
    
    puts "Status: #{status} (#{progress}%) - #{message}"
    
    break if status == 'completed'
    
    if status == 'failed'
      puts "Build failed: #{job_info['error']}"
      return
    end
  end
  
  # Step 3: Download APK
  puts "Downloading APK..."
  download_response = HTTParty.get(download_url)
  
  if download_response.code == 200
    File.open('myapp.apk', 'wb') { |file| file.write(download_response.body) }
    puts "APK downloaded successfully!"
  else
    puts "Download error: #{download_response.body}"
  end
end

build_and_download_apk
```

### Go - Complete Workflow

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "mime/multipart"
    "net/http"
    "os"
    "time"
)

type JobResponse struct {
    Success     bool   `json:"success"`
    JobID       string `json:"job_id"`
    DownloadURL string `json:"download_url"`
    StatusURL   string `json:"status_url"`
}

type StatusResponse struct {
    Success bool `json:"success"`
    Job     struct {
        Status   string `json:"status"`
        Progress int    `json:"progress"`
        Message  string `json:"message"`
        Error    string `json:"error"`
    } `json:"job"`
}

func buildAndDownloadAPK() error {
    // Step 1: Create build job
    fmt.Println("Creating APK build job...")
    buildURL := "https://your-domain.com/api/v1/build-apk"
    
    var b bytes.Buffer
    w := multipart.NewWriter(&b)
    w.WriteField("appName", "My Awesome App")
    w.WriteField("url", "https://example.com")
    w.Close()
    
    req, _ := http.NewRequest("POST", buildURL, &b)
    req.Header.Set("X-API-Key", "apk_your_api_key_here")
    req.Header.Set("Content-Type", w.FormDataContentType())
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    var jobResp JobResponse
    json.NewDecoder(resp.Body).Decode(&jobResp)
    
    fmt.Printf("Job created: %s\n", jobResp.JobID)
    fmt.Printf("Download URL: %s\n", jobResp.DownloadURL)
    
    // Step 2: Poll for completion
    for {
        time.Sleep(30 * time.Second)
        
        fmt.Println("Checking build status...")
        statusResp, _ := http.Get(jobResp.StatusURL)
        var status StatusResponse
        json.NewDecoder(statusResp.Body).Decode(&status)
        statusResp.Body.Close()
        
        fmt.Printf("Status: %s (%d%%) - %s\n", 
            status.Job.Status, status.Job.Progress, status.Job.Message)
        
        if status.Job.Status == "completed" {
            break
        }
        if status.Job.Status == "failed" {
            return fmt.Errorf("build failed: %s", status.Job.Error)
        }
    }
    
    // Step 3: Download APK
    fmt.Println("Downloading APK...")
    downloadResp, _ := http.Get(jobResp.DownloadURL)
    defer downloadResp.Body.Close()
    
    out, _ := os.Create("myapp.apk")
    defer out.Close()
    io.Copy(out, downloadResp.Body)
    
    fmt.Println("APK downloaded successfully!")
    return nil
}

func main() {
    buildAndDownloadAPK()
}
```

---

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Description | Used By |
|------|-------------|---------|
| 200 | Success - APK file returned | `/api/v1/download/{job_id}` (when ready) |
| 202 | Accepted - Job created successfully | `/api/v1/build-apk` |
| 202 | Accepted - APK still building | `/api/v1/download/{job_id}` (when pending) |
| 400 | Bad Request - Missing or invalid parameters | `/api/v1/build-apk` |
| 401 | Unauthorized - Missing API key | `/api/v1/build-apk` |
| 403 | Forbidden - Invalid or revoked API key | `/api/v1/build-apk` |
| 404 | Not Found - Job ID not found | `/api/v1/status/{job_id}`, `/api/v1/download/{job_id}` |
| 500 | Internal Server Error - Server-side issue | All endpoints |

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

#### Job Not Found (Async Endpoints)
```json
{
  "success": false,
  "error": "Job not found",
  "message": "Invalid job ID or job may have expired"
}
```

#### APK Still Building (Download Endpoint)
```json
{
  "success": false,
  "status": "processing",
  "message": "Your APK is being built... Decompiling base APK...",
  "progress": 20,
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "tip": "APK building can take 10-20 minutes on free tier. Please be patient."
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

### 3. **Async Workflow Best Practices**
- **Poll Responsibly**: Check status every 30-60 seconds (don't spam the API)
- **Set Timeouts**: Implement reasonable timeouts (30 minutes recommended)
- **Store Job IDs**: Save `job_id` and `download_url` for later retrieval
- **Handle All States**: Handle `pending`, `processing`, `completed`, and `failed` states
- **Retry Logic**: Implement exponential backoff for network errors

### 4. **Performance Tips**
- **Expected Build Time**: 
  - Free tier (0.1 CPU): 10-20 minutes
  - Paid tier: 2-5 minutes
- **Concurrent Jobs**: You can create multiple jobs simultaneously
- **Download Links**: Save download URLs - they remain valid until job expires

### 5. **Optimize Icon Files**
- Use square images (1:1 aspect ratio)
- Recommended size: 512x512 pixels
- Supported formats: PNG, JPG
- Keep file size under 2MB

### 6. **URL Format**
- Include protocol (https:// or http://)
- Ensure URL is accessible and valid
- Test URLs before sending to API

### 7. **Rate Limiting**
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
- [ ] Implement async polling logic (30-60 second intervals)
- [ ] Implement error handling for all states
- [ ] Add custom icon support (optional)
- [ ] Deploy to production

---

## 📖 Quick Reference

### Endpoint Summary

| Endpoint | Method | Auth Required | Returns |
|----------|--------|---------------|---------|
| `/api/v1/build-apk` | POST | Yes | Job ID & URLs (202) |
| `/api/v1/status/{job_id}` | GET | No | Job status (200) |
| `/api/v1/download/{job_id}` | GET | No | APK or status (200/202) |

### Job Status Values

| Status | Description |
|--------|-------------|
| `pending` | Job created, waiting to start |
| `processing` | APK is being built |
| `completed` | APK ready for download |
| `failed` | Build failed, check error message |

### Quick cURL Example

```bash
# 1. Create job
curl -X POST https://your-domain.com/api/v1/build-apk \
  -H "X-API-Key: your_key" \
  -F "appName=My App" \
  -F "url=https://example.com"

# 2. Check status (use job_id from step 1)
curl https://your-domain.com/api/v1/status/{job_id}

# 3. Download APK (when ready)
curl https://your-domain.com/api/v1/download/{job_id} -o app.apk
```

---

**Last Updated:** October 2025  
**API Version:** 1.0 (Async)

---

## 🔄 Async Integration Flow

```
1. User enters website URL in your app
       ↓
2. Your backend calls /api/v1/build-apk
       ↓
3. Receive job_id & download_url immediately (202 Accepted)
       ↓
4. Show user "Building..." with progress
       ↓
5. Poll /api/v1/status/{job_id} every 30-60s
       ↓
6. When status = "completed", download from download_url
       ↓
7. Deliver APK to user
```

**Build Time:** 10-20 minutes (free tier) | 2-5 minutes (paid tier)

---

*Built with ❤️ for developers who want to convert websites to Android apps instantly.*
