#!/usr/bin/env bash
# ==============================================================================
# CivicAudit AI — Production Startup Script (Linux/macOS)
# National Pre-Approval Public Works Evidence Intelligence Gateway
# ==============================================================================

set -e

echo ""
echo "====================================================================="
echo "    CIVICAUDIT AI - NATIONAL PRE-APPROVAL EVIDENCE GATEWAY          "
echo "    Compliant with GFR 2017 Rule 175 & Section 6(1) RTI Act 2005     "
echo "====================================================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# 1. Start Backend in Background
echo "[1/2] Launching FastAPI Backend Gateway on http://127.0.0.1:8002..."
cd "$BACKEND_DIR"
python3 -m uvicorn main:app --host 127.0.0.1 --port 8002 &
BACKEND_PID=$!

# 2. Start Frontend in Background
echo "[2/2] Launching Next.js Frontend Portal on http://localhost:3000..."
cd "$FRONTEND_DIR"
npm run dev -- -p 3000 &
FRONTEND_PID=$!

echo ""
echo "====================================================================="
echo "  SUCCESS! Both CivicAudit AI Services are Live & Operational:      "
echo "  * Frontend GovTech Portal:  http://localhost:3000                 "
echo "  * FastAPI Swagger API Docs: http://127.0.0.1:8002/docs            "
echo "====================================================================="
echo ""

wait $BACKEND_PID $FRONTEND_PID
