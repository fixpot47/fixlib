#!/usr/bin/env python3
"""Import pinned ukulib source and apply FixLib edits, preserving attribution."""
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
import io, json, shutil

ROOT = Path(__file__).resolve().parents[1]
COMMIT = "4831e85a5f9af891ce287e97ef01f00d61b1a3ae"
URL = f"https://github.com/uku3lig/ukulib/archive/{COMMIT}.zip"
if (ROOT / "fabric/src/main/resources/fabric.mod.json").exists():
    print("Source already imported; not overwriting")
    raise SystemExit(0)

data = urlopen(URL, timeout=120).read()
with ZipFile(io.BytesIO(data)) as archive:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        archive.extractall(tmp)
        src = next(Path(tmp).glob("ukulib-*"))
        for name in ("common", "fabric", "neoforge", "buildSrc", "gradle",
                     "build.gradle.kts", "settings.gradle.kts", "gradle.properties",
                     "gradlew", "gradlew.bat", "lombok.config", ".gitignore"):
            source = src / name
            if not source.exists():
                raise FileNotFoundError(source)
            dest = ROOT / name
            if source.is_dir():
                shutil.copytree(source, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(source, dest)

conf = ROOT / "common/src/main/java/net/uku3lig/ukulib/config/impl/UkulibConfig.java"
s = conf.read_text()
assert 'UkulibConfig.class, "ukulib"' in s and 'headName = "uku3lig"' in s
s = s.replace('UkulibConfig.class, "ukulib"', 'UkulibConfig.class, "fixlib"')
s = s.replace('headName = "uku3lig"', 'headName = "fixlib_"')
conf.write_text(s)

meta_path = ROOT / "fabric/src/main/resources/fabric.mod.json"
meta = json.loads(meta_path.read_text())
meta.update({
    "id": "fixlib", "name": "FixLib",
    "description": "Compatibility fork of ukulib for Minecraft Fabric",
    "authors": ["fixpot47"],
    "contributors": ["uku (original ukulib author)"],
    "provides": ["ukulib"],
    "contact": {
        "homepage": "https://github.com/fixpot47/fixlib",
        "issues": "https://github.com/fixpot47/fixlib/issues",
        "sources": "https://github.com/fixpot47/fixlib"
    }
})
meta.pop("custom", None)
meta["custom"] = {"modmenu": {"badges": ["library"]}}
meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")

settings = ROOT / "settings.gradle.kts"
settings.write_text(settings.read_text().replace('rootProject.name = "ukulib"', 'rootProject.name = "fixlib"'))
for p in (ROOT / "fabric/src/main/resources/assets/ukulib/lang").glob("*.json"):
    lang = json.loads(p.read_text())
    if "ukulib.config.title" in lang:
        lang["ukulib.config.title"] = "FixLib Config"
        p.write_text(json.dumps(lang, ensure_ascii=False, indent=2) + "\n")

# Keep original project license/attribution and publish the complete buildable source.
print("Imported and modified pinned ukulib sources for FixLib.")
