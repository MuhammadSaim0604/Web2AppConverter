import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def fetch_url_metadata(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = None
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        
        og_title = soup.find('meta', property='og:title')
        if og_title:
            content = og_title.get('content')
            if content and isinstance(content, str):
                title = content.strip()
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('www.', '')
        
        if not title:
            title = domain.split('.')[0].capitalize()
        
        site_name = re.sub(r'[^a-zA-Z0-9]', '', domain.split('.')[0]).lower()
        package_name = f'com.web2app.{site_name}'
        
        favicon_url = None
        icon_link = soup.find('link', rel=lambda x: x and isinstance(x, str) and 'icon' in x.lower())
        if icon_link:
            href = icon_link.get('href')
            if href and isinstance(href, str):
                favicon_url = urljoin(url, href)
        else:
            favicon_url = urljoin(url, '/favicon.ico')
        
        return {
            'title': title,
            'domain': domain,
            'package_name': package_name,
            'favicon_url': favicon_url,
            'url': url
        }
    
    except Exception as e:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace('www.', '')
        site_name = re.sub(r'[^a-zA-Z0-9]', '', domain.split('.')[0]).lower()
        
        return {
            'title': domain.split('.')[0].capitalize(),
            'domain': domain,
            'package_name': f'com.web2app.{site_name}',
            'favicon_url': None,
            'url': url
        }
