$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvRoot = Join-Path $ProjectRoot '.venv'
$VenvPython = Join-Path $VenvRoot 'Scripts\python.exe'
$VenvConfig = Join-Path $VenvRoot 'pyvenv.cfg'

if (-not (Test-Path -LiteralPath $VenvPython) -or -not (Test-Path -LiteralPath $VenvConfig)) {
    throw 'The .venv environment is missing. Run .\run_all.ps1 first.'
}

& $VenvPython -c "import sys" 2>$null
if ($LASTEXITCODE -ne 0) {
    throw 'The .venv environment is damaged. Run .\run_all.ps1 to repair it.'
}

Set-Location -LiteralPath $ProjectRoot
& $VenvPython -m streamlit run (Join-Path $ProjectRoot 'Lab1_dashboard\app.py')
