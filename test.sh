set -eo pipefail

#COLOR_GREEN=tput setaf 2;
#COLOR_NC=tput sgr0;

echo "Starting black"
uv run black .
echo "OK"

echo "Starting ruff"
uv run ruff check --select I --fix
uv run ruff check --fix
echo "OK"

echo "${COLOR_GREEN}ALL tests passed successfully!${COLOR_NC}"