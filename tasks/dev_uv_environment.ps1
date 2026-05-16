uv python install 3.13 ; 
uv python pin 3.13 ; 
uv sync --dev --no-cache ; 
uv lock ; 

.venv\Scripts\Activate.ps1 ; 
$env:UV_ENV_FILE = ".dev.env" ; 
