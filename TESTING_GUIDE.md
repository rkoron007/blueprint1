# Quick Testing Guide for Disk Mount Documentation

## Purpose
Validate that the disk mount path documentation is clear and accurate for users.

## Quick Test Workflow

### 1️⃣ Deploy (No Disk)
```bash
# Deploy the app with disk configuration commented out
# Wait for: ✅ Service is live
```

### 2️⃣ Find Absolute Path
**Via Shell:**
```bash
# In Render Dashboard → Your Service → Shell tab
pwd
# Example output: /opt/render/project/src
```

**Via API:**
```bash
curl https://your-app.onrender.com/paths | jq .current_working_directory
# Example output: "/opt/render/project/src"
```

### 3️⃣ Add Disk Configuration
Update `render.yaml` with the actual path from step 2:

```yaml
disk:
  name: test-disk
  mountPath: /opt/render/project/src/data  # Use path from pwd + /data
  sizeGB: 1
```

Commit and push to trigger redeployment.

### 4️⃣ Verify Disk Works
```bash
# Check disk exists and is writable
curl https://your-app.onrender.com/paths

# Write test file
curl -X POST "https://your-app.onrender.com/write?path=/opt/render/project/src/data"

# Read test file
curl "https://your-app.onrender.com/read?path=/opt/render/project/src/data"
```

## What You're Testing

This validates the documentation instructs users to:

✅ **Deploy first** - Users deploy without a disk initially
✅ **Use `pwd`** - Users find the absolute path via shell command
✅ **Understand absolute paths** - Mount path is filesystem absolute, not project-relative
✅ **Choose mount location** - Users can mount inside or outside project

## Common Path Patterns to Test

| Mount Path | Location | Use Case |
|------------|----------|----------|
| `/opt/render/project/src/data` | Inside project | App uploads, generated files |
| `/opt/render/project/src/uploads` | Inside project | User uploaded content |
| `/var/data` | Outside project | Persistent data, survives builds |
| `/var/lib/app-data` | Outside project | Application state |

## Success Criteria

- [ ] Documentation clearly states mount paths are **absolute**
- [ ] Documentation shows how to use `pwd` to find project path
- [ ] Documentation provides examples of inside vs outside project
- [ ] Users can successfully mount a disk after following the steps
- [ ] Users understand why they need to deploy first

## Edge Cases to Consider

1. **What if user tries relative path?**
   - Mount path `./data` won't work
   - Documentation should clarify "absolute path"

2. **What if user doesn't know project path?**
   - Documentation provides `pwd` solution
   - Documentation mentions typical path: `/opt/render/project/src`

3. **What if user mounts outside project?**
   - App must be configured to use that path
   - Documentation includes this note

## Browser Testing

For non-technical validation, visit these URLs in a browser:

1. `https://your-app.onrender.com/` - Should show welcome page
2. `https://your-app.onrender.com/paths` - Should show current paths (JSON)
3. `https://your-app.onrender.com/write?path=/opt/render/project/src/data` - Should write file
4. `https://your-app.onrender.com/read?path=/opt/render/project/src/data` - Should read file

## Sample Documentation Test Script

```bash
#!/bin/bash
# Test the documentation workflow

APP_URL="https://your-app.onrender.com"

echo "Step 1: Check if app is deployed (no disk yet)..."
curl -s "$APP_URL/health" | jq .

echo "\nStep 2: Find project path..."
PROJECT_PATH=$(curl -s "$APP_URL/paths" | jq -r .current_working_directory)
echo "Project is at: $PROJECT_PATH"

echo "\nStep 3: After adding disk to render.yaml..."
echo "Suggested mount path: $PROJECT_PATH/data"

echo "\nStep 4: Verify disk is mounted..."
curl -s "$APP_URL/paths" | jq '.paths_checked'

echo "\nStep 5: Test write operation..."
curl -s -X POST "$APP_URL/write?path=$PROJECT_PATH/data" | jq .

echo "\nStep 6: Test read operation..."
curl -s "$APP_URL/read?path=$PROJECT_PATH/data" | jq .

echo "\n✅ All tests complete!"
```

## Documentation Feedback to Validate

Original customer feedback:
> "For the future it might be good to add this path clarification to the documentation, now it implies that project root is the starting point and you can't know the absolute path when activating the service the first time."

Does your new documentation address:
- ✅ Clarify absolute vs relative paths?
- ✅ Show how to find the absolute path?
- ✅ Explain you need to deploy first to find the path?
- ✅ Provide examples of paths inside and outside project?

## Next Steps After Testing

1. **If tests pass:** Documentation is clear and accurate ✅
2. **If tests fail:** Note where confusion occurs and update docs
3. **Gather feedback:** Have someone unfamiliar with Render follow the docs
4. **Iterate:** Update based on real user testing

---

**Pro Tip:** The `/paths` endpoint is your best friend for debugging mount issues!
