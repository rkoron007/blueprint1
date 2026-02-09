#!/bin/bash

# Render Disk Mount Path Tester
# Quick command-line test script for the documentation workflow

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if app URL is provided
if [ -z "$1" ]; then
    echo -e "${RED}Usage: $0 <app-url>${NC}"
    echo "Example: $0 https://disk-mount-test-app.onrender.com"
    exit 1
fi

APP_URL="$1"
# Remove trailing slash if present
APP_URL="${APP_URL%/}"

echo "================================================"
echo "  Render Disk Mount Path Documentation Test"
echo "================================================"
echo ""

# Step 1: Health check
echo -e "${YELLOW}Step 1: Checking if app is deployed...${NC}"
if curl -s -f "$APP_URL/health" > /dev/null; then
    echo -e "${GREEN}✓ App is healthy and responding${NC}"
else
    echo -e "${RED}✗ App is not responding. Check deployment.${NC}"
    exit 1
fi
echo ""

# Step 2: Find project path
echo -e "${YELLOW}Step 2: Finding project absolute path (this is the 'pwd' step)...${NC}"
PROJECT_PATH=$(curl -s "$APP_URL/paths" | grep -o '"current_working_directory": "[^"]*"' | cut -d'"' -f4)

if [ -z "$PROJECT_PATH" ]; then
    echo -e "${RED}✗ Could not determine project path${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Project path found: $PROJECT_PATH${NC}"
echo ""
echo "  📝 Documentation step: In your terminal, you would run 'pwd' and see:"
echo "     $PROJECT_PATH"
echo ""

# Suggested mount paths
MOUNT_PATH_INSIDE="$PROJECT_PATH/data"
MOUNT_PATH_OUTSIDE="/var/data"

echo -e "${YELLOW}Step 3: Suggested disk mount paths...${NC}"
echo "  Option A (inside project): $MOUNT_PATH_INSIDE"
echo "  Option B (outside project): $MOUNT_PATH_OUTSIDE"
echo ""
echo "  📝 Documentation step: Add to render.yaml:"
echo "     disk:"
echo "       name: test-disk"
echo "       mountPath: $MOUNT_PATH_INSIDE"
echo "       sizeGB: 1"
echo ""

# Step 4: Check all paths
echo -e "${YELLOW}Step 4: Checking which paths are mounted...${NC}"
curl -s "$APP_URL/paths" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('  Current directory:', data['current_working_directory'])
print()
print('  Paths checked:')
for path, info in data['paths_checked'].items():
    if info['exists']:
        status = '✓ Writable' if info['writable'] else '⚠ Read-only'
        color = '\033[0;32m' if info['writable'] else '\033[1;33m'
    else:
        status = '✗ Not found'
        color = '\033[0;31m'
    print(f'  {color}{status}\033[0m {path}')
"
echo ""

# Step 5: Test write operation
echo -e "${YELLOW}Step 5: Testing write operation...${NC}"
echo "  Testing path: $MOUNT_PATH_INSIDE"

WRITE_RESULT=$(curl -s -X POST "$APP_URL/write?path=$MOUNT_PATH_INSIDE")
WRITE_STATUS=$(echo "$WRITE_RESULT" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)

if [ "$WRITE_STATUS" = "success" ]; then
    echo -e "${GREEN}✓ Write operation successful${NC}"
    echo "$WRITE_RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('  Written to:', data.get('path', 'N/A'))
print('  Content:', data.get('content', 'N/A'))
"
else
    echo -e "${RED}✗ Write operation failed${NC}"
    echo "  If this fails, you need to:"
    echo "  1. Add disk configuration to render.yaml"
    echo "  2. Redeploy the service"
    echo ""
    echo "  Error details:"
    echo "$WRITE_RESULT" | python3 -m json.tool
    echo ""
    exit 0  # Don't exit with error, this is expected if disk not mounted yet
fi
echo ""

# Step 6: Test read operation
echo -e "${YELLOW}Step 6: Testing read operation...${NC}"
echo "  Reading from: $MOUNT_PATH_INSIDE"

READ_RESULT=$(curl -s "$APP_URL/read?path=$MOUNT_PATH_INSIDE")
READ_STATUS=$(echo "$READ_RESULT" | grep -o '"status": "[^"]*"' | cut -d'"' -f4)

if [ "$READ_STATUS" = "success" ]; then
    echo -e "${GREEN}✓ Read operation successful${NC}"
    echo "$READ_RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('  Read from:', data.get('path', 'N/A'))
print('  Content:', data.get('content', 'N/A'))
"
else
    echo -e "${RED}✗ Read operation failed${NC}"
    echo "  Error details:"
    echo "$READ_RESULT" | python3 -m json.tool
fi
echo ""

# Summary
echo "================================================"
echo "  Test Summary"
echo "================================================"
echo ""
echo "Documentation workflow validation:"
echo "  ✓ Step 1: Deploy without disk - TESTED"
echo "  ✓ Step 2: Find path with 'pwd' - SIMULATED ($PROJECT_PATH)"
echo "  ? Step 3: Add disk to render.yaml - MANUAL STEP REQUIRED"
echo "  ? Step 4: Verify write/read - $([ "$WRITE_STATUS" = "success" ] && echo 'PASSED' || echo 'NEEDS DISK')"
echo ""

if [ "$WRITE_STATUS" = "success" ]; then
    echo -e "${GREEN}🎉 All tests passed! Your disk is properly mounted.${NC}"
    echo ""
    echo "Your documentation is correct! Users can:"
    echo "  1. Deploy their service"
    echo "  2. Run 'pwd' to find: $PROJECT_PATH"
    echo "  3. Mount disk at: $MOUNT_PATH_INSIDE (or similar)"
    echo "  4. Successfully read/write data"
else
    echo -e "${YELLOW}⚠ Next step: Add disk configuration to render.yaml${NC}"
    echo ""
    echo "Add this to your render.yaml:"
    echo ""
    echo "services:"
    echo "  - type: web"
    echo "    name: disk-mount-test-app"
    echo "    # ... other config ..."
    echo "    disk:"
    echo "      name: test-disk"
    echo "      mountPath: $MOUNT_PATH_INSIDE"
    echo "      sizeGB: 1"
    echo ""
    echo "Then redeploy and run this script again!"
fi

echo ""
echo "================================================"
echo ""
