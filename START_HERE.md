# 🚀 Quick Start - Testing Disk Mount Documentation

## What Is This?

A complete Flask test application to validate your Render disk mount path documentation. Deploy it, follow the steps, and confirm your docs work perfectly!

## ⚡ Super Quick Start (2 minutes)

1. **Deploy this folder as a Render Blueprint**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - New → Blueprint
   - Connect this repository or upload `render.yaml`

2. **Visit your deployed app URL**
   - You'll see a beautiful UI
   - Click "Find My Path"
   - Note the path shown (e.g., `/opt/render/project/src`)

3. **Uncomment disk config in `render.yaml`**
   ```yaml
   disk:
     name: test-disk
     mountPath: /opt/render/project/src/data  # Use your path from step 2
     sizeGB: 1
   ```

4. **Redeploy and test**
   - Click "Test Write" then "Test Read"
   - Both should succeed! ✅

## 📚 Documentation Files

Pick your learning style:

| File | Best For | Time |
|------|----------|------|
| **START_HERE.md** | You are here! | 2 min |
| **README.md** | Complete guide with all details | 10 min |
| **VISUAL_GUIDE.md** | Visual learners, diagrams | 5 min |
| **TESTING_GUIDE.md** | QA testers, checklists | 5 min |
| **TEST_APP_SUMMARY.md** | Technical overview | 3 min |

## 🎯 What You're Testing

Your new documentation says:

> **The mount path you specify is an absolute filesystem path**, not relative to your project directory.
>
> **To mount a disk within your project:**
> 1. First deploy your service without a disk attached
> 2. Access your service's shell and run `pwd`
> 3. Add a disk with mount path under your project directory

This app lets you verify:
- ✅ Can users find their absolute path easily?
- ✅ Does the `pwd` workflow make sense?
- ✅ Can users successfully mount and use a disk?
- ✅ Is the distinction between absolute/relative clear?

## 🧪 Three Ways to Test

### Option 1: Web UI (Easiest!)
```bash
# After deploying
open https://your-app.onrender.com
# Click through the visual interface
```

### Option 2: Shell Script (Automated!)
```bash
./test_disk.sh https://your-app.onrender.com
# Runs all tests automatically
```

### Option 3: Manual API (Most Control!)
```bash
curl https://your-app.onrender.com/paths
curl -X POST "https://your-app.onrender.com/write?path=/opt/render/project/src/data"
curl "https://your-app.onrender.com/read?path=/opt/render/project/src/data"
```

## 🎨 The Web UI

Visit your deployed app to see:

```
┌─────────────────────────────────────────┐
│  🔧 Render Disk Mount Path Tester       │
│                                          │
│  [Check All Paths] ← Click to find pwd  │
│                                          │
│  Step 1: Find Your Project Path         │
│  Step 2: Configure Your Disk            │
│  Step 3: Test Write Operation           │
│  Step 4: Test Read Operation            │
│                                          │
│  Visual, color-coded results!           │
└─────────────────────────────────────────┘
```

## 📝 File Reference

**Core Files:**
- `app.py` - Flask app with testing endpoints + UI
- `render.yaml` - Blueprint config (edit this to add disk)
- `requirements.txt` - Dependencies (already configured)

**Documentation:**
- `START_HERE.md` - This quick start (you are here!)
- `README.md` - Complete testing guide
- `VISUAL_GUIDE.md` - Workflow diagrams
- `TESTING_GUIDE.md` - QA checklist and scripts
- `TEST_APP_SUMMARY.md` - Technical overview

**Tools:**
- `test_disk.sh` - Automated test script

## ✅ Success Looks Like

When you visit `/paths` after mounting a disk:

```json
{
  "current_working_directory": "/opt/render/project/src",
  "paths_checked": {
    "/opt/render/project/src/data": {
      "exists": true,        ← Disk is mounted!
      "is_directory": true,
      "writable": true       ← You can write to it!
    }
  }
}
```

## 🐛 Troubleshooting

**"exists: false" for my mount path**
→ Check `render.yaml` disk config is uncommented and redeployed

**"Permission denied" when writing**
→ Verify mount path matches exactly (absolute path with `/`)

**Can't find project path**
→ Visit `/paths` endpoint or use shell `pwd` command

## 🎓 Customer Feedback Addressed

Your customer said:
> "It might be good to add this path clarification to the documentation, now it implies that project root is the starting point and you can't know the absolute path when activating the service the first time."

This test app proves your documentation now:
1. ✅ Clearly states paths are **absolute**
2. ✅ Shows how to use `pwd` to find the path
3. ✅ Explains to deploy first, then add disk
4. ✅ Provides concrete examples

## 🚦 Next Steps

1. **Deploy** this app to Render (2 minutes)
2. **Test** the workflow yourself (5 minutes)
3. **Share** the deployed URL with teammates for feedback
4. **Update** your documentation if you find any gaps
5. **Ship** your improved docs with confidence! 🎉

## 💡 Pro Tips

- The **web UI** is best for visual verification
- The **shell script** is best for automated testing
- The **API endpoints** are best for integration testing
- Test both **inside** and **outside** project mount paths
- Verify data **persists** after redeployment

---

**Questions?** Check `README.md` for the full guide or `VISUAL_GUIDE.md` for diagrams!

**Ready to deploy?** Just push to GitHub and connect to Render, or upload the `render.yaml` as a Blueprint!
