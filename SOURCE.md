# Source and attribution

FixLib 2.2.0+26.3 is a compatibility fork/rebrand of **ukulib 2.2.0+26.3** by **uku**.

Upstream source: https://github.com/uku3lig/ukulib/tree/2.2.0%2B26.3  
Upstream project: https://github.com/uku3lig/ukulib  
Upstream release commit: `4831e85a5f9af891ce287e97ef01f00d61b1a3ae`  
License: Mozilla Public License 2.0 (MPL-2.0)

This repository contains the source form of the FixLib-specific modifications and a reproducible repack script. FixLib preserves the upstream `net.uku3lig.ukulib` Java package/API and Fabric entrypoint classes.

The compatibility JAR is produced from the upstream Fabric build and changes only documented branding/compatibility details:

- Fabric mod id/name/contact metadata becomes `fixlib` / **FixLib**.
- `provides: ["ukulib"]` is added so compatible downstream mods can resolve the legacy dependency name.
- FixLib icon/title-screen avatar resources replace the upstream branding resources.
- `ukulib.config.title` translation values are branded as **FixLib Config**.
- In `UkulibConfig.class`, only two exact constant-pool string values are changed: the config namespace `ukulib` -> `fixlib`, and the default head username `uku3lig` -> `fixlib_`. Package/class names are not relocated or rewritten.

No original ukulib JAR should be installed alongside FixLib in the same Minecraft profile because FixLib intentionally provides the `ukulib` compatibility identity.
