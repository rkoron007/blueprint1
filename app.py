import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Simple test app is running!',
        'endpoints': {
            '/': 'This page',
            '/health': 'Health check',
            '/db': 'Database connection test'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

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
