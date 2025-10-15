import os
import sys
import uuid
import shutil
from functools import wraps
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from services.url_metadata import fetch_url_metadata
from services.android_generator import generate_android_project
from services.zipper import create_zip
from api_key_manager import APIKeyManager

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from apk_builder.version_detector import VersionDetector

app = Flask(__name__, static_folder='../frontend')
CORS(app)

api_key_manager = APIKeyManager()

GENERATED_DIR = os.path.join(os.path.dirname(__file__), '..', 'generated')
os.makedirs(GENERATED_DIR, exist_ok=True)

def require_api_key(f):
    """
    Decorator to require API key authentication for endpoints
    API key can be provided via:
    - Header: X-API-Key
    - Query parameter: api_key
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from header or query parameter
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')

        if not api_key:
            return jsonify({
                'error': 'API key is required',
                'message': 'Please provide your API key via X-API-Key header or api_key query parameter'
            }), 401

        # Validate API key
        key_record = api_key_manager.validate_api_key(api_key)

        if not key_record:
            return jsonify({
                'error': 'Invalid or inactive API key',
                'message': 'The provided API key is not valid or has been revoked'
            }), 403

        # Add key info to request context for logging
        request.api_key_info = key_record

        return f(*args, **kwargs)

    return decorated_function

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/API_DOCUMENTATION.md')
def serve_api_docs():
    docs_dir = os.path.join(os.path.dirname(__file__), '..')
    return send_from_directory(docs_dir, 'API_DOCUMENTATION.md')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/generate-key', methods=['POST'])
def generate_api_key():
    """Generate a new API key for users"""
    try:
        data = request.get_json() or {}
        name = data.get('name', 'Unnamed API Key')

        # Generate new API key
        result = api_key_manager.generate_api_key(name=name)

        return jsonify({
            'success': True,
            'api_key': result['api_key'],
            'key_id': result['key_id'],
            'name': result['name'],
            'created_at': result['created_at'],
            'message': 'API key generated successfully. Save it securely - you won\'t see it again!'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/keys/verify', methods=['POST'])
def verify_own_key():
    """Verify and get info about your own API key (requires the actual key)"""
    try:
        data = request.get_json() or {}
        api_key = data.get('api_key', '')

        if not api_key:
            return jsonify({'error': 'API key is required'}), 400

        key_record = api_key_manager.validate_api_key(api_key)

        if not key_record:
            return jsonify({
                'success': False,
                'error': 'Invalid or inactive API key'
            }), 403

        return jsonify({
            'success': True,
            'key_info': {
                'key_id': key_record['key_id'],
                'name': key_record['name'],
                'created_at': key_record['created_at'],
                'last_used': key_record['last_used'],
                'request_count': key_record['request_count'],
                'active': key_record['active']
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/keys/revoke', methods=['POST'])
def revoke_own_key():
    """Revoke your own API key (requires the actual key to revoke itself)"""
    try:
        data = request.get_json() or {}
        api_key = data.get('api_key', '')

        if not api_key:
            return jsonify({'error': 'API key is required'}), 400

        # First validate the key
        key_record = api_key_manager.validate_api_key(api_key)

        if not key_record:
            return jsonify({
                'success': False,
                'error': 'Invalid or inactive API key'
            }), 403

        # Revoke the key using its key_id
        success = api_key_manager.revoke_api_key(key_record['key_id'])

        if success:
            return jsonify({
                'success': True,
                'message': 'API key revoked successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to revoke API key'
            }), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Legacy endpoint - kept for backward compatibility
# Use /api/build-apk for direct APK generation
@app.route('/api/generate', methods=['POST'])
def generate_app():
    """
    Legacy: Generates Android Studio project ZIP
    Note: Use /api/build-apk for direct APK download instead
    """
    try:
        url = request.form.get('url', '').strip()

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        app_name = request.form.get('appName', '')
        theme_color = request.form.get('themeColor', '#2196F3')
        enable_offline = request.form.get('enableOffline', 'false').lower() == 'true'

        uploaded_icon = request.files.get('appIcon')

        metadata = fetch_url_metadata(url)

        if not app_name:
            app_name = metadata.get('title', metadata.get('domain', 'MyApp'))

        job_id = str(uuid.uuid4())
        project_dir = os.path.join(GENERATED_DIR, job_id)

        custom_icon_path = None
        if uploaded_icon:
            icon_dir = os.path.join(GENERATED_DIR, 'temp_icons')
            os.makedirs(icon_dir, exist_ok=True)

            safe_filename = secure_filename(uploaded_icon.filename) if uploaded_icon.filename else 'icon.png'
            if not safe_filename or safe_filename == '':
                ext = uploaded_icon.filename.rsplit('.', 1)[1].lower() if uploaded_icon.filename and '.' in uploaded_icon.filename else 'png'
                safe_filename = f'icon.{ext}'

            custom_icon_path = os.path.join(icon_dir, f'{job_id}_{safe_filename}')
            uploaded_icon.save(custom_icon_path)

        generate_android_project(
            project_dir=project_dir,
            url=url,
            app_name=app_name,
            package_name=metadata['package_name'],
            theme_color=theme_color,
            enable_offline=enable_offline,
            favicon_url=metadata.get('favicon_url'),
            metadata=metadata,
            custom_icon_path=custom_icon_path
        )

        zip_path = os.path.join(GENERATED_DIR, f'{job_id}.zip')
        create_zip(project_dir, zip_path)

        shutil.rmtree(project_dir, ignore_errors=True)
        if custom_icon_path and os.path.exists(custom_icon_path):
            os.remove(custom_icon_path)

        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f'{metadata["package_name"]}.zip',
            mimetype='application/zip'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cleanup/<job_id>')
def cleanup(job_id):
    try:
        zip_path = os.path.join(GENERATED_DIR, f'{job_id}.zip')
        if os.path.exists(zip_path):
            os.remove(zip_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/build-apk', methods=['POST'])
@require_api_key
def build_apk_api():
    """
    External API: Build custom APK with auto-detection of base version
    Accepts: app_name, url, optional icon
    Returns: Signed APK file
    Requires: API key via X-API-Key header or api_key parameter
    """
    try:
        # Get form data
        url = request.form.get('url', '').strip()
        app_name = request.form.get('appName', '').strip()
        uploaded_icon = request.files.get('appIcon')

        # Validate required fields
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        if not app_name:
            return jsonify({'error': 'App name is required'}), 400

        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Prepare user inputs for version detection
        user_inputs = {
            'app_name': app_name,
            'url': url,
            'icon': None
        }

        # Save uploaded icon if provided
        icon_path = None
        if uploaded_icon:
            icon_dir = os.path.join(GENERATED_DIR, 'temp_icons')
            os.makedirs(icon_dir, exist_ok=True)

            safe_filename = secure_filename(uploaded_icon.filename) if uploaded_icon.filename else 'icon.png'
            if not safe_filename or safe_filename == '':
                ext = uploaded_icon.filename.rsplit('.', 1)[1].lower() if uploaded_icon.filename and '.' in uploaded_icon.filename else 'png'
                safe_filename = f'icon.{ext}'

            icon_path = os.path.join(icon_dir, f'{uuid.uuid4()}_{safe_filename}')
            uploaded_icon.save(icon_path)
            user_inputs['icon'] = icon_path

        # Auto-detect base version
        detector = VersionDetector()
        base_version = detector.detect_base_version(user_inputs)

        # Build APK (builder uses unique temp directory)
        from apk_builder.builder import APKBuilder
        builder = APKBuilder(base_version=base_version)

        try:
            apk_path = builder.build(
                app_name=app_name,
                url=url,
                icon_path=icon_path
            )

            # Copy APK to a temporary location before cleanup
            final_apk_path = os.path.join(GENERATED_DIR, f'{uuid.uuid4()}.apk')
            shutil.copy(apk_path, final_apk_path)

            # Generate download filename
            safe_app_name = "".join(c for c in app_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_app_name = safe_app_name.replace(' ', '_')
            download_name = f"{safe_app_name}.apk"

            # Send APK file
            response = send_file(
                final_apk_path,
                as_attachment=True,
                download_name=download_name,
                mimetype='application/vnd.android.package-archive'
            )

            # Schedule cleanup after sending
            @response.call_on_close
            def cleanup_files():
                builder.cleanup()
                if icon_path and os.path.exists(icon_path):
                    try:
                        os.remove(icon_path)
                    except:
                        pass
                if os.path.exists(final_apk_path):
                    try:
                        os.remove(final_apk_path)
                    except:
                        pass

            return response

        except Exception as e:
            builder.cleanup()
            if icon_path and os.path.exists(icon_path):
                try:
                    os.remove(icon_path)
                except:
                    pass
            raise

    except Exception as e:
        print(f"API APK Build Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/build-apk', methods=['POST'])
def build_custom_apk():
    """
    Build custom APK with auto-detection of base version
    Accepts: app_name, url, optional icon
    Returns: Signed APK file
    For frontend use (no API key required)
    """
    try:
        # Get form data
        url = request.form.get('url', '').strip()
        app_name = request.form.get('appName', '').strip()
        uploaded_icon = request.files.get('appIcon')

        # Validate required fields
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        if not app_name:
            return jsonify({'error': 'App name is required'}), 400

        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Prepare user inputs for version detection
        user_inputs = {
            'app_name': app_name,
            'url': url,
            'icon': None
        }

        # Save uploaded icon if provided
        icon_path = None
        if uploaded_icon:
            icon_dir = os.path.join(GENERATED_DIR, 'temp_icons')
            os.makedirs(icon_dir, exist_ok=True)

            safe_filename = secure_filename(uploaded_icon.filename) if uploaded_icon.filename else 'icon.png'
            if not safe_filename or safe_filename == '':
                ext = uploaded_icon.filename.rsplit('.', 1)[1].lower() if uploaded_icon.filename and '.' in uploaded_icon.filename else 'png'
                safe_filename = f'icon.{ext}'

            icon_path = os.path.join(icon_dir, f'{uuid.uuid4()}_{safe_filename}')
            uploaded_icon.save(icon_path)
            user_inputs['icon'] = icon_path

        # Auto-detect base version
        detector = VersionDetector()
        base_version = detector.detect_base_version(user_inputs)

        print(f"Building APK with base version: {base_version}")
        print(f"App Name: {app_name}")
        print(f"URL: {url}")
        print(f"Icon: {'Yes' if icon_path else 'No'}")

        # Build APK (builder uses unique temp directory)
        from apk_builder.builder import APKBuilder
        builder = APKBuilder(base_version=base_version)

        try:
            apk_path = builder.build(
                app_name=app_name,
                url=url,
                icon_path=icon_path
            )

            # Copy APK to a temporary location before cleanup
            final_apk_path = os.path.join(GENERATED_DIR, f'{uuid.uuid4()}.apk')
            shutil.copy(apk_path, final_apk_path)

            # Generate download filename
            safe_app_name = "".join(c for c in app_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_app_name = safe_app_name.replace(' ', '_')
            download_name = f"{safe_app_name}.apk"

            # Send APK file
            response = send_file(
                final_apk_path,
                as_attachment=True,
                download_name=download_name,
                mimetype='application/vnd.android.package-archive'
            )

            # Schedule cleanup after sending
            @response.call_on_close
            def cleanup_files():
                # Cleanup builder's temp directory
                builder.cleanup()
                # Cleanup icon
                if icon_path and os.path.exists(icon_path):
                    try:
                        os.remove(icon_path)
                    except:
                        pass
                # Cleanup final APK
                if os.path.exists(final_apk_path):
                    try:
                        os.remove(final_apk_path)
                    except:
                        pass

            return response

        except Exception as e:
            # Cleanup on error
            builder.cleanup()
            if icon_path and os.path.exists(icon_path):
                try:
                    os.remove(icon_path)
                except:
                    pass
            raise

    except Exception as e:
        print(f"APK Build Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable (Render provides $PORT)
    port = int(os.environ.get('PORT', 5000))
    # Disable debug in production
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)