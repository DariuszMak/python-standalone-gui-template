Push-Location $PSScriptRoot

npx --yes prettier --write .
npx --yes eslint . --fix
npx --yes tsc --noEmit
npx --yes vitest run
npx --yes vite build

Pop-Location