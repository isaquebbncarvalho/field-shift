# Instalação no Windows (PowerShell). Rode na raiz do repositório:
#   powershell -ExecutionPolicy Bypass -File setup\setup.ps1

$ErrorActionPreference = "Stop"
Write-Host "== Field Shift: instalação ==" -ForegroundColor Green

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host "Python não encontrado. Instale o Python 3.10+ em https://www.python.org/downloads/ (marque 'Add to PATH')." -ForegroundColor Red
    exit 1
}
python --version

if (-not (Test-Path ".venv")) { python -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip -q
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt -q

Write-Host "`n== Testes ==" -ForegroundColor Green
& .\.venv\Scripts\python.exe -m pytest -q

Write-Host "`nPronto. Para abrir o app:" -ForegroundColor Green
Write-Host "  .\.venv\Scripts\activate"
Write-Host "  streamlit run app\streamlit_app.py"

$claude = Get-Command claude -ErrorAction SilentlyContinue
if ($claude) {
    Write-Host "`nClaude Code encontrado. Skills e plugins recomendados: veja setup\ferramentas.md" -ForegroundColor Yellow
}
