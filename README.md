# Simple Render Test Blueprint

A minimal Flask app with PostgreSQL for testing Render deployments.

## What's Included

- **Flask web app** with 3 endpoints
- **PostgreSQL database** connection
- **Render Blueprint** configuration

## Endpoints

- `GET /` - Welcome page with endpoint list
- `GET /health` - Health check endpoint
- `GET /db` - Test database connection

## Deploy to Render

### Option 1: Via Render Dashboard

1. Create a new Blueprint instance
2. Upload the `render.yaml` file
3. Render will create both the web service and database

### Option 2: Via Render CLI

```bash
render blueprint launch
```

### Option 3: From Git Repository

1. Push these files to a GitHub repository
2. In Render dashboard, create a new Blueprint
3. Connect your repository
4. Render will auto-detect `render.yaml`

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set database URL (optional for local testing)
export DATABASE_URL="postgresql://user:pass@localhost/dbname"

# Run the app
python app.py
```

Visit `http://localhost:5000` to test locally.

## Files

- `render.yaml` - Render Blueprint configuration
- `app.py` - Simple Flask application
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Notes

- Uses free tier for both web service and database
- Python 3.11
- Minimal dependencies for fast builds
- All endpoints return JSON
