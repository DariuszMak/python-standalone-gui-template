CURRENT_DIR="$(pwd)"
cd "$(dirname "$0")"

if [ ! -d "node_modules" ]; then
  npm ci
fi

npx vitest run

cd "$CURRENT_DIR"