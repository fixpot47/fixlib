# FixLib

**FixLib** is a client-side utility library for Fabric mods by **fixpot47**.

Current version: **2.1.1+26.2**  
Minecraft: **26.2**  
Loader: **Fabric**

## Compatibility

FixLib 2.1.1 is a compatibility fork/rebrand of **ukuLib 2.1.1+26.2**. It intentionally preserves the legacy `net.uku3lig.ukulib` Java API and the `ukulib` entrypoint key so existing mods can be migrated with minimal changes.

The Fabric mod id is `fixlib`, and FixLib declares that it provides `ukulib` for compatibility.

## What changed

- Mod name/id changed to **FixLib / `fixlib`**
- Author metadata changed to **fixpot47**
- FixLib icon is based on the custom image supplied by fixpot47
- Source/issues links point to this repository
- `ukulib` is provided as a compatibility alias
- Original API/classes remain intact for compatibility

## Build / reproduce the JAR

Run:

```bash
python3 tools/build_fixlib.py /path/to/ukulib-fabric-2.1.1+26.2.jar /path/to/fixlib-icon.png
```

The second argument is optional if `assets/fixlib/icon.png` exists in the repository.

The resulting file is written to:

```text
dist/fixlib-fabric-2.1.1+26.2.jar
```

## License and attribution

FixLib 2.1.1 is based on [ukuLib](https://github.com/uku3lig/ukulib) by uku and remains under **MPL-2.0**. See `LICENSE`, `NOTICE`, and `SOURCE.md`.
