"""
APK Builder - Modify and rebuild Android APKs
"""
import os
import shutil
import subprocess
import json
import re
from pathlib import Path
from PIL import Image
import tempfile


class APKBuilder:

  def __init__(self, base_version='base_1'):
    self.base_version = base_version
    # Create unique temp directory for this build to avoid concurrency issues
    self.work_dir = Path(tempfile.mkdtemp(prefix='apk_build_'))
    self.decompiled_dir = None
    self.output_apk = None

    # Load config
    with open('apk_builder/config.json', 'r') as f:
      self.config = json.load(f)

    self.base_config = self.config['base_versions'][base_version]
    self.keystore_config = self.config['keystore']

    # Get keystore credentials from environment or config
    self.keystore_path = os.getenv('KEYSTORE_PATH',
                                   self.keystore_config['path'])
    self.keystore_alias = os.getenv('KEYSTORE_ALIAS',
                                    self.keystore_config['alias'])
    self.keystore_pass = os.getenv('KEYSTORE_PASS',
                                   self.keystore_config['store_pass'])
    self.key_pass = os.getenv('KEY_PASS', self.keystore_config['key_pass'])

  def cleanup(self):
    """Clean up temporary files - removes entire unique work directory"""
    if self.work_dir and self.work_dir.exists():
      shutil.rmtree(self.work_dir, ignore_errors=True)

  def decompile(self):
    """Decompile base APK using apktool"""
    base_apk = self.base_config['apk_path']
    self.decompiled_dir = self.work_dir / 'decompiled'

    # Decompile APK (cross-platform)
    cmd = ['apktool', 'd', str(base_apk), '-o', str(self.decompiled_dir), '-f']

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
      raise Exception(f"Decompile failed: {result.stderr}")

    return True

  def modify_app_name(self, new_name):
    """Modify app name in strings.xml"""
    if not self.decompiled_dir:
      raise Exception("APK not decompiled yet")

    strings_path = self.decompiled_dir / 'res' / 'values' / 'strings.xml'

    if not strings_path.exists():
      raise Exception(f"strings.xml not found at {strings_path}")

    with open(strings_path, 'r', encoding='utf-8') as f:
      content = f.read()

    # Replace app_name value
    content = re.sub(r'(<string name="app_name">).*?(</string>)',
                     rf'\1{new_name}\2', content)

    with open(strings_path, 'w', encoding='utf-8') as f:
      f.write(content)

    return True

  def modify_url(self, new_url):
    """Modify website URL in MainActivity"""
    if not self.decompiled_dir:
      raise Exception("APK not decompiled yet")

    # Find MainActivity file
    main_activity_paths = list(self.decompiled_dir.rglob('MainActivity.smali'))

    if not main_activity_paths:
      raise Exception("MainActivity.smali not found")

    main_activity_path = main_activity_paths[0]

    with open(main_activity_path, 'r', encoding='utf-8') as f:
      content = f.read()

    # Find and replace URL in smali code
    # Look for const-string patterns with URLs
    url_pattern = r'const-string[^,]+,\s*"https?://[^"]*"'

    def replace_url(match):
      return match.group(0).rsplit('"', 2)[0] + f'"{new_url}"'

    content = re.sub(url_pattern, replace_url, content)

    with open(main_activity_path, 'w', encoding='utf-8') as f:
      f.write(content)

    return True

  def modify_icon(self, icon_path):
    """Replace app icon with custom icon"""
    if not icon_path or not os.path.exists(icon_path):
      return False

    if not self.decompiled_dir:
      raise Exception("APK not decompiled yet")

    # Icon sizes for different densities
    icon_sizes = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192
    }

    # Open source icon
    try:
      source_icon = Image.open(icon_path)
      source_icon = source_icon.convert('RGBA')
    except Exception as e:
      raise Exception(f"Failed to open icon: {e}")

    # Generate icons for each density
    for density, size in icon_sizes.items():
      mipmap_dir = self.decompiled_dir / 'res' / f'mipmap-{density}'
      mipmap_dir.mkdir(parents=True, exist_ok=True)

      # Resize icon
      resized_icon = source_icon.resize((size, size), Image.Resampling.LANCZOS)

      # Save as ic_launcher.png
      icon_output = mipmap_dir / 'ic_launcher.png'
      resized_icon.save(icon_output, 'PNG')

    return True

  def recompile(self, output_name='modified.apk'):
    """Recompile APK using apktool"""
    self.output_apk = self.work_dir / output_name

    # Build APK
    cmd = ['apktool', 'b', str(self.decompiled_dir), '-o', str(self.output_apk)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
      raise Exception(f"Recompile failed: {result.stderr}")

    return True

  def sign(self, output_name='signed.apk'):
    """Sign APK using jarsigner (compatible with all Java versions)"""
    if not self.output_apk:
      raise Exception("No APK to sign")

    signed_apk = self.work_dir / output_name

    # First, create a copy for signing
    shutil.copy(str(self.output_apk), str(signed_apk))

    # Use jarsigner (comes with Java, always available)
    cmd = (f'jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 '
           f'-keystore "{self.keystore_path}" '
           f'-storepass {self.keystore_pass} '
           f'-keypass {self.key_pass} '
           f'"{signed_apk}" {self.keystore_alias}')

    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
      raise Exception(f"Signing failed: {result.stderr}")

    self.output_apk = signed_apk
    return True

  def build(self, app_name, url, icon_path=None):
    """
        Complete build process
        
        Args:
            app_name: New app name
            url: Website URL
            icon_path: Path to custom icon (optional)
        
        Returns:
            Path to signed APK
        """
    try:
      print("Starting APK build process...")

      # 1. Cleanup
      print("1. Cleaning up workspace...")
      self.cleanup()

      # 2. Decompile
      print("2. Decompiling base APK...")
      self.decompile()

      # 3. Modify app name
      print(f"3. Setting app name to: {app_name}")
      self.modify_app_name(app_name)

      # 4. Modify URL
      print(f"4. Setting URL to: {url}")
      self.modify_url(url)

      # 5. Modify icon (if provided)
      if icon_path:
        print("5. Replacing app icon...")
        self.modify_icon(icon_path)
      else:
        print("5. Skipping icon replacement (not provided)")

      # 6. Recompile
      print("6. Recompiling APK...")
      self.recompile()

      # 7. Sign
      print("7. Signing APK with jarsigner...")
      self.sign()

      print(f"✓ APK build complete: {self.output_apk}")
      return str(self.output_apk)

    except Exception as e:
      print(f"✗ Build failed: {e}")
      raise


# Convenience function
def build_apk(app_name, url, icon_path=None, base_version='base_1'):
  """Build custom APK with given parameters"""
  builder = APKBuilder(base_version=base_version)
  return builder.build(app_name, url, icon_path)
