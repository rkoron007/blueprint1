import os
from flask import Flask, jsonify, request, render_template_string
from sqlalchemy import create_engine, text
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# HTML template for the UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Render Disk Mount Path Tester</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .path-info {
            background: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #667eea;
            margin: 10px 0;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 14px;
        }
        .button {
            background: #667eea;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        .button:hover {
            background: #5568d3;
        }
        .input {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: 400px;
            font-size: 14px;
            font-family: 'Monaco', 'Courier New', monospace;
        }
        .result {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 15px;
            margin: 10px 0;
            white-space: pre-wrap;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
        }
        .error {
            background: #ffebee;
            border-left: 4px solid #f44336;
        }
        .step {
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 15px;
            margin: 15px 0;
        }
        .step-number {
            display: inline-block;
            background: #ff9800;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            margin-right: 10px;
        }
        h2 { color: #333; margin-top: 0; }
        code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }
        .tip { color: #666; font-style: italic; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔧 Render Disk Mount Path Tester</h1>
        <p>Interactive tool to test and validate disk mount path documentation</p>
    </div>

    <div class="card">
        <h2>📍 Current Path Information</h2>
        <button class="button" onclick="checkPaths()">Check All Paths</button>
        <div id="pathResult"></div>
    </div>

    <div class="card">
        <h2>📝 Documentation Testing Workflow</h2>

        <div class="step">
            <span class="step-number">1</span>
            <strong>Find Your Project Path</strong>
            <p>First, discover where your project is located. This is the <code>pwd</code> value.</p>
            <button class="button" onclick="checkPaths()">Find My Path</button>
        </div>

        <div class="step">
            <span class="step-number">2</span>
            <strong>Configure Your Disk</strong>
            <p>Add a disk to your <code>render.yaml</code> using an absolute path.<br>
            Example: <code>/opt/render/project/src/data</code></p>
        </div>

        <div class="step">
            <span class="step-number">3</span>
            <strong>Test Write Operation</strong>
            <p>Verify you can write to your mounted disk:</p>
            <input type="text" id="writePath" class="input" placeholder="/opt/render/project/src/data" value="/opt/render/project/src/data">
            <button class="button" onclick="testWrite()">Test Write</button>
            <div id="writeResult"></div>
        </div>

        <div class="step">
            <span class="step-number">4</span>
            <strong>Test Read Operation</strong>
            <p>Verify you can read from your mounted disk:</p>
            <input type="text" id="readPath" class="input" placeholder="/opt/render/project/src/data" value="/opt/render/project/src/data">
            <button class="button" onclick="testRead()">Test Read</button>
            <div id="readResult"></div>
        </div>
    </div>

    <div class="card">
        <h2>📚 Common Mount Path Examples</h2>
        <div class="path-info">
            <strong>Inside Project (recommended for app data):</strong><br>
            • /opt/render/project/src/data<br>
            • /opt/render/project/src/uploads<br>
            • /opt/render/project/src/storage
        </div>
        <div class="path-info">
            <strong>Outside Project (survives across builds):</strong><br>
            • /var/data<br>
            • /var/lib/app-data<br>
            • /mnt/disk
        </div>
    </div>

    <script>
        async function checkPaths() {
            const resultDiv = document.getElementById('pathResult');
            resultDiv.innerHTML = '<p>Loading...</p>';

            try {
                const response = await fetch('/paths');
                const data = await response.json();

                let html = '<div class="result">';
                html += '<strong>Current Working Directory:</strong>\\n';
                html += data.current_working_directory + '\\n\\n';
                html += '<strong>Paths Checked:</strong>\\n';

                for (const [path, info] of Object.entries(data.paths_checked)) {
                    const status = info.exists ? (info.writable ? '✅ Writable' : '⚠️  Read-only') : '❌ Not found';
                    html += `${status} ${path}\\n`;
                }

                html += '\\n💡 Tip: ' + data.tip;
                html += '</div>';

                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = `<div class="result error">Error: ${error.message}</div>`;
            }
        }

        async function testWrite() {
            const path = document.getElementById('writePath').value;
            const resultDiv = document.getElementById('writeResult');
            resultDiv.innerHTML = '<p>Writing...</p>';

            try {
                const response = await fetch(`/write?path=${encodeURIComponent(path)}`, {
                    method: 'POST'
                });
                const data = await response.json();

                let html = '<div class="result';
                if (data.status === 'error') html += ' error';
                html += '">';
                html += JSON.stringify(data, null, 2);
                html += '</div>';

                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = `<div class="result error">Error: ${error.message}</div>`;
            }
        }

        async function testRead() {
            const path = document.getElementById('readPath').value;
            const resultDiv = document.getElementById('readResult');
            resultDiv.innerHTML = '<p>Reading...</p>';

            try {
                const response = await fetch(`/read?path=${encodeURIComponent(path)}`);
                const data = await response.json();

                let html = '<div class="result';
                if (data.status === 'error' || data.status === 'warning') html += ' error';
                html += '">';
                html += JSON.stringify(data, null, 2);
                html += '</div>';

                resultDiv.innerHTML = html;
            } catch (error) {
                resultDiv.innerHTML = `<div class="result error">Error: ${error.message}</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api')
def api_home():
    return jsonify({
        'status': 'success',
        'message': 'Disk Mount Path Test App',
        'description': 'Use this app to test and verify disk mount paths on Render',
        'endpoints': {
            '/': 'Interactive web UI',
            '/api': 'This page - API documentation',
            '/health': 'Health check',
            '/db': 'Database connection test',
            '/paths': 'Show current paths and disk information',
            '/write': 'Test writing to a disk (POST with path param)',
            '/read': 'Test reading from a disk (GET with path param)',
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
