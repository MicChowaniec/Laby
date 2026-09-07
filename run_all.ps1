$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

$PythonExe = $null
$PythonArgs = @()
if (Get-Command python -ErrorAction SilentlyContinue) {
    $Candidate = (Get-Command python).Source
    & $Candidate --version 2>$null
    if ($LASTEXITCODE -eq 0) { $PythonExe = $Candidate }
}

if (-not $PythonExe -and (Get-Command py -ErrorAction SilentlyContinue)) {
    $Candidate = (Get-Command py).Source
    & $Candidate -3 --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $PythonExe = $Candidate
        $PythonArgs = @('-3')
    }
}

if (-not $PythonExe) {
    throw 'Python 3.10+ was not found. Install it from https://www.python.org/downloads/ and select Add Python to PATH.'
}

$VenvRoot = Join-Path $ProjectRoot '.venv'
$VenvPython = Join-Path $VenvRoot 'Scripts\python.exe'
$VenvConfig = Join-Path $VenvRoot 'pyvenv.cfg'

$VenvIsValid = $false
if ((Test-Path -LiteralPath $VenvPython) -and (Test-Path -LiteralPath $VenvConfig)) {
    & $VenvPython -c "import sys; print(sys.executable)" 2>$null | Out-Null
    $VenvIsValid = ($LASTEXITCODE -eq 0)
}

if (-not $VenvIsValid) {
    Write-Host 'Creating or repairing the local .venv environment...'
    & $PythonExe @PythonArgs -m venv --clear $VenvRoot
    if ($LASTEXITCODE -ne 0) { throw 'Could not create or repair the .venv environment.' }
}

if (-not (Test-Path -LiteralPath $VenvConfig)) {
    throw 'The .venv environment is incomplete: pyvenv.cfg is missing.'
}

& $VenvPython -c "import sys; print(sys.version)" 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw 'The .venv Python executable does not work.'
}

$env:MPLBACKEND = 'Agg'
$env:MPLCONFIGDIR = Join-Path $ProjectRoot 'data\mplconfig'
Write-Host "Project Python: $VenvPython"
& $VenvPython -m pip install -r (Join-Path $ProjectRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
& $VenvPython (Join-Path $ProjectRoot 'prepare_data.py')
if ($LASTEXITCODE -ne 0) { throw 'Data preparation failed.' }

$Analyses = @(
    'Lab2_EDA\analysis.py',
    'Lab3_redukcja_wymiarowosci\analysis.py',
    'Lab4_testy_statystyczne\analysis.py',
    'Lab5_redukcja_wymiarowosci\analysis.py',
    'Lab6_szeregi_czasowe\analysis.py'
)

foreach ($Analysis in $Analyses) {
    Write-Host "Running $Analysis"
    & $VenvPython (Join-Path $ProjectRoot $Analysis)
    if ($LASTEXITCODE -ne 0) { throw "Analysis failed: $Analysis" }
}

Write-Host 'Done. Results are available in the wyniki subfolders.'
Write-Host 'Start the dashboard with: .\run_dashboard.ps1'
