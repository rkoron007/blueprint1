# Render Disk Mount Path Test App

A Flask application specifically designed to test and verify **persistent disk mount paths** on Render. Use this to validate the disk mount documentation instructions.

## Purpose

This app helps you test the disk mount path documentation by:
- Showing the actual project directory path
- Testing disk read/write operations
- Verifying absolute vs relative paths
- Demonstrating the `pwd` workflow from the docs

## What's Included

- **Flask web app** with disk testing endpoints
- **PostgreSQL database** connection (optional)
- **Render Blueprint** configuration with disk examples
- **Interactive API** for testing mount paths

## Endpoints

### Core Endpoints
- `GET /` - Welcome page with all available endpoints
- `GET /health` - Health check endpoint
- `GET /paths` - **KEY ENDPOINT** Shows current working directory, project paths, and checks common mount locations
- `POST /write?path=/your/path` - Write a test file to verify disk is writable
- `GET /read?path=/your/path` - Read test file to verify disk is readable
- `GET /db` - Test database connection

## Testing the Documentation Instructions

Follow these steps to test your disk mount documentation:

### Step 1: Deploy Without a Disk

1. Deploy this app to Render using the Blueprint
2. The `render.yaml` has disk configuration commented out initially
3. Wait for deployment to complete

### Step 2: Find Your Project's Absolute Path

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Open your service
3. Click on "Shell" tab to access the shell
4. Run: `pwd`
5. You should see something like: `/opt/render/project/src`

**OR** use the app itself:

1. Visit your deployed app URL
2. Go to `/paths` endpoint
3. Look for `current_working_directory` in the JSON response

### Step 3: Configure Disk with Absolute Path

Edit `render.yaml` and uncomment one of the disk configurations:

**Option A - Inside Project Directory:**
```yaml
disk:
  name: test-disk
  mountPath: /opt/render/project/src/data
  sizeGB: 1
```

**Option B - Outside Project Directory:**
```yaml
disk:
  name: test-disk
  mountPath: /var/data
  sizeGB: 1
```

Push changes to trigger redeployment.

### Step 4: Verify Disk Mount

After redeployment, test the disk:

1. **Check paths:** Visit `/paths` to see if your mount path exists and is writable
2. **Write test:** Visit `/write?path=/opt/render/project/src/data` (or your mount path)
3. **Read test:** Visit `/read?path=/opt/render/project/src/data`

### Expected Results

✅ **Success indicators:**
- `/paths` shows `exists: true` and `writable: true` for your mount path
- `/write` returns success with the absolute path
- `/read` returns the content you wrote
- Data persists across deployments

❌ **Common errors:**
- `exists: false` - Disk not mounted at that path
- `writable: false` - Permission issues
- `FileNotFoundError` - Path doesn't exist, check your `render.yaml`

## Example API Usage

### Check All Paths
```bash
curl https://your-app.onrender.com/paths
```

### Write to Inside-Project Mount
```bash
curl -X POST "https://your-app.onrender.com/write?path=/opt/render/project/src/data"
```

### Write to Outside-Project Mount
```bash
curl -X POST "https://your-app.onrender.com/write?path=/var/data"
```

### Read from Disk
```bash
curl "https://your-app.onrender.com/read?path=/opt/render/project/src/data"
```

## Deploy to Render

### Via Render Dashboard

1. Create a new Blueprint instance
2. Upload the `render.yaml` file (disk configuration commented out initially)
3. Deploy and verify the service starts
4. Follow testing steps above

### Via Git Repository

1. Push these files to a GitHub repository
2. In Render dashboard, create a new Blueprint
3. Connect your repository
4. Render will auto-detect `render.yaml`
5. Follow testing steps above

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://localhost:5000/paths` to see local filesystem info.

**Note:** Local testing won't match Render paths, but you can test the endpoints work.

## Documentation Validation Checklist

Use this checklist to validate the documentation instructions:

- [ ] Deploy service without disk (Step 1)
- [ ] Access shell and run `pwd` command (Step 2)
- [ ] Confirm path is `/opt/render/project/src` or similar (Step 2)
- [ ] Add disk with mount path inside project directory (Step 3)
- [ ] Verify `/paths` shows disk as writable (Step 4)
- [ ] Successfully write to disk (Step 4)
- [ ] Successfully read from disk (Step 4)
- [ ] Try mounting outside project directory at `/var/data` (Optional)
- [ ] Verify data persists after redeployment (Optional)

## Files

- `render.yaml` - Render Blueprint configuration with disk examples
- `app.py` - Flask application with disk testing endpoints
- `requirements.txt` - Python dependencies
- `README.md` - This testing guide

## Troubleshooting

**Problem:** `/paths` shows mount path doesn't exist
- **Solution:** Check your `render.yaml` disk configuration is uncommented and matches the path

**Problem:** Can't write to disk
- **Solution:** Ensure the mount path is absolute and the disk is attached in Render dashboard

**Problem:** `pwd` shows different path than expected
- **Solution:** This is expected! Update your documentation with the actual path from `pwd`

## Notes

- Uses free tier for web service and database
- Minimal disk size (1GB) for testing
- All endpoints return JSON for easy testing
- Mount paths are **absolute filesystem paths**, not relative to project
