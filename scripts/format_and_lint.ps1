uv run ruff format tests src --exclude 'moc_.*\.py|files_rc\.py'
uv run ruff check --fix tests src --exclude 'moc_.*\.py|files_rc\.py'
uv run ruff check --fix --unsafe-fixes tests src --exclude 'moc_.*\.py|files_rc\.py'
uv run ruff check --fix --select I tests src --exclude 'moc_.*\.py|files_rc\.py'

uv run vulture src tests --exclude "src/ui/pyside_ui/forms" --min-confidence 80

uv run pip-audit
uv run ruff check tests src --exclude 'moc_.*\.py|files_rc\.py'
uv run ruff format --check tests src --exclude 'moc_.*\.py|files_rc\.py'

uv run mypy --strict tests src --exclude 'moc_.*\.py|files_rc\.py'

# uv run mypy --explicit-package-bases tests src --exclude 'moc_.*\.py|files_rc\.py'
# uv run mypy --explicit-package-bases --check-untyped-defs tests src --exclude 'moc_.*\.py|files_rc\.py'
# uv run mypy --strict tests src