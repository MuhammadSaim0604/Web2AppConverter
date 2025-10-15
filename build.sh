
#!/bin/bash

echo "=========================================="
echo "Render Build Script - Installing Dependencies"
echo "=========================================="

# Step 1: Install Java JDK
echo "[1/3] Installing Java JDK..."
apt-get update -qq
apt-get install -y openjdk-17-jdk wget unzip

# Verify Java installation
java -version

# Step 2: Install apktool
echo "[2/3] Installing apktool..."
mkdir -p /opt/apktool
cd /opt/apktool

# Download apktool wrapper and JAR
wget -q https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
wget -q https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar -O apktool.jar

# Make executable
chmod +x apktool
chmod +x apktool.jar

# Add to PATH
export PATH="/opt/apktool:$PATH"

# Verify apktool
/opt/apktool/apktool --version

# Step 3: Install Python dependencies
echo "[3/3] Installing Python dependencies..."
pip install -r requirements.txt

# Create required directories
mkdir -p db generated android_templates_apks

echo "=========================================="
echo "✓ Build Complete!"
echo "=========================================="
