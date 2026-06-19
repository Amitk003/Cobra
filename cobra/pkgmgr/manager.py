import json
import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlparse


COBRA_DIR = Path.home() / ".cobra"
PACKAGES_DIR = COBRA_DIR / "packages"
REGISTRY_URL = "https://raw.githubusercontent.com/Amitk003/cobra-registry/main/packages.json"


def ensure_dirs():
    COBRA_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)


def get_manifest_path(project_dir="."):
    return Path(project_dir) / "cobra-pkg.json"


def init(project_dir="."):
    ensure_dirs()
    manifest_path = get_manifest_path(project_dir)
    if manifest_path.exists():
        print(f"cobra-pkg.json already exists in {project_dir}")
        return

    manifest = {
        "name": Path(project_dir).resolve().name,
        "version": "0.1.0",
        "description": "",
        "dependencies": {}
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Created {manifest_path}")


def install(package_spec, project_dir="."):
    ensure_dirs()
    manifest_path = get_manifest_path(project_dir)
    manifest = {"dependencies": {}}
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)

    if package_spec.startswith("http://") or package_spec.startswith("https://"):
        url = package_spec
        name = url.split("/")[-1].replace(".zip", "").replace(".git", "")
    else:
        name = package_spec
        url = f"https://github.com/{package_spec}/archive/main.zip" if "/" in package_spec else None

    target_dir = PACKAGES_DIR / name
    if target_dir.exists():
        print(f"Package '{name}' is already installed")
        return

    if url:
        print(f"Downloading {name} from {url}...")
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                zip_path = os.path.join(tmp_dir, "package.zip")
                _download(url, zip_path)
                with zipfile.ZipFile(zip_path, "r") as zf:
                    zf.extractall(tmp_dir)
                extracted = os.path.join(tmp_dir, os.listdir(tmp_dir)[0])
                if os.path.isdir(extracted):
                    shutil.copytree(extracted, target_dir)
                else:
                    shutil.copy2(extracted, target_dir / os.path.basename(extracted))
            print(f"Installed {name}")
        except Exception as e:
            print(f"Failed to install {name}: {e}")
            return
    else:
        print(f"Could not resolve package '{name}'")
        return

    manifest.setdefault("dependencies", {})[name] = "0.1.0"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)


def uninstall(name, project_dir="."):
    target_dir = PACKAGES_DIR / name
    if not target_dir.exists():
        print(f"Package '{name}' is not installed")
        return

    shutil.rmtree(target_dir)
    manifest_path = get_manifest_path(project_dir)
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        manifest.get("dependencies", {}).pop(name, None)
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
    print(f"Uninstalled {name}")


def list_packages():
    ensure_dirs()
    if not PACKAGES_DIR.exists():
        print("No packages installed")
        return

    packages = [d for d in PACKAGES_DIR.iterdir() if d.is_dir()]
    if not packages:
        print("No packages installed")
        return

    print("Installed packages:")
    for pkg in sorted(packages):
        manifest_file = pkg / "cobra-pkg.json"
        version = "unknown"
        if manifest_file.exists():
            with open(manifest_file) as f:
                version = json.load(f).get("version", "unknown")
        print(f"  {pkg.name} v{version}")


def _download(url, dest):
    with urlopen(url) as response:
        with open(dest, "wb") as f:
            f.write(response.read())
