uv run ruff format test src --exclude 'moc_.*\.py|files_rc\.py'
uv run ruff check --fix test src --exclude 'moc_.*\.py|files_rc\.py'
uv run ruff check --fix --unsafe-fixes test src --exclude 'moc_.*\.py|files_rc\.py'
uv run ruff check --fix --select I test src --exclude 'moc_.*\.py|files_rc\.py'

uv run pip-audit
uv run ruff check test src --exclude 'moc_.*\.py|files_rc\.py'
uv run ruff format --check test src --exclude 'moc_.*\.py|files_rc\.py'
uv run mypy --strict test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 

# uv run mypy --explicit-package-bases test src --exclude 'moc_.*\.py|files_rc\.py'
# uv run mypy --explicit-package-bases --check-untyped-defs test src --exclude 'moc_.*\.py|files_rc\.py'
# uv run mypy --strict test src