#!/usr/bin/env bash
set -euo pipefail

# Директория со скриптом
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Путь к виртуальному окружению
VENV_DIR="${SCRIPT_DIR}/.venv"

# Python из виртуального окружения
PYTHON_BIN="${VENV_DIR}/bin/python"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "[✗] Не найден интерпретатор ${PYTHON_BIN}"
  echo "    Убедись, что venv существует и активируй его, например:"
  echo "    python3 -m venv venv"
  echo "    ${VENV_DIR}/bin/pip install aiohttp"
  exit 1
fi

echo "[*] Запускаю change_ip.py..."

set +e
"${PYTHON_BIN}" "${SCRIPT_DIR}/change_ip.py"
STATUS=$?
set -e

if [[ $STATUS -eq 0 ]]; then
  echo "[✓] IP успешно обновлен в рабочей системе"
else
  echo "[✗] Ошибка при обновлении IP (код ${STATUS})"
fi
