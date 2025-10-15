let cropper = null;
let croppedBlob = null;

// Ensure modal is hidden on page load
window.addEventListener('DOMContentLoaded', function() {
    const cropModal = document.getElementById('cropModal');
    cropModal.classList.add('hidden');
});

document.getElementById('appIcon').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const cropModal = document.getElementById('cropModal');
            const cropImage = document.getElementById('cropImage');
            
            cropImage.src = event.target.result;
            cropModal.classList.remove('hidden');
            
            if (cropper) {
                cropper.destroy();
            }
            
            cropper = new Cropper(cropImage, {
                aspectRatio: 1,
                viewMode: 1,
                autoCropArea: 1,
                responsive: true,
                background: false,
                guides: true,
                center: true,
                highlight: true,
                cropBoxResizable: true,
                cropBoxMovable: true,
                toggleDragModeOnDblclick: false,
            });
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('cancelCrop').addEventListener('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const cropModal = document.getElementById('cropModal');
    cropModal.classList.add('hidden');
    document.getElementById('appIcon').value = '';
    croppedBlob = null;
    
    if (cropper) {
        cropper.destroy();
        cropper = null;
    }
});

document.getElementById('applyCrop').addEventListener('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    
    if (cropper) {
        cropper.getCroppedCanvas({
            width: 512,
            height: 512,
            imageSmoothingQuality: 'high'
        }).toBlob(function(blob) {
            croppedBlob = blob;
            const cropModal = document.getElementById('cropModal');
            cropModal.classList.add('hidden');
            
            if (cropper) {
                cropper.destroy();
                cropper = null;
            }
        }, 'image/png');
    }
});

document.getElementById('converterForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData();
    
    formData.append('url', document.getElementById('url').value.trim());
    formData.append('appName', document.getElementById('appName').value.trim());
    formData.append('themeColor', document.getElementById('themeColor').value);
    formData.append('enableOffline', document.getElementById('enableOffline').checked);
    
    if (croppedBlob) {
        formData.append('appIcon', croppedBlob, 'app-icon.png');
    }

    const generateBtn = document.getElementById('generateBtn');
    const loadingDiv = document.getElementById('loading');
    const successDiv = document.getElementById('success');
    const errorDiv = document.getElementById('error');

    generateBtn.disabled = true;
    form.style.display = 'none';
    loadingDiv.classList.remove('hidden');
    successDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');

    try {
        const response = await fetch('/api/build-apk', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to build APK');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        
        const contentDisposition = response.headers.get('content-disposition');
        let filename = 'MyApp.apk';
        if (contentDisposition) {
            const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
            if (filenameMatch && filenameMatch[1]) {
                filename = filenameMatch[1].replace(/['"]/g, '');
            }
        }
        
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        loadingDiv.classList.add('hidden');
        successDiv.classList.remove('hidden');

        setTimeout(() => {
            successDiv.classList.add('hidden');
            form.style.display = 'block';
            form.reset();
            document.getElementById('themeColor').value = '#2196F3';
            generateBtn.disabled = false;
        }, 5000);

    } catch (error) {
        loadingDiv.classList.add('hidden');
        errorDiv.classList.remove('hidden');
        document.getElementById('errorMessage').textContent = error.message;

        setTimeout(() => {
            errorDiv.classList.add('hidden');
            form.style.display = 'block';
            generateBtn.disabled = false;
        }, 5000);
    }
});

// API Key Management - Client-side storage
function getStoredApiKeys() {
    const keys = localStorage.getItem('apiKeys');
    return keys ? JSON.parse(keys) : [];
}

function saveApiKey(keyData) {
    const keys = getStoredApiKeys();
    keys.push(keyData);
    localStorage.setItem('apiKeys', JSON.stringify(keys));
}

function removeStoredApiKey(keyToRemove) {
    let keys = getStoredApiKeys();
    keys = keys.filter(k => k.api_key !== keyToRemove);
    localStorage.setItem('apiKeys', JSON.stringify(keys));
}

async function verifyAndDisplayKey(keyData) {
    try {
        const response = await fetch('/api/keys/verify', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ api_key: keyData.api_key })
        });
        
        if (response.ok) {
            const data = await response.json();
            return { ...keyData, ...data.key_info };
        }
        return null;
    } catch (error) {
        return null;
    }
}

async function loadApiKeys() {
    const container = document.getElementById('apiKeysList');
    const storedKeys = getStoredApiKeys();
    
    if (storedKeys.length === 0) {
        container.innerHTML = '<p class="no-keys">No API keys saved. Generate one to get started!</p>';
        return;
    }
    
    // Verify each key and display info
    const keyPromises = storedKeys.map(k => verifyAndDisplayKey(k));
    const verifiedKeys = await Promise.all(keyPromises);
    
    const activeKeys = verifiedKeys.filter(k => k !== null);
    
    if (activeKeys.length > 0) {
        container.innerHTML = activeKeys.map(key => `
            <div class="api-key-item">
                <div class="api-key-info">
                    <strong>${key.name}</strong>
                    <small>Created: ${new Date(key.created_at).toLocaleDateString()}</small>
                    ${key.last_used ? `<small>Last used: ${new Date(key.last_used).toLocaleDateString()}</small>` : '<small>Never used</small>'}
                    <small>Requests: ${key.request_count}</small>
                    <small style="font-family: monospace; font-size: 11px; color: #64748b;">Key: ${key.api_key.substring(0, 20)}...</small>
                </div>
                <div class="api-key-actions">
                    <span class="status ${key.active ? 'active' : 'inactive'}">${key.active ? 'Active' : 'Revoked'}</span>
                    ${key.active ? `<button onclick="revokeApiKey('${key.api_key}')" class="btn-revoke">Revoke</button>` : ''}
                </div>
            </div>
        `).join('');
    } else {
        container.innerHTML = '<p class="no-keys">No active API keys. Generate a new one!</p>';
    }
}

document.getElementById('generateApiBtn').addEventListener('click', async () => {
    const nameInput = document.getElementById('apiKeyName');
    const name = nameInput.value.trim() || 'Unnamed API Key';
    
    try {
        const response = await fetch('/api/generate-key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const displayDiv = document.getElementById('apiKeyDisplay');
            const keyElement = document.getElementById('generatedApiKey');
            
            keyElement.textContent = data.api_key;
            displayDiv.classList.remove('hidden');
            nameInput.value = '';
            
            // Save to localStorage
            saveApiKey({
                api_key: data.api_key,
                name: data.name,
                created_at: data.created_at,
                key_id: data.key_id
            });
            
            loadApiKeys();
        } else {
            alert('Failed to generate API key: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Error generating API key: ' + error.message);
    }
});

document.getElementById('copyApiKey').addEventListener('click', () => {
    const keyElement = document.getElementById('generatedApiKey');
    const key = keyElement.textContent;
    
    navigator.clipboard.writeText(key).then(() => {
        const btn = document.getElementById('copyApiKey');
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(err => {
        alert('Failed to copy: ' + err);
    });
});

async function revokeApiKey(apiKey) {
    if (!confirm('Are you sure you want to revoke this API key? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/keys/revoke', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ api_key: apiKey })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Remove from localStorage
            removeStoredApiKey(apiKey);
            loadApiKeys();
            alert('API key revoked successfully');
        } else {
            alert('Failed to revoke API key: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Error revoking API key: ' + error.message);
    }
}

document.getElementById('viewApiDocs').addEventListener('click', (e) => {
    e.preventDefault();
    window.open('API_DOCUMENTATION.md', '_blank');
});

// Load API keys on page load
window.addEventListener('DOMContentLoaded', () => {
    loadApiKeys();
});
