# FixLib

**FixLib** is a client-side utility library for Fabric mods by **fixpot47**.

Current version: **2.2.0+26.3**  
Minecraft: **26.3**  
Loader: **Fabric**

## Compatibility

FixLib 2.2.0 is a compatibility fork/rebrand of **ukulib 2.2.0+26.3**. It intentionally preserves the legacy `net.uku3lig.ukulib` Java package/API and upstream entrypoint classes so existing compatible mods can continue using the same API.

The Fabric mod id is `fixlib`, and FixLib declares `provides: ["ukulib"]` for dependency compatibility. The established FixLib config namespace is also preserved as `fixlib`.

Minecraft 26.2 users should keep using the previous FixLib 2.1.1+26.2 release.

## FixLib-specific changes

- Mod name/id changed to **FixLib / `fixlib`**
- Author metadata changed to **fixpot47**
- `ukulib` is exposed as a compatibility alias through `provides`
- Legacy `net.uku3lig.ukulib` packages/classes remain intact
- Config namespace remains `fixlib`
- Built-in config title is branded as **FixLib Config**
- FixLib icon and title-screen avatar are preserved
- Source/issues links point to this repository

## Build / reproduce the JAR

Obtain the Fabric JAR for upstream **ukulib 2.2.0+26.3** and the previous FixLib 2.1.1+26.2 JAR, then run:

```bash
python3 tools/build_fixlib.py /path/to/ukulib-fabric-2.2.0+26.3.jar /path/to/fixlib-2.1.1+26.2.jar
```

The resulting file is written to:

```text
dist/fixlib-fabric-2.2.0+26.3.jar
```

The second JAR is used only as the branding reference so the existing FixLib icon and small title-screen avatar are preserved exactly. The build script applies only the documented FixLib branding/metadata/config-namespace changes and leaves the upstream API/package layout intact.

## License and attribution

FixLib 2.2.0+26.3 is based on [ukulib](https://github.com/uku3lig/ukulib) by **uku** and remains under **MPL-2.0**. See `LICENSE`, `NOTICE`, and `SOURCE.md`.
