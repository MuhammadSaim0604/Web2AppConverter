"""
Auto-detect base version based on user inputs
"""
import json
import os

class VersionDetector:
    def __init__(self, config_path='apk_builder/config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
    
    def detect_base_version(self, user_inputs):
        """
        Auto-detect which base version to use based on user inputs
        
        Args:
            user_inputs: dict with keys like 'app_name', 'url', 'icon', etc.
        
        Returns:
            str: base version name (e.g., 'base_1', 'base_2')
        """
        # Get list of provided customizations (excluding None/empty values)
        provided_customizations = [
            key for key, value in user_inputs.items() 
            if value is not None and value != ''
        ]
        
        # Find best matching base version
        # Priority: exact match > superset match > first available
        
        base_versions = self.config['base_versions']
        
        # Try exact match first
        for version_name, version_config in base_versions.items():
            version_customizations = set(version_config['customizations'])
            provided_set = set(provided_customizations)
            
            # Check if all required fields are provided
            required_fields = set(version_config.get('required_fields', []))
            if not required_fields.issubset(provided_set):
                continue
            
            # Check if provided customizations match this version
            if provided_set.issubset(version_customizations):
                return version_name
        
        # If no exact match, return base_1 as default
        return 'base_1'
    
    def get_base_config(self, version_name):
        """Get configuration for a specific base version"""
        return self.config['base_versions'].get(version_name)
    
    def get_keystore_config(self):
        """Get keystore configuration"""
        return self.config['keystore']
