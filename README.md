# OpenWrt support for COMFAST CF-WR630AX

Hardware-verified OpenWrt support, reproducible build records and provenance archive for the **COMFAST CF-WR630AX AX3000**.

This repository began as an independent archive of the device support from [OpenWrt PR #20654](https://github.com/openwrt/openwrt/pull/20654). The archived code has since been tested on real hardware, corrected where measurements showed errors, installed permanently to NAND, and ported to current OpenWrt main.

> [!WARNING]
> **Experimental device support.**
>
> Permanent OpenWrt installation has been verified on one physical CF-WR630AX test unit. The NAND partition named **Factory** contains device-specific calibration data and MAC addresses and must never be erased or overwritten. Keep verified backups and a working UART/TFTP recovery path before flashing another unit.

## Current status

| Area | Status | Notes |
|---|:---:|---|
| Current OpenWrt main port | ✅ | Built from OpenWrt commit <code>c759267c92b0697a6fd6f369164a5ed4c1a6a03c</code> |
| Initramfs / RAM boot | ✅ | U-Boot TFTP + FIT validation + bootm |
| Permanent NAND install | ✅ | sysupgrade validation passed; normal NAND boot verified |
| Kernel / target | ✅ | Linux 6.18.52, mediatek/filogic |
| LAN | ✅ | LAN1–LAN3 physically mapped and verified |
| WAN | ✅ | eth1, 1 Gbit/s full duplex |
| 2.4 GHz Wi-Fi | ✅ | Real client association verified |
| 5 GHz Wi-Fi | ✅ | Real Wi-Fi 6 client association verified |
| LEDs | ✅ | Mesh, WAN, 2.4 GHz and 5 GHz mappings verified |
| WPS/Mesh button | ✅ | GPIO 1, active-low, verified on hardware |
| Wi-Fi NVMEM MAC layout | ✅ | Per-band Factory offsets verified |
| Protected MTD partitions | ✅ | BL2, env, Factory and FIP unchanged after sysupgrade |
| LuCI | ✅ | Installed and operational on the verified current-main build |

The currently installed test build reports:

~~~text
OpenWrt SNAPSHOT r0+36743-c759267c92
Linux 6.18.52
Target: mediatek/filogic
Board: comfast,cf-wr630ax
rootfs_type: squashfs
~~~

## Documentation

The detailed evidence and test records live in the project Wiki:

- **[Wiki home](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki)** — project overview and verified image history
- **[Hardware](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Hardware)** — SoC, NAND, Ethernet, GPIO and Factory/NVMEM layout
- **[Hardware modifications](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Hardware-modifications)** — corrections derived from real-hardware testing
- **[Verification and safety](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Verification-and-safety)** — flash safety, backups, installation gate and recovery
- **[Current OpenWrt main verification](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Current-main-verification)** — sanitized current-main boot log, RAM tests and permanent NAND verification
- **[Provenance](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Provenance)** — original PR history and attribution

The Markdown source for the Wiki is also kept under [wiki-source/](wiki-source/) so changes remain auditable in the normal repository history.

## Hardware at a glance

| Item | CF-WR630AX |
|---|---|
| SoC | MediaTek MT7981B |
| CPU | 2 × ARM Cortex-A53 @ 1.3 GHz |
| RAM | 256 MiB DDR3 |
| Flash | 128 MiB Winbond SPI-NAND |
| LAN | 3 × Gigabit via MediaTek MT7531 |
| WAN | 1 × Gigabit via MT7981 internal PHY |
| Switch CPU link | fixed 2.5 Gbit/s |
| Wi-Fi | 2.4 GHz + 5 GHz, Wi-Fi 6 |
| UART | 3.3 V TTL, 115200 8N1 |
| Bootloader | U-Boot 2023.10-rc4 |
| NAND layer | NMBM |

## Current OpenWrt main port

Development for the modern OpenWrt tree is kept on the **[current-main-port branch](https://github.com/stelin66/openwrt-cf-wr630ax-archive/tree/current-main-port)**.

Important files:

- [current-main/mt7981b-comfast-cf-wr630ax.dts](https://github.com/stelin66/openwrt-cf-wr630ax-archive/blob/current-main-port/current-main/mt7981b-comfast-cf-wr630ax.dts)
- [current-main/apply-port.py](https://github.com/stelin66/openwrt-cf-wr630ax-archive/blob/current-main-port/current-main/apply-port.py)
- [current-main initramfs workflow](https://github.com/stelin66/openwrt-cf-wr630ax-archive/blob/current-main-port/.github/workflows/build-cf-wr630ax-current-main-initramfs.yml)
- [current-main full-image workflow](https://github.com/stelin66/openwrt-cf-wr630ax-archive/blob/current-main-port/.github/workflows/build-cf-wr630ax-current-main-full.yml)

Pinned OpenWrt source:

~~~text
c759267c92b0697a6fd6f369164a5ed4c1a6a03c
~~~

Pinned feed revisions used for the verified build:

~~~text
packages   95d73ebcc95ade2ea78b0a281898cf8b6ec7b7f9
luci       32775cf32b94ecf12bca08ce62aeb2723d2d51ce
routing    4b9891b9136259f93294a424507ed24c5e8c1cbd
telephony  5d68d53c160a325ea9d03fce393e051573bcc736
video      2baec75e2c07b3bb3ae3b73580a3bd3074818707
~~~

### Verified current-main initramfs

[GitHub Actions run 36784301628](https://github.com/stelin66/openwrt-cf-wr630ax-archive/actions/runs/36784301628)

~~~text
openwrt-mediatek-filogic-comfast_cf-wr630ax-initramfs-kernel.bin
9090776 bytes (0x8ab6d8)
SHA256 1866be3b8379e2b776db055141f97a258624f0e4ec563f188ff03311356b42b0
~~~

This image was booted from RAM over TFTP before any current-main NAND write. NAND/NMBM/UBI, all physical Ethernet ports, both Wi-Fi bands, LEDs, WPS/Mesh GPIO and per-band NVMEM MAC assignment were verified on the physical router.

### Verified current-main full images

[GitHub Actions run 36863399195](https://github.com/stelin66/openwrt-cf-wr630ax-archive/actions/runs/36863399195)

~~~text
openwrt-mediatek-filogic-comfast_cf-wr630ax-squashfs-factory.bin
10747904 bytes
SHA256 b58d3593a5bb991f8555dde4986f7e7cb88ead5cbe2909d23480b635b117107a

openwrt-mediatek-filogic-comfast_cf-wr630ax-squashfs-sysupgrade.bin
9369879 bytes
SHA256 610ae53e659a4c5a82308d6a01c2851751e372a53861f12b8087e0c1641b61b7
~~~

The sysupgrade image:

1. passed workflow-side image validation,
2. matched its SHA256 again on the router,
3. passed sysupgrade -T with exit status 0,
4. was installed with sysupgrade -n,
5. rebooted normally from NAND,
6. reported rootfs_type=squashfs, and
7. left BL2, u-boot-env, Factory and FIP byte-identical to their verified backups.

See **[Current-main verification](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Current-main-verification)** for the complete sanitized record.

## Hardware-verified corrections

The original archived support is preserved unchanged. Later corrections are maintained separately in [archive/cf-wr630ax-hwfix-v1.patch](archive/cf-wr630ax-hwfix-v1.patch).

Verified mappings include:

| GPIO | Function |
|---:|---|
| 0 | Reset button |
| 1 | WPS/Mesh button |
| 8 | Mesh LED |
| 13 | WAN LED |
| 34 | 2.4 GHz LED |
| 35 | 5 GHz LED |

The project also replaces the original runtime Wi-Fi MAC workaround with per-band NVMEM cells verified against the NAND Factory data:

~~~text
Factory + 0x0004 -> 2.4 GHz radio
Factory + 0x8000 -> 5 GHz radio
~~~

Exact device MAC addresses are intentionally omitted from public documentation.

## Flash safety

The verified fixed NAND layout is:

~~~text
mtd0: 00100000 "BL2"
mtd1: 00080000 "u-boot-env"
mtd2: 00200000 "Factory"
mtd3: 00200000 "FIP"
mtd4: 04000000 "ubi"
~~~

> [!CAUTION]
> The NAND partition named **Factory** contains Wi-Fi calibration and device-specific MAC data. Do not erase or write it.
>
> An OpenWrt file named factory.bin is an installation image. It is **not** the NAND Factory partition.

The project follows a strict **RAM first, flash last** workflow:

~~~text
UART/TFTP recovery
      ↓
initramfs in RAM
      ↓
hardware verification
      ↓
backups + checksums
      ↓
sysupgrade -T
      ↓
permanent install
      ↓
re-read protected partitions
~~~

See **[Verification and safety](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Verification-and-safety)** before attempting an installation.

## Original PR archive and provenance

The repository still preserves the original work from OpenWrt PR #20654.

- Upstream repository: openwrt/openwrt
- Pull request: [#20654](https://github.com/openwrt/openwrt/pull/20654)
- PR title: mediatek: add support for Comfast CF-WR633AX CF-WR630AX CF-WR631AX
- Base commit: <code>7670addb077d7556a5603f0b26e2bad1b052ae84</code>
- PR head: <code>cd4e07f7b7ec8e26857f18606b7261c334a4a4c0</code>
- PR state at archival: closed, not merged
- Original CF-WR630AX support commit: <code>17c723ea611972b57d648dbe6e44fe46188e7d30</code>

Preserved material:

- [archive/openwrt-pr-20654.patch](archive/openwrt-pr-20654.patch) — complete original PR patch
- [archive/SOURCE_PR.md](archive/SOURCE_PR.md) — archived PR description and metadata
- snapshots of all seven source files touched by the PR

### Attribution

The public Git history records:

- **PR submitter / GitHub handler:** ddf29
- **device-support commit author:** dingjie &lt;DW22965391@outlook.com&gt;

The public record does not establish whether ddf29 and dingjie are the same person. This repository does not speculate.

Full credit for the original support remains with its recorded author. Later hardware verification, corrections and current-main porting are deliberately kept separate so the provenance stays clear.

See **[Provenance](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Provenance)** for details.

## Repository structure

~~~text
archive/           original PR material + hardware-fix patch
current-main/      current OpenWrt main port material (current-main-port branch)
wiki-source/       auditable source for the GitHub Wiki
.github/workflows/ reproducible historical and current-main builds
~~~

The repository intentionally preserves both the historical source and the later verified work instead of rewriting the original history.

## Snapshot package note

The verified images are pinned OpenWrt snapshots. Package repositories continue moving after an image is built, so later package or kernel-module ABIs may no longer match the installed snapshot.

Do not use forced package upgrades to cross an ABI mismatch. In particular, build kmod-* packages against the exact installed OpenWrt source/kernel ABI.

LuCI was successfully installed on the verified current-main image while the matching feed revision was still available.

## CF-WR630AX is not CF-WR632AX

The current upstream CF-WR632AX support is useful as a comparison for some Factory/NVMEM conventions, but the devices are materially different.

**Do not flash CF-WR632AX firmware on a CF-WR630AX.**

## Project scope

This is an independent hardware-verification and porting project, not an official OpenWrt release and not a claim that the original PR was merged upstream.

No new license is asserted by this archive. Original SPDX/license headers, commit attribution, Signed-off-by lines and upstream licensing terms remain applicable to the archived source.
