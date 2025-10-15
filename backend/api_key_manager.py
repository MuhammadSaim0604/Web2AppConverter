"""
API Key Management System
Handles generation, validation, and storage of API keys
"""
import json
import secrets
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

class APIKeyManager:
    def __init__(self, db_path='db/api_keys.json'):
        self.db_path = Path(db_path)
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file exists"""
        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_data({'api_keys': []})
    
    def _load_data(self) -> Dict:
        """Load API keys from file"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {'api_keys': []}
    
    def _save_data(self, data: Dict):
        """Save API keys to file"""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def generate_api_key(self, name: str = "Unnamed API Key") -> Dict:
        """
        Generate a new API key
        
        Args:
            name: Friendly name for the API key
            
        Returns:
            Dict with api_key, key_id, name, and created_at
        """
        # Generate random API key (32 bytes = 64 hex chars)
        api_key = f"apk_{secrets.token_hex(32)}"
        
        # Create key hash for storage (don't store raw key)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Generate unique key ID
        key_id = secrets.token_hex(8)
        
        # Create API key record
        api_key_record = {
            'key_id': key_id,
            'key_hash': key_hash,
            'name': name,
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'request_count': 0,
            'active': True
        }
        
        # Save to database
        data = self._load_data()
        data['api_keys'].append(api_key_record)
        self._save_data(data)
        
        # Return the actual key (only time it's visible!)
        return {
            'api_key': api_key,
            'key_id': key_id,
            'name': name,
            'created_at': api_key_record['created_at']
        }
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """
        Validate an API key
        
        Args:
            api_key: The API key to validate
            
        Returns:
            API key record if valid, None otherwise
        """
        if not api_key or not api_key.startswith('apk_'):
            return None
        
        # Hash the provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Load and search for matching key
        data = self._load_data()
        for key_record in data['api_keys']:
            if key_record['key_hash'] == key_hash and key_record['active']:
                # Update last used time and request count
                key_record['last_used'] = datetime.now().isoformat()
                key_record['request_count'] += 1
                self._save_data(data)
                
                return key_record
        
        return None
    
    def list_api_keys(self) -> List[Dict]:
        """List all API keys (without showing the actual keys)"""
        data = self._load_data()
        return [{
            'key_id': key['key_id'],
            'name': key['name'],
            'created_at': key['created_at'],
            'last_used': key['last_used'],
            'request_count': key['request_count'],
            'active': key['active']
        } for key in data['api_keys']]
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key by key_id"""
        data = self._load_data()
        for key_record in data['api_keys']:
            if key_record['key_id'] == key_id:
                key_record['active'] = False
                self._save_data(data)
                return True
        return False
    
    def delete_api_key(self, key_id: str) -> bool:
        """Permanently delete an API key by key_id"""
        data = self._load_data()
        original_count = len(data['api_keys'])
        data['api_keys'] = [k for k in data['api_keys'] if k['key_id'] != key_id]
        
        if len(data['api_keys']) < original_count:
            self._save_data(data)
            return True
        return False
