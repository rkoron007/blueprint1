# Visual Workflow Diagram

## Testing Your Disk Mount Documentation with This App

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOCUMENTATION WORKFLOW                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Deploy Without Disk                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  render.yaml (disk section commented out)                       │
│  ↓                                                               │
│  Deploy to Render                                               │
│  ↓                                                               │
│  ✅ Service is live!                                             │
│                                                                  │
│  TEST: Visit https://your-app.onrender.com/health               │
│  RESULT: {"status": "healthy"}                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Find Your Project's Absolute Path                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  METHOD A: Shell (as documented)                                │
│  ┌────────────────────────────────────┐                         │
│  │ Render Dashboard → Shell Tab       │                         │
│  │ $ pwd                              │                         │
│  │ /opt/render/project/src            │  ← This is the path!   │
│  └────────────────────────────────────┘                         │
│                                                                  │
│  METHOD B: Web UI (easier!)                                     │
│  ┌────────────────────────────────────┐                         │
│  │ Visit: https://your-app/           │                         │
│  │ Click: "Find My Path" button       │                         │
│  │ Shows: /opt/render/project/src     │  ← Same result!        │
│  └────────────────────────────────────┘                         │
│                                                                  │
│  METHOD C: API                                                  │
│  ┌────────────────────────────────────┐                         │
│  │ $ curl https://your-app/paths      │                         │
│  │ {"current_working_directory":      │                         │
│  │  "/opt/render/project/src"}        │  ← Programmatic!       │
│  └────────────────────────────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Configure Disk with Absolute Path                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Update render.yaml:                                            │
│  ┌────────────────────────────────────────────────┐             │
│  │ services:                                      │             │
│  │   - type: web                                  │             │
│  │     name: disk-mount-test-app                  │             │
│  │     # ... other config ...                     │             │
│  │     disk:                                      │             │
│  │       name: test-disk                          │             │
│  │       mountPath: /opt/render/project/src/data  │ ← Absolute! │
│  │       sizeGB: 1                                │             │
│  └────────────────────────────────────────────────┘             │
│                                                                  │
│  Key Points (from your documentation):                          │
│  • Path is ABSOLUTE, not relative                               │
│  • Path is under the project directory you found                │
│  • Format: {project_path}/data (or /uploads, /storage, etc.)   │
│                                                                  │
│  Commit and push → Triggers redeploy                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Verify Disk Works                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TEST A: Check disk exists                                      │
│  ┌────────────────────────────────────────────────┐             │
│  │ Visit: https://your-app/paths                  │             │
│  │                                                │             │
│  │ Result:                                        │             │
│  │ {                                              │             │
│  │   "paths_checked": {                           │             │
│  │     "/opt/render/project/src/data": {          │             │
│  │       "exists": true,          ✅              │             │
│  │       "is_directory": true,    ✅              │             │
│  │       "writable": true         ✅              │             │
│  │     }                                          │             │
│  │   }                                            │             │
│  │ }                                              │             │
│  └────────────────────────────────────────────────┘             │
│                                                                  │
│  TEST B: Write to disk                                          │
│  ┌────────────────────────────────────────────────┐             │
│  │ Method: POST /write?path=/opt/render/.../data  │             │
│  │ Result: {"status": "success", ...}   ✅        │             │
│  └────────────────────────────────────────────────┘             │
│                                                                  │
│  TEST C: Read from disk                                         │
│  ┌────────────────────────────────────────────────┐             │
│  │ Method: GET /read?path=/opt/render/.../data    │             │
│  │ Result: {"status": "success", ...}   ✅        │             │
│  └────────────────────────────────────────────────┘             │
│                                                                  │
│  ✅ ALL TESTS PASSED!                                            │
│  Your documentation workflow is validated!                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    PATH PATTERNS EXPLAINED                       │
└─────────────────────────────────────────────────────────────────┘

INSIDE PROJECT (what you'd typically recommend):
┌──────────────────────────────────────────────────────────────┐
│                                                               │
│  /opt/render/project/src/  ← Your project root (from pwd)   │
│           │                                                   │
│           ├── app.py                                         │
│           ├── requirements.txt                               │
│           ├── render.yaml                                    │
│           │                                                   │
│           └── data/  ← DISK MOUNTED HERE                     │
│               └── test.txt  (your persistent files)          │
│                                                               │
│  Benefits:                                                   │
│  • Easy to access from your app code                         │
│  • Can use relative paths in code                            │
│  • Intuitive for developers                                  │
│                                                               │
└──────────────────────────────────────────────────────────────┘

OUTSIDE PROJECT (alternative pattern):
┌──────────────────────────────────────────────────────────────┐
│                                                               │
│  /var/data/  ← DISK MOUNTED HERE (outside project)          │
│       └── test.txt                                           │
│                                                               │
│  /opt/render/project/src/  ← Your project                   │
│       ├── app.py (must reference /var/data explicitly)       │
│       └── ...                                                 │
│                                                               │
│  Benefits:                                                   │
│  • Survives across builds/deploys                            │
│  • Cleaner separation of code vs data                        │
│  • Common for database files                                 │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   WHAT THE APP DOES FOR YOU                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────┐      ┌─────────────────────┐
│   Beautiful Web UI  │      │    API Endpoints    │
├─────────────────────┤      ├─────────────────────┤
│                     │      │                     │
│ • Click buttons     │      │ • GET /paths        │
│ • See results       │      │ • POST /write       │
│ • Visual feedback   │      │ • GET /read         │
│ • Step-by-step      │      │ • Scriptable        │
│                     │      │                     │
└─────────────────────┘      └─────────────────────┘
         │                            │
         └────────────────┬───────────┘
                          │
                          ↓
              ┌───────────────────────┐
              │   Validates Your      │
              │   Documentation!      │
              └───────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              QUICK TEST COMMANDS                                 │
└─────────────────────────────────────────────────────────────────┘

# Using the shell script (easiest!)
./test_disk.sh https://your-app.onrender.com

# Using curl (manual testing)
curl https://your-app.onrender.com/paths
curl -X POST "https://your-app.onrender.com/write?path=/opt/render/project/src/data"
curl "https://your-app.onrender.com/read?path=/opt/render/project/src/data"

# Using browser (most visual)
Open: https://your-app.onrender.com
Click through the steps!

┌─────────────────────────────────────────────────────────────────┐
│              SUCCESS INDICATORS                                  │
└─────────────────────────────────────────────────────────────────┘

Before disk mount:
❌ /opt/render/project/src/data → exists: false

After disk mount:
✅ /opt/render/project/src/data → exists: true
✅ /opt/render/project/src/data → writable: true
✅ Write operation → success
✅ Read operation → success
✅ Data persists across deploys

🎉 Documentation is correct and working!
