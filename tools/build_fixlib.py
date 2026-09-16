#!/usr/bin/env python3
import json
import struct
import sys
import tempfile
import zipfile
from pathlib import Path

VERSION = "2.2.0+26.3"
UPSTREAM_VERSION = "2.2.0+26.3"


def patch_class_utf8_exact(path: Path, replacements: dict[str, str]) -> None:
    """Replace only exact CONSTANT_Utf8 values, never package-name substrings."""
    data = bytearray(path.read_bytes())
    if data[:4] != b"\xca\xfe\xba\xbe":
        raise ValueError(f"Not a Java class file: {path}")

    cp_count = struct.unpack_from(">H", data, 8)[0]
    pos = 10
    idx = 1
    patched = set()

    while idx < cp_count:
        tag = data[pos]
        pos += 1
        if tag == 1:
            length = struct.unpack_from(">H", data, pos)[0]
            pos += 2
            raw = bytes(data[pos:pos + length])
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = None
            if text in replacements:
                new_raw = replacements[text].encode("utf-8")
                if len(new_raw) != length:
                    raise ValueError(f"Replacement length mismatch: {text!r}")
                data[pos:pos + length] = new_raw
                patched.add(text)
            pos += length
        elif tag in (3, 4):
            pos += 4
        elif tag in (5, 6):
            pos += 8
            idx += 1
        elif tag in (7, 8, 16, 19, 20):
            pos += 2
        elif tag in (9, 10, 11, 12, 17, 18):
            pos += 4
        elif tag == 15:
            pos += 3
        else:
            raise ValueError(f"Unsupported constant-pool tag {tag} in {path}")
        idx += 1

    missing = set(replacements) - patched
    if missing:
        raise ValueError(f"Expected branding constants not found: {sorted(missing)}")
    path.write_bytes(data)


def main() -> int:
    if len(sys.argv) != 3:
        print(
            "Usage: python3 tools/build_fixlib.py "
            "/path/to/ukulib-fabric-2.2.0+26.3.jar "
            "/path/to/fixlib-2.1.1+26.2.jar"
        )
        return 2

    base_jar = Path(sys.argv[1]).expanduser().resolve()
    branding_jar = Path(sys.argv[2]).expanduser().resolve()
    for label, jar in (("Upstream JAR", base_jar), ("Branding reference JAR", branding_jar)):
        if not jar.is_file():
            print(f"{label} not found: {jar}")
            return 2

    repo_root = Path(__file__).resolve().parents[1]
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
            "description": "Client-side utility library for fixpot47's Fabric mods. Compatibility fork of uku's ukulib 2.2.0 for Minecraft 26.3.",
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

        # Preserve the exact icon/title-screen avatar from the previous FixLib release.
        with zipfile.ZipFile(branding_jar, "r") as branding:
            branding_assets = {
                "assets/fixlib/icon.png": "assets/fixlib/icon.png",
                "assets/ukulib/icon.png": "assets/ukulib/icon.png",
                "assets/ukulib/uku.png": "assets/ukulib/uku.png"
            }
            for source, target in branding_assets.items():
                try:
                    data = branding.read(source)
                except KeyError as exc:
                    raise ValueError(f"Branding reference JAR is missing: {source}") from exc
                target_path = tmp / target
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_bytes(data)

        # Preserve FixLib's established config namespace/default avatar name without
        # touching the legacy net.uku3lig.ukulib package/API.
        config_class = tmp / "net/uku3lig/ukulib/config/impl/UkulibConfig.class"
        patch_class_utf8_exact(config_class, {"ukulib": "fixlib", "uku3lig": "fixlib_"})

        # Rebrand the built-in config title in all bundled translations.
        for lang_path in sorted((tmp / "assets/ukulib/lang").glob("*.json")):
            lang = json.loads(lang_path.read_text(encoding="utf-8"))
            if "ukulib.config.title" in lang:
                lang["ukulib.config.title"] = "FixLib Config"
                lang_path.write_text(json.dumps(lang, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        (tmp / "NOTICE").write_text(
            f"FixLib {VERSION}\n\n"
            f"Compatibility fork/rebrand of uku's ukulib {UPSTREAM_VERSION}.\n"
            "Original project: https://github.com/uku3lig/ukulib\n"
            "Original copyright: Copyright (c) 2023 uku\n"
            "License: Mozilla Public License 2.0 (MPL-2.0)\n"
            "FixLib branding/metadata/config-namespace changes maintained by fixpot47.\n",
            encoding="utf-8"
        )

        # Modified archives cannot keep upstream signatures if they are ever added.
        meta_inf = tmp / "META-INF"
        if meta_inf.exists():
            for pattern in ("*.SF", "*.RSA", "*.DSA", "*.EC"):
                for signature in meta_inf.glob(pattern):
                    signature.unlink()

        with zipfile.ZipFile(out_jar, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(tmp.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(tmp).as_posix())

    print(out_jar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
