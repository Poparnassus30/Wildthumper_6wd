from __future__ import annotations
import os
import sys
import subprocess
from pathlib import Path
import platform

def sh(cmd: list[str], cwd: Path | None = None) -> None:
    print("▶", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(cwd) if cwd else None)

def pip_install_editable(py: str, path: Path) -> None:
    print(f"🧩 MasterLib (editable): {path}")
    sh([py, "-m", "pip", "install", "-e", str(path), "--quiet"])

def resolve_masterlib(app_dir: Path) -> Path:
    # mêmes variables/env que ton start.sh
    masterlib_local = os.environ.get("MASTERLIB_LOCAL", "").strip()
    masterlib_url   = os.environ.get("MASTERLIB_URL", "https://github.com/Poparnassus30/MasterLib.git").strip()
    masterlib_ref   = os.environ.get("MASTERLIB_REF", "dev").strip()
    deps_dir        = Path(os.environ.get("DEPS_DIR", str(app_dir / ".deps")))
    clone_dir       = Path(os.environ.get("MASTERLIB_CLONE_DIR", str(deps_dir / "MasterLib")))

    # 2.a) local explicite
    if masterlib_local:
        p = Path(masterlib_local)
        if p.is_dir():
            return p

    # 2.b) local “standard” si présent (garde ton comportement)
    standard = Path("/home/poparnassus/github/MasterLib")
    if standard.is_dir():
        return standard

    # 2.c) sinon auto-clone/update
    deps_dir.mkdir(parents=True, exist_ok=True)
    if not (clone_dir / ".git").is_dir():
        print("⬇️  Clone MasterLib…")
        sh(["git", "clone", "--branch", masterlib_ref, "--depth", "1", masterlib_url, str(clone_dir)])
    else:
        print("🔄 Update MasterLib…")
        sh(["git", "-C", str(clone_dir), "fetch", "origin", masterlib_ref, "--depth", "1"])
        sh(["git", "-C", str(clone_dir), "reset", "--hard", f"origin/{masterlib_ref}"])
    return clone_dir

def main() -> int:
    app_dir = Path(__file__).resolve().parents[1]
    app_main = Path(os.environ.get("APP_MAIN", str(app_dir / "main.py")))

    os.environ["APP_PATH"] = str(app_dir)
    os.environ["APP_NAME"] = os.environ.get("APP_NAME", app_dir.name)

    print(f"🚗 App: {os.environ['APP_NAME']}")
    print(f"📁 APP_PATH={os.environ['APP_PATH']}")
    print(f"🖥️  OS: {platform.system()}")
    print()

    # On n’utilise PAS de venv custom ici : on part du principe “industriel”
    # = l’utilisateur installe le projet dans un venv/pipx/uv… et la commande marche.
    py = sys.executable
    sh([py, "-m", "pip", "install", "--upgrade", "pip", "--quiet"])

    masterlib_path = resolve_masterlib(app_dir)
    pip_install_editable(py, masterlib_path)

    print(f"▶️  Launch: {app_main}")
    os.execv(py, [py, str(app_main), *sys.argv[1:]])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
