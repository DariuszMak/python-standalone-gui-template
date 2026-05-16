# Python Standalone GUI template

### Executable files do download for Windows and Linux

<table>
  <tr>
    <th style="text-align: center;">Windows (click on image):</th>
    <th style="width: 100px;"></th>
    <th style="text-align: center;">Linux (click on image):</th>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/DariuszMak/python-standalone-gui-template/releases/download/0.18.0/GUI_client.exe">
        <img src="images/Windows_runtime_screenshot.png" width="200px" alt="Windows Preview">
      </a>
    </td>
    <td></td>
    <td align="center">
      <a href="https://github.com/DariuszMak/python-standalone-gui-template/releases/download/0.18.0/GUI_client">
        <img src="images/Linux_runtime_screenshot.png" width="200px" alt="Linux Preview">
      </a>
    </td>
  </tr>
</table>

### Project structure diagrams

##### Modular perspective

<p align="center">
  <img src="images/structure_module.svg" alt="Modular perspective" width="600">
</p>

##### Library dependencies perspective

<p align="center">
  <img src="images/structure_module_clustered.svg" alt="Library dependencies perspective" width="600">
</p>

## Requirements

- [UV](https://github.com/astral-sh/uv) package manager
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Local development (Windows PowerShell)

You can also use VSCode `settings.json` and `launch.json` files to run the project (choose interpreter created by UV).

## Fast native Windows development

```commandline
.\tasks\cleanup.ps1 ; 

#####

.\tasks\dev_uv_environment.ps1

.\tasks\static_analysis_and_tests.ps1

########## RUN APPLICATION LOCALLY

.\tasks\kibana_elastic.ps1

Start-Process uv -ArgumentList "run", "python", "src\main.py" ; 

do {
    Start-Sleep -Seconds 3

    try {
        $api = Invoke-RestMethod `
            -Uri "http://127.0.0.1:8000/openapi.json" `
            -Method Get
    }
    catch {
        $api = $null
    }

} until ($api)

newman run collections\Python_GUI_API.postman_collection.json --environment collections\environments_API\API_Windows.postman_environment.json ; 
newman run collections\Python_GUI_UI.postman_collection.json --environment collections\environments_UI\Panel_UI_Dev_Windows.postman_environment.json ; 
newman run collections\Python_GUI_UI.postman_collection.json --environment collections\environments_UI\React_UI_Dev_Windows.postman_environment.json ; 

Start-Process "http://127.0.0.1:8000/openapi.json" ; 
Start-Process "http://127.0.0.1:8000/redoc" ; 
Start-Process "http://127.0.0.1:8000/docs" ; 
Start-Process "http://127.0.0.1:8001" ; 
Start-Process "http://127.0.0.1:8002" ; 
```

## Full static analysis

Login in SonarQube as `admin` with password `Admin1@Admin1@`.

```commandline
.\tasks\cleanup.ps1 ; 

#####

.\tasks\dev_uv_environment.ps1

.\tasks\static_analysis_and_tests.ps1

.\tasks\sonarqube.ps1

.\tasks\generate_diagrams.ps1
```

## Thorough setup from scratch for Windows and Linux enviroment

```commandline
.\tasks\cleanup.ps1 ; 

#####

docker-compose run --build app ; 

uv python install 3.13 ; 
uv python pin 3.13 ; 
uv sync --dev --no-cache --locked ; 

#####

.venv\Scripts\Activate.ps1 ; 
$env:UV_ENV_FILE = ".dev.env" ; 

.\scripts\format_and_lint.ps1 ; 
.\src\ui\react_ui\frontend\frontend_format_and_lint.ps1 ; 

docker-compose run app sh -c "dos2unix thorough.env src/ui/react_ui/frontend/frontend_test.sh" ; 
docker-compose run app sh -c "cd src/ui/react_ui/frontend && rm -rf node_modules package-lock.json && npm install && cd /app && uv sync --dev --locked --no-cache && chmod +x src/ui/react_ui/frontend/frontend_test.sh && src/ui/react_ui/frontend/frontend_test.sh && uv run pytest tests/ --cov=src"
docker-compose run --rm --remove-orphans app sh -c "uv sync --dev --locked --no-cache && uv run pyinstaller --clean ./scripts/standalone_build_linux.spec && cp -r dist/* releases/linux/" ; 
rm -r -fo .\dist, .\build, .\linux ; 

cd src\ui\react_ui\frontend ; 
if (Test-Path node_modules) {
    Remove-Item -Recurse -Force node_modules
}
del package-lock.json ; 
npm cache clean --force ; 
npm install ; 
cd (git rev-parse --show-toplevel)

.\src\ui\react_ui\frontend\frontend_test.ps1 ; 
uv run pytest tests/ --cov=src -vv ;
uv sync --no-dev --locked --no-cache ; 
uv run pyinstaller --clean .\scripts\standalone_build_windows.spec ; 
cp -r -fo .\dist\* .\releases\windows\ ; 
rm -r -fo .\dist, .\build ; 

########## RUN APPLICATIONS LOCALLY

Start-Process wsl -ArgumentList @(
    'bash', '-c',
    'export DISPLAY=$(grep nameserver /etc/resolv.conf | awk "{print \$2}"):0 && \
     export QT_QPA_PLATFORM=wayland && \
     set -a && source thorough.env && set +a && \
     export API_HOST=$LINUX_API_HOST && \
     export API_PORT=$LINUX_API_PORT && \
     export PANEL_HOST=$LINUX_PANEL_HOST && \
     export PANEL_PORT=$LINUX_PANEL_PORT && \
     export REACT_HOST=$LINUX_REACT_HOST && \
     export REACT_PORT=$LINUX_REACT_PORT && \
     export LOG_FILE=$LINUX_LOG_FILE && \
     ./releases/linux/GUI_client'
)

do {
    Start-Sleep -Seconds 3

    try {
        $api = Invoke-RestMethod `
            -Uri "http://127.0.0.1:8003/openapi.json" `
            -Method Get
    }
    catch {
        $api = $null
    }

} until ($api)

newman run collections\Python_GUI_API.postman_collection.json --environment collections\environments_API\API_Linux.postman_environment.json ; 
newman run collections\Python_GUI_UI.postman_collection.json --environment collections\environments_UI\Panel_UI_Linux.postman_environment.json ; 
newman run collections\Python_GUI_UI.postman_collection.json --environment collections\environments_UI\React_UI_Linux.postman_environment.json ; 

Start-Process "http://127.0.0.1:8003/openapi.json" ; 
Start-Process "http://127.0.0.1:8003/redoc" ; 
Start-Process "http://127.0.0.1:8003/docs" ; 
Start-Process "http://127.0.0.1:8004" ; 
Start-Process "http://127.0.0.1:8005" ; 

##### Windows runtime uses no .env file, just default values

Start-Process .\releases\windows\GUI_client.exe ; 

do {
    Start-Sleep -Seconds 3

    try {
        $api = Invoke-RestMethod `
            -Uri "http://127.0.0.1:8000/openapi.json" `
            -Method Get
    }
    catch {
        $api = $null
    }

} until ($api)
 
newman run collections\Python_GUI_API.postman_collection.json --environment collections\environments_API\API_Windows.postman_environment.json ; 
newman run collections\Python_GUI_UI.postman_collection.json --environment collections\environments_UI\Panel_UI_Windows.postman_environment.json ; 
newman run collections\Python_GUI_UI.postman_collection.json --environment collections\environments_UI\React_UI_Windows.postman_environment.json ; 

Start-Process "http://127.0.0.1:8000/openapi.json" ; 
Start-Process "http://127.0.0.1:8000/redoc" ; 
Start-Process "http://127.0.0.1:8000/docs" ; 
Start-Process "http://127.0.0.1:8001" ; 
Start-Process "http://127.0.0.1:8002" ;

#####

uv sync --dev --locked --no-cache ; 
```

## Edit `ui` forms with QT Designer

```commandline
uv run pyside6-designer src\ui\pyside_ui\forms\main_window.ui ; 
uv run pyside6-designer src\ui\pyside_ui\forms\warning_dialog.ui ; 
```

### GUI files specification

<mark>.qrc</mark> - resources file edited in QT Designer

<mark>.ui</mark> - QT Designer form

<mark>ui_*.py</mark> - QT Designer generated tools
