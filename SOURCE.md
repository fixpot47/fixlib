# Source and attribution

FixLib 2.1.1+26.2 is a compatibility fork/rebrand of **ukulib 2.1.1+26.2** by **uku**.

Upstream source: https://github.com/uku3lig/ukulib/tree/2.1.1%2B26.2
Upstream project: https://github.com/uku3lig/ukulib
License: Mozilla Public License 2.0 (MPL-2.0)

This repository contains the FixLib-specific source-form modifications (metadata and reproducible repack script). The Java bytecode in the compatibility JAR is the unmodified upstream ukulib 2.1.1+26.2 bytecode; FixLib changes the mod metadata and branding while preserving the legacy Java package/API and `ukulib` entrypoint key for compatibility.

The Fabric mod id is `fixlib`. It declares `provides: ["ukulib"]` so mods that depend on ukulib 2.1.x can resolve the compatibility provider without installing the original ukulib JAR at the same time.
