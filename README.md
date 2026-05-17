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

.\tasks\wait_for_windows_api.ps1

.\tasks\test_windows_api.ps1
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

.\tasks\build_release.ps1

########## RUN APPLICATIONS LOCALLY

.\tasks\run_linux_application.ps1

.\tasks\wait_for_linux_api.ps1

.\tasks\test_linux_api.ps1

##### Windows runtime uses no .env file, just default values

.\tasks\run_windows_application.ps1

.\tasks\wait_for_windows_api.ps1
 
.\tasks\test_windows_api.ps1

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
