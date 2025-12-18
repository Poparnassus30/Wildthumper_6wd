#!/usr/bin/env bash
set -euo pipefail

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${VENV_DIR:-$APP_DIR/.venv}"
PY="$VENV_DIR/bin/python"
APP_MAIN="${APP_MAIN:-$APP_DIR/main.py}"

# --- MasterLib source (priorité au local, sinon auto-clone) ---
MASTERLIB_LOCAL="${MASTERLIB_LOCAL:-}"  # ex: /home/poparnassus/github/MasterLib
MASTERLIB_URL="${MASTERLIB_URL:-https://github.com/Poparnassus30/MasterLib.git}"
MASTERLIB_REF="${MASTERLIB_REF:-dev}"   # dev / main / tag
DEPS_DIR="${DEPS_DIR:-$APP_DIR/.deps}"
MASTERLIB_CLONE_DIR="${MASTERLIB_CLONE_DIR:-$DEPS_DIR/MasterLib}"

export APP_PATH="$APP_DIR"
export APP_NAME="${APP_NAME:-$(basename "$APP_DIR")}"

echo "🚗 App: $APP_NAME"
echo "📁 APP_PATH=$APP_PATH"
echo "🧪 Venv: $VENV_DIR"
echo

# 1) venv
if [[ ! -d "$VENV_DIR" ]]; then
  echo "🔧 Création venv…"
  python3 -m venv "$VENV_DIR"
fi
"$PY" -m pip install --upgrade pip --quiet

# 2) installer MasterLib
install_masterlib_editable () {
  local path="$1"
  echo "🧩 MasterLib (editable): $path"
  "$PY" -m pip install -e "$path" --quiet
}

# 2.a) si local explicite
if [[ -n "$MASTERLIB_LOCAL" && -d "$MASTERLIB_LOCAL" ]]; then
  install_masterlib_editable "$MASTERLIB_LOCAL"

else
  # 2.b) si local “standard” existe
  if [[ -d "/home/poparnassus/github/MasterLib" ]]; then
    install_masterlib_editable "/home/poparnassus/github/MasterLib"
  else
    # 2.c) sinon auto-clone + update
    mkdir -p "$DEPS_DIR"
    if [[ ! -d "$MASTERLIB_CLONE_DIR/.git" ]]; then
      echo "⬇️  Clone MasterLib…"
      git clone --branch "$MASTERLIB_REF" --depth 1 "$MASTERLIB_URL" "$MASTERLIB_CLONE_DIR"
    else
      echo "🔄 Update MasterLib…"
      git -C "$MASTERLIB_CLONE_DIR" fetch origin "$MASTERLIB_REF" --depth 1
      git -C "$MASTERLIB_CLONE_DIR" reset --hard "origin/$MASTERLIB_REF"
    fi
    install_masterlib_editable "$MASTERLIB_CLONE_DIR"
  fi
fi

# 3) CTRL+Q (souvent bloqué par XON/XOFF)
if [[ -t 0 ]]; then
  stty -ixon 2>/dev/null || true
fi

echo "▶️  Launch: $APP_MAIN"
exec "$PY" "$APP_MAIN" "$@"
