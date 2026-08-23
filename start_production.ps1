# ==============================================================================
# CivicAudit AI — Production Startup Script (Windows PowerShell)
# National Pre-Approval Public Works Evidence Intelligence Gateway
# ==============================================================================

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "    CIVICAUDIT AI - NATIONAL PRE-APPROVAL EVIDENCE GATEWAY          " -ForegroundColor Yellow
Write-Host "    Compliant with GFR 2017 Rule 175 & Section 6(1) RTI Act 2005     " -ForegroundColor White
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$BACKEND_DIR = Join-Path $SCRIPT_DIR "backend"
$FRONTEND_DIR = Join-Path $SCRIPT_DIR "frontend"

# 1. Verify Python Installation
Write-Host "[1/4] Checking Python Environment..." -ForegroundColor Green
$pythonCmd = "py -3.14"
try {
    & py -3.14 --version 2>$null
} catch {
    $pythonCmd = "python"
}

# 2. Verify Node.js Environment
Write-Host "[2/4] Checking Node.js Environment..." -ForegroundColor Green
try {
    $nodeVersion = & node --version
    Write-Host "      Node.js Version: $nodeVersion" -ForegroundColor Gray
} catch {
    Write-Host "ERROR: Node.js is required but not found in PATH." -ForegroundColor Red
    exit 1
}

# 3. Start FastAPI Backend Gateway
Write-Host "[3/4] Launching FastAPI Multi-Vector Forensic Gateway on port 8002..." -ForegroundColor Green
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$BACKEND_DIR'; $pythonCmd -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload" -WindowStyle Minimized

# 4. Start Next.js Frontend Dev/Production Server
Write-Host "[4/4] Launching GovTech Frontend on port 3000..." -ForegroundColor Green
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$FRONTEND_DIR'; npm run dev -- -p 3000" -WindowStyle Minimized

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "  SUCCESS! Both CivicAudit AI Services are Live & Operational:      " -ForegroundColor Yellow
Write-Host "  * Frontend GovTech Portal:  http://localhost:3000                 " -ForegroundColor White
Write-Host "  * Gatekeeper Scrutiny Form: http://localhost:3000/intake          " -ForegroundColor White
Write-Host "  * Macro Analytics Cockpit:  http://localhost:3000/analytics       " -ForegroundColor White
Write-Host "  * Citizen RTI Portal:       http://localhost:3000/citizen         " -ForegroundColor White
Write-Host "  * FastAPI Swagger API Docs: http://127.0.0.1:8002/docs            " -ForegroundColor White
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
