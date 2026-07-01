param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"

Write-Host "╔══════════════════════════════════════════╗"
Write-Host "║  MyNotes AI — Backend Smoke Test        ║"
Write-Host "╚══════════════════════════════════════════╝"
Write-Host "Target: $BaseUrl`n"

# ── Helper ──────────────────────────────────────────────────────
$passed = 0
$failed = 0

function Test-Step {
    param([string]$Name, [scriptblock]$Block)
    try {
        & $Block
        Write-Host "  ✓ $Name" -ForegroundColor Green
        $script:passed++
    } catch {
        Write-Host "  ✗ $Name" -ForegroundColor Red
        Write-Host "    Error: $_" -ForegroundColor Red
        $script:failed++
    }
}

# ── 1. Health ───────────────────────────────────────────────────
Write-Host "── 1. Health check ──"
Test-Step -Name "GET /api/health returns 200" -Block {
    $r = Invoke-RestMethod -Uri "$BaseUrl/api/health" -Method GET -TimeoutSec 5
    if ($r.status -ne "ok") { throw "Expected status=ok, got $($r.status)" }
}

# ── 2. GET settings (initial) ───────────────────────────────────
Write-Host "`n── 2. Read AI settings ──"
Test-Step -Name "GET /api/ai/settings returns 200" -Block {
    $r = Invoke-RestMethod -Uri "$BaseUrl/api/ai/settings" -Method GET -TimeoutSec 5
    if (-not $r.PSObject.Properties.Name -contains "hasApiKey") {
        throw "Response missing hasApiKey field"
    }
    Write-Host "    provider=$($r.provider)  hasApiKey=$($r.hasApiKey)" -ForegroundColor Gray
}

# ── 3. PUT settings (save mock) ─────────────────────────────────
Write-Host "`n── 3. Save AI settings (mock) ──"
Test-Step -Name "PUT /api/ai/settings returns 200 with mock" -Block {
    $body = @{
        provider       = "mock"
        baseUrl        = "https://api.deepseek.com"
        model          = "deepseek-v4-flash"
        temperature    = 0.3
        timeoutSeconds = 40
    } | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "$BaseUrl/api/ai/settings" -Method PUT -Body $body -ContentType "application/json" -TimeoutSec 5
    if ($r.provider -ne "mock") { throw "Expected provider=mock, got $($r.provider)" }
    Write-Host "    provider=$($r.provider)  hasApiKey=$($r.hasApiKey)" -ForegroundColor Gray
}

# ── 4. GET settings (verify persistence) ────────────────────────
Write-Host "`n── 4. Verify settings persisted ──"
Test-Step -Name "GET /api/ai/settings after save" -Block {
    $r = Invoke-RestMethod -Uri "$BaseUrl/api/ai/settings" -Method GET -TimeoutSec 5
    if ($r.provider -ne "mock") { throw "Expected provider=mock, got $($r.provider)" }
    Write-Host "    provider=$($r.provider) — persistence OK" -ForegroundColor Gray
}

# ── 5. AI test (mock mode) ──────────────────────────────────────
Write-Host "`n── 5. Test AI (mock mode) ──"
Test-Step -Name "POST /api/ai/test returns mock result" -Block {
    $body = @{ prompt = "Say hi" } | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "$BaseUrl/api/ai/test" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 10
    if ($r.mode -ne "mock") { throw "Expected mode=mock, got $($r.mode)" }
    if ($r.ok -ne $true) { throw "Expected ok=true" }
    Write-Host "    mode=$($r.mode)  message=$($r.message)" -ForegroundColor Gray
}

# ── Summary ─────────────────────────────────────────────────────
Write-Host "`n── Results ──"
Write-Host "Passed: $passed   Failed: $failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
if ($failed -eq 0) {
    Write-Host "All smoke tests passed!" -ForegroundColor Green
} else {
    Write-Host "Some tests failed." -ForegroundColor Red
    exit 1
}
