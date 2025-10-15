import os
import shutil
import re
import requests
from PIL import Image
from io import BytesIO

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'android_templates')

def generate_android_project(project_dir, url, app_name, package_name, theme_color, 
                            enable_offline, favicon_url, metadata, custom_icon_path=None):
    
    shutil.copytree(TEMPLATE_DIR, project_dir)
    
    package_path = package_name.replace('.', '/')
    
    replacements = {
        '{{PACKAGE_NAME}}': package_name,
        '{{APP_NAME}}': app_name,
        '{{URL}}': url,
        '{{THEME_COLOR}}': theme_color,
        '{{ENABLE_OFFLINE}}': 'true' if enable_offline else 'false',
    }
    
    for root, dirs, files in os.walk(project_dir):
        for filename in files:
            if filename.endswith(('.kt', '.xml', '.gradle', '.kts', '.properties', '.json', '.md')):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for old, new in replacements.items():
                    content = content.replace(old, new)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    old_package_path = os.path.join(project_dir, 'app', 'src', 'main', 'java', 'com', 'web2app', 'template')
    new_package_path = os.path.join(project_dir, 'app', 'src', 'main', 'java', package_path)
    
    if os.path.exists(old_package_path):
        os.makedirs(os.path.dirname(new_package_path), exist_ok=True)
        shutil.move(old_package_path, new_package_path)
        
        parent_dir = os.path.dirname(old_package_path)
        while parent_dir != os.path.join(project_dir, 'app', 'src', 'main', 'java'):
            if not os.listdir(parent_dir):
                os.rmdir(parent_dir)
                parent_dir = os.path.dirname(parent_dir)
            else:
                break
    
    if custom_icon_path:
        try:
            process_custom_icon(custom_icon_path, project_dir)
        except:
            create_default_icon(project_dir, app_name, theme_color)
    elif favicon_url:
        try:
            download_and_convert_favicon(favicon_url, project_dir, app_name)
        except:
            create_default_icon(project_dir, app_name, theme_color)
    else:
        create_default_icon(project_dir, app_name, theme_color)
    
    return project_dir

def process_custom_icon(icon_path, project_dir):
    img = Image.open(icon_path)
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    icon_sizes = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192
    }
    
    for density, size in icon_sizes.items():
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        mipmap_dir = os.path.join(project_dir, 'app', 'src', 'main', 'res', f'mipmap-{density}')
        os.makedirs(mipmap_dir, exist_ok=True)
        
        icon_path_dest = os.path.join(mipmap_dir, 'ic_launcher.png')
        resized_img.save(icon_path_dest, 'PNG')

def download_and_convert_favicon(favicon_url, project_dir, app_name):
    response = requests.get(favicon_url, timeout=10)
    response.raise_for_status()
    
    img = Image.open(BytesIO(response.content))
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    icon_sizes = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192
    }
    
    for density, size in icon_sizes.items():
        resized_img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        mipmap_dir = os.path.join(project_dir, 'app', 'src', 'main', 'res', f'mipmap-{density}')
        os.makedirs(mipmap_dir, exist_ok=True)
        
        icon_path = os.path.join(mipmap_dir, 'ic_launcher.png')
        resized_img.save(icon_path, 'PNG')

def create_default_icon(project_dir, app_name, theme_color):
    icon_sizes = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192
    }
    
    color_rgb = hex_to_rgb(theme_color)
    
    for density, size in icon_sizes.items():
        img = Image.new('RGBA', (size, size), color_rgb)
        
        mipmap_dir = os.path.join(project_dir, 'app', 'src', 'main', 'res', f'mipmap-{density}')
        os.makedirs(mipmap_dir, exist_ok=True)
        
        icon_path = os.path.join(mipmap_dir, 'ic_launcher.png')
        img.save(icon_path, 'PNG')

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
