Push-Location $PSScriptRoot

npm audit fix
npm audit --audit-level=moderate
npx --yes prettier --write .
npx --yes eslint . --fix
npx --yes tsc --noEmit
npx --yes vitest run
npx --yes vite build
npx knip                          # dead code

Pop-Location