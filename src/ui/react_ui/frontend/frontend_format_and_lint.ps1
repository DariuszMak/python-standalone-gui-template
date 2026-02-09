Push-Location $PSScriptRoot

npx --yes eslint . --fix
npx --yes tsc --noEmit
npx --yes vite build

Pop-Location