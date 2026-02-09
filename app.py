import os
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Disk Mount Path Test App',
        'description': 'Use this app to test and verify disk mount paths on Render',
        'endpoints': {
            '/': 'This page',
            '/health': 'Health check',
            '/db': 'Database connection test',
            '/paths': 'Show current paths and disk information',
            '/write': 'Test writing to a disk (POST with path param)',
            '/read': 'Test reading from a disk (GET with path param)',
            '/test': 'Test endpoint for preview'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/test')
def test():
    """NEW endpoint to demonstrate preview environment"""
    return jsonify({
        'status': 'success',
        'message': 'This is a NEW test endpoint!',
        'note': 'This only exists in the preview environment',
        'data': {
            'feature': 'test-feature',
            'version': '2.0',
            'preview': True
        }
    })

@app.route('/paths')
def show_paths():
    """Show filesystem paths and disk information"""
    current_dir = os.getcwd()
    
    # Common mount paths to check
    paths_to_check = [
        '/opt/render/project/src',
        '/opt/render/project/src/data',
        '/opt/render/project/src/uploads',
        '/var/data',
        current_dir
    ]
    
    path_info = {}
    for path in paths_to_check:
        path_obj = Path(path)
        path_info[path] = {
            'exists': path_obj.exists(),
            'is_directory': path_obj.is_dir() if path_obj.exists() else None,
            'writable': os.access(path, os.W_OK) if path_obj.exists() else None
        }
    
    return jsonify({
        'status': 'success',
        'current_working_directory': current_dir,
        'project_root': os.path.dirname(os.path.abspath(__file__)),
        'paths_checked': path_info,
        'environment': os.environ.get('RENDER', 'local'),
        'tip': 'Run pwd in the Render shell to see your actual project path'
    })

@app.route('/write', methods=['POST'])
def write_test():
    """Test writing to a disk path"""
    mount_path = request.args.get('path', '/opt/render/project/src/data')
    
    try:
        # Create directory if it doesn't exist
        Path(mount_path).mkdir(parents=True, exist_ok=True)
        
        # Write a test file
        test_file = Path(mount_path) / 'test.txt'
        timestamp = datetime.now().isoformat()
        test_file.write_text(f'Test write at {timestamp}\n')
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully wrote to {test_file}',
            'path': str(test_file),
            'content': f'Test write at {timestamp}',
            'disk_exists': Path(mount_path).exists(),
            'absolute_path': str(test_file.absolute())
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'path': mount_path,
            'tip': 'Make sure the disk is mounted at this path in render.yaml'
        }), 500

@app.route('/read', methods=['GET'])
def read_test():
    """Test reading from a disk path"""
    mount_path = request.args.get('path', '/opt/render/project/src/data')
    
    try:
        test_file = Path(mount_path) / 'test.txt'
        
        if not test_file.exists():
            return jsonify({
                'status': 'warning',
                'message': f'File not found at {test_file}',
                'tip': 'Use POST /write?path={mount_path} to create a test file first'
            }), 404
        
        content = test_file.read_text()
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully read from {test_file}',
            'path': str(test_file),
            'content': content,
            'absolute_path': str(test_file.absolute())
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'path': mount_path
        }), 500

@app.route('/db')
def test_db():
    """Test database connection"""
    database_url = os.environ.get('DATABASE_URL')

    if not database_url:
        return jsonify({
            'status': 'error',
            'message': 'DATABASE_URL not configured'
        }), 500

    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            return jsonify({
                'status': 'success',
                'message': 'Database connected!',
                'postgres_version': version
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
