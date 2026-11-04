"""Prepare the four allowlisted public resources for local Jupyter or Colab."""
from __future__ import annotations

import hashlib
import importlib.metadata
import os
import subprocess
import sys
import urllib.request
from pathlib import Path


REPOSITORY = "handicapskater/datascience"
RESOURCE_SHA256 = {
    "data/public/skating_evidence.v1.json": "123f9ca90c10a39350f2c39b370b7ec8c10708a836688bbadd3b97185e0ccf30",
    "data/public/skating_evidence.v1.sha256": "2715c3330e23d499d470f198a8e36c93cb55b23d6afa11626adef81b59f38d59",
    "scripts/public_notebook_evidence.py": "e5e534ce6eb0b40534540c55a4ef6ce0239b65ed90a0352f2d531faf1cb9444c",
    "requirements-public-runtime.txt": "28b5072f0b65094afae470d004c7a699b31dcaf7cd4292d4e44f4a60f2b5a8e9",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_repository_root(start: Path) -> Path:
    """Find a local checkout; a copied standalone notebook is insufficient."""
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "scripts/public_notebook_bootstrap.py").is_file() and (candidate / "data/public/skating_evidence.v1.json").is_file():
            return candidate
    raise FileNotFoundError("Open the notebook from the datascience repository checkout, or use its Colab launch link. Required scripts/ and data/public/ were not found.")


def _fetch(relative: str, commit: str, target: Path, opener=urllib.request.urlopen) -> None:
    if relative not in RESOURCE_SHA256:
        raise ValueError(f"Resource is outside the public allowlist: {relative}")
    if len(commit) != 40 or any(char not in "0123456789abcdef" for char in commit):
        raise ValueError("A full 40-character Git commit SHA is required")
    if target.is_file() and sha256(target) == RESOURCE_SHA256[relative]:
        return
    url = f"https://raw.githubusercontent.com/{REPOSITORY}/{commit}/{relative}"
    try:
        with opener(url, timeout=30) as response:
            content = response.read()
    except Exception as exc:
        raise RuntimeError(f"Could not download {relative} from pinned commit {commit}. Check Colab network access and the public GitHub repository.") from exc
    if hashlib.sha256(content).hexdigest() != RESOURCE_SHA256[relative]:
        raise ValueError(f"Downloaded {relative} failed its pinned SHA-256 check")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".download")
    temporary.write_bytes(content)
    os.replace(temporary, target)


def ensure_resources(root: Path, commit: str, *, download: bool, opener=urllib.request.urlopen) -> None:
    for relative, expected in RESOURCE_SHA256.items():
        target = root / relative
        if download:
            _fetch(relative, commit, target, opener=opener)
        elif not target.is_file() or sha256(target) != expected:
            raise FileNotFoundError(f"Missing or changed public resource: {relative}. Restore the reviewed repository checkout at commit {commit}.")


def ensure_runtime_dependencies(requirements: Path, *, installer=subprocess.check_call) -> bool:
    """Install the small runtime requirement only when missing or out of range."""
    if not requirements.is_file():
        raise FileNotFoundError(f"Missing runtime requirements: {requirements}")
    if requirements.read_text(encoding="utf-8").splitlines()[-1] != "matplotlib>=3.9,<4":
        raise ValueError("Unexpected runtime dependency specification")
    try:
        major, minor = (int(part) for part in importlib.metadata.version("matplotlib").split(".")[:2])
        installed = (major, minor) >= (3, 9) and major < 4
    except (importlib.metadata.PackageNotFoundError, ValueError):
        installed = False
    if installed:
        return False
    try:
        installer([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "-r", str(requirements)])
    except Exception as exc:
        raise RuntimeError("Could not install the public notebook runtime dependencies. Run pip install -r requirements-public-runtime.txt, then retry.") from exc
    return True


def prepare_environment(root: Path, commit: str, *, colab: bool, opener=urllib.request.urlopen, install: bool = True) -> Path:
    """Fetch only pinned public files in Colab; verify local files in Jupyter."""
    root = root.resolve()
    ensure_resources(root, commit, download=colab, opener=opener)
    if install:
        ensure_runtime_dependencies(root / "requirements-public-runtime.txt")
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root
