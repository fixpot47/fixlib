#!/usr/bin/env python3
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

VERSION = "2.1.1+26.2"


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("Usage: python3 tools/build_fixlib.py /path/to/ukulib-fabric-2.1.1+26.2.jar [/path/to/fixlib-icon.png]")
        return 2

    base_jar = Path(sys.argv[1]).expanduser().resolve()
    if not base_jar.is_file():
        print(f"Input JAR not found: {base_jar}")
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    icon = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) == 3 else repo_root / "assets" / "fixlib" / "icon.png"
    if not icon.is_file():
        print(f"FixLib icon not found: {icon}")
        return 2

    out_dir = repo_root / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_jar = out_dir / f"fixlib-fabric-{VERSION}.jar"

    with tempfile.TemporaryDirectory(prefix="fixlib-") as tmp_dir:
        tmp = Path(tmp_dir)
        with zipfile.ZipFile(base_jar, "r") as zf:
            zf.extractall(tmp)

        metadata_path = tmp / "fabric.mod.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata.update({
            "id": "fixlib",
            "version": VERSION,
            "name": "FixLib",
            "description": "Client-side utility library for fixpot47's Fabric mods. Compatibility fork of uku's ukulib 2.1.1 for Minecraft 26.2.",
            "authors": ["fixpot47"],
            "contributors": ["uku (original ukulib author)"],
            "provides": ["ukulib"],
            "contact": {
                "sources": "https://github.com/fixpot47/fixlib",
                "issues": "https://github.com/fixpot47/fixlib/issues",
                "homepage": "https://github.com/fixpot47/fixlib"
            },
            "license": "MPL-2.0",
            "icon": "assets/fixlib/icon.png",
            "custom": {"modmenu": {"badges": ["library"]}}
        })
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        (tmp / "assets" / "fixlib").mkdir(parents=True, exist_ok=True)
        shutil.copy2(icon, tmp / "assets" / "fixlib" / "icon.png")
        legacy_icon = tmp / "assets" / "ukulib" / "icon.png"
        legacy_icon.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(icon, legacy_icon)

        (tmp / "NOTICE").write_text(
            "FixLib 2.1.1+26.2\n\n"
            "Compatibility fork/rebrand of uku's ukulib 2.1.1+26.2.\n"
            "Original project: https://github.com/uku3lig/ukulib\n"
            "Original copyright: Copyright (c) 2023 uku\n"
            "License: Mozilla Public License 2.0 (MPL-2.0)\n"
            "FixLib branding/metadata/icon changes maintained by fixpot47.\n",
            encoding="utf-8"
        )

        with zipfile.ZipFile(out_jar, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(tmp.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(tmp).as_posix())

    print(out_jar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
