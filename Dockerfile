FROM python:3.11-slim

# Install system dependencies including ncurses for tput
RUN apt-get update && apt-get install -y \
    ncurses-bin \
    default-jdk \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install apktool
RUN mkdir -p /opt/apktool && \
    cd /opt/apktool && \
    wget -q https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool && \
    wget -q https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar -O apktool.jar && \
    chmod +x apktool && \
    chmod +x apktool.jar

# Add apktool to PATH
ENV PATH="/opt/apktool:${PATH}"

# Set Python path to include app directory
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create required directories
RUN mkdir -p db generated android_templates_apks

# Expose port
EXPOSE 5000

# Start command with increased timeout for APK building on slow CPU (30 minutes)
# Using threads to support async job processing in background
CMD gunicorn backend.app:app --bind 0.0.0.0:$PORT --timeout 1800 --workers 1 --threads 2 --worker-class gthread
