# OpenWrt support for COMFAST CF-WR630AX

Hardware-verified OpenWrt support, validation records and provenance for the
**COMFAST CF-WR630AX AX3000**.

This repository preserves the earlier CF-WR630AX work from
[OpenWrt PR #20654](https://github.com/openwrt/openwrt/pull/20654), plus the
later hardware verification, corrections and current OpenWrt port.

> [!WARNING]
> Support has been verified on one physical CF-WR630AX test unit. The NAND
> partition named **Factory** contains device-specific Wi-Fi calibration and
> MAC data. Never erase or overwrite it.

## Upstream candidate

The current upstream candidate is maintained in
[My OpenWrt fork](https://github.com/stelin66/openwrt):

- branch: `mediatek-filogic-cf-wr630ax-final`
- candidate commit: `59d74b047a6efc21330612b7d3cd371e57a49898`
- target: `mediatek/filogic`
- one logical device-support commit
- exactly five OpenWrt source files changed
- DCO/sign-off chain preserves original author credit
- normal image: `squashfs-sysupgrade.bin`
- recovery image: `initramfs-kernel.bin`
- legacy stock board ID `cf-wr630ax` is retained in
  `SUPPORTED_DEVICES` for migration compatibility

The final candidate was rebuilt and validated successfully in GitHub Actions
run `37147860083`. The generated images have SHA256:

- sysupgrade: `4e90d99d91f5d8f19b8dbc5877cf0d49d61f0cfad727aa7729058bccc0f6ba01`
- initramfs: `9878e15ba8f7ac97490aacce63bb22f0f4e62cb7fdc723fc174fe55d536de7e1`

## Hardware at a glance

| Item | CF-WR630AX |
|---|---|
| SoC | MediaTek MT7981B |
| CPU | 2 × ARM Cortex-A53 @ 1.3 GHz |
| RAM | 256 MiB DDR3 |
| Flash | 128 MiB Winbond SPI-NAND |
| LAN | 3 × 1 GbE via MediaTek MT7531 |
| WAN | 1 × 1 GbE via MT7981 internal PHY |
| Switch CPU link | fixed 2.5 Gbit/s |
| Wi-Fi | 2.4/5 GHz Wi-Fi 6, 2x2 |
| UART | 3.3 V TTL, 115200 8N1 |
| Power | 12 VDC, 1 A |
| Bootloader | U-Boot 2023.10-rc4 |
| NAND layer | NMBM |

Hardware verification covers LAN1–LAN3, WAN, both Wi-Fi bands, all four LEDs,
Reset/WPS-Mesh GPIOs, NVMEM MAC assignment, NAND/NMBM/UBI, sysupgrade and
preservation of BL2, u-boot-env, Factory and FIP.

The permanently installed verification build reports:

```text
OpenWrt SNAPSHOT r0+36743-c759267c92
Linux 6.18.52
Target: mediatek/filogic
Board: comfast,cf-wr630ax
rootfs_type: squashfs
```

## Boot log and verification evidence

The detailed records are intentionally kept in the Wiki instead of making this
README a long test transcript:

- **[Full sanitized boot log](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Current-main-verification#full-sanitized-boot-log)**
- **[OEM BL2/U-Boot/NMBM boot log](https://openwrt.org/inbox/toh/comfast/cf-wr630ax_v1#bootlogs)** — power-on bootloader/NMBM evidence on the OpenWrt device Wiki
- **[Current-main hardware verification](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Current-main-verification)** — boot, NAND/NMBM/UBI, Ethernet, Wi-Fi, GPIO, MAC and permanent-install evidence
- **[Hardware](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Hardware)** — board layout, UART, NAND partitions and Factory/NVMEM offsets
- **[Verification and safety](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Verification-and-safety)** — backups, hashes, protected partitions and recovery boundary
- **[Hardware modifications](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Hardware-modifications)** — corrections derived from real-hardware testing
- **[Provenance](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Provenance)** — original PR, authorship and archived source history

The auditable Markdown source for the Wiki lives in
[`wiki-source/`](wiki-source/).

## Installation

For a router still running COMFAST stock firmware, connect a computer to a LAN
port and open `http://192.168.0.1/`. The intended normal install path is the
stock COMFAST firmware-update WebUI using:

```text
openwrt-mediatek-filogic-comfast_cf-wr630ax-squashfs-sysupgrade.bin
```

The COMFAST stock firmware itself uses the OpenWrt sysupgrade archive format
with legacy board ID `cf-wr630ax`.

Opening the enclosure is **not** required for normal installation. UART/TFTP
with the initramfs image is retained as the recovery/unbrick path.

The verified recovery interface is 3.3 V TTL at 115200 8N1. Connect
**GND/TX/RX only** and leave VCC disconnected. See
**[Hardware](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Hardware)**
for the photographed header, pinout and recovery procedure.

Reverting from OpenWrt to COMFAST stock firmware has not been hardware-verified,
so this project does not publish an unverified stock-flash procedure.

## Flash safety

Verified NAND layout:

```text
0x000000  0x100000  BL2
0x100000  0x080000  u-boot-env
0x180000  0x200000  Factory
0x380000  0x200000  FIP
0x580000  0x4000000 ubi
```

> [!CAUTION]
> The NAND partition named **Factory** contains Wi-Fi calibration and
> device-specific MAC data. Do not erase or write it.

BL2, u-boot-env, Factory and FIP remained byte-identical after the verified
sysupgrade. The detailed hashes and checks are in
**[Verification and safety](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Verification-and-safety)**.

## MAC layout

The current DTS reads MAC data directly from Factory NVMEM cells:

| Interface | Source |
|---|---|
| LAN | Factory + `0xe000` |
| WAN | Factory + `0xe000`, +1 |
| 2.4 GHz | Factory + `0x0004` |
| 5 GHz | Factory + `0x8000` |

Exact unit-specific MAC addresses are intentionally omitted from public
documentation.

## Provenance and credit

The public Git history records:

- **earlier PR submitter:** `ddf29`
- **original CF-WR630AX device-support commit author:**
  `dingjie <DW22965391@outlook.com>`
- **original WR630AX commit:**
  `17c723ea611972b57d648dbe6e44fe46188e7d30`

The final upstream candidate preserves dingjie's original authorship/sign-off
and explicitly credits ddf29 for submitting #20654. Later completion,
hardware verification and current-main adaptation are recorded separately.

The public record does not establish whether `ddf29` and `dingjie` are the
same person, and this repository does not speculate.

See **[Provenance](https://github.com/stelin66/openwrt-cf-wr630ax-archive/wiki/Provenance)**
for the full record.

## Archive scope

Historical builds, the original PR patch and earlier image experiments remain
preserved for auditability. They are historical records and should not be
confused with the final upstream image definition, which emits the sysupgrade
image plus the initramfs recovery image.

This is an independent hardware-verification and upstreaming project, not an
official OpenWrt release.
