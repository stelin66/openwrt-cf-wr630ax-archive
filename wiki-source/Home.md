# COMFAST CF-WR630AX — OpenWrt hardware verification

![Initramfs build](https://github.com/stelin66/openwrt-cf-wr630ax-archive/actions/workflows/build-cf-wr630ax-initramfs.yml/badge.svg)

> [!WARNING]
> **Experimental device support.**
>
> Permanent OpenWrt installation has now been verified on one physical CF-WR630AX test unit, including normal cold boot from NAND/UBI. The NAND **Factory** partition contains device-specific calibration data and MAC addresses and must never be erased or overwritten. Keep verified backups and a UART/TFTP recovery path before flashing another unit.

This wiki documents an independent hardware-verification effort for the **COMFAST CF-WR630AX AX3000**, based on the archived OpenWrt support from [PR #20654](https://github.com/openwrt/openwrt/pull/20654).

The goal is to preserve the original work, verify it against real hardware, fix only what measurements show is wrong, and keep the original author attribution separate from later hardware corrections.

## Hardware at a glance

| Item | CF-WR630AX |
|---|---|
| SoC | MediaTek MT7981B, dual-core Cortex-A53 @ 1.3 GHz |
| RAM | 256 MiB DDR3 |
| Flash | 128 MiB Winbond SPI-NAND |
| LAN | 3 × Gigabit via MediaTek MT7531 |
| WAN | 1 × Gigabit via MT7981 internal PHY |
| Wi-Fi | 2.4 GHz + 5 GHz, Wi-Fi 6 |
| UART | 3.3 V, 115200 8N1 |
| Bootloader | U-Boot 2023.10-rc4 |
| NAND layer | NMBM |

## Current verification status

| Area | Status | Notes |
|---|:---:|---|
| U-Boot console | ✅ | UART console, TFTP and `bootm` verified |
| Initramfs RAM boot | ✅ | FIT image boots without writing NAND |
| NAND / NMBM / UBI attach | ✅ | Detected and attached correctly |
| LAN | ✅ | DSA/MT7531 and LAN links verified |
| WAN | ✅ | MT7981 PHY verified at 1 Gbit/s full duplex |
| 2.4 GHz Wi-Fi | ✅ | AP operation verified |
| 5 GHz Wi-Fi | ✅ | AP operation verified |
| LEDs | ✅ | Physical GPIO mapping verified |
| WPS/Mesh button | ✅ | GPIO level and pressed/released hotplug events verified |
| Wi-Fi MAC layout | ✅ | Factory offsets verified directly on hardware |
| NVMEM Wi-Fi MAC fix | ✅ | Verified from RAM and after permanent NAND install |
| Full sysupgrade image | ✅ | Tar/control validation and hardware install verified |
| Protected MTD partitions | ✅ | BL2, env, Factory and FIP byte-identical after sysupgrade |
| Cold boot from NAND | ✅ | Normal U-Boot autoboot and OpenWrt startup verified |
| LuCI image | ✅ | Pinned LuCI full build boots and web UI is operational |
| Current OpenWrt main initramfs | ✅ | Kernel 6.18.52 boots on hardware; LAN/WAN, both radios, LEDs, WPS and NVMEM verified in RAM |

## Verified images

### Initramfs build #4

```text
openwrt-mediatek-filogic-comfast_cf-wr630ax-initramfs-kernel.bin
8746048 bytes (0x857440)
SHA256 9ceca37d2188f1e785d952a2cbb47d8e1b8d993469488b6c8fcd8bab4a18708b
```

### Hardware-fixed full build

```text
factory.bin
10354688 bytes
SHA256 ac8606bf5f548bb26ab3b62112bc73c8c1e8bade2506cdb4d63c94794bd4c6f5

sysupgrade.bin
9052439 bytes
SHA256 7ad1a79edf6d419594e837d900e16e00eed81d55e27dc583853759d693fc84be
```

This sysupgrade image was installed to NAND and survived normal reboot and cold boot.

### LuCI full build #1

GitHub Actions run **36767167724** completed successfully.

```text
factory.bin
10878976 bytes
SHA256 86911460d89a00b2b73c17a4c67c51284bb0c0ed78d645e58bcc38196d3448b6

sysupgrade.bin
9502999 bytes
SHA256 0ccb08a90c756ed10df3ba317233e69fafb4203d11a1e7afabb062fb093ea1aa
```

The LuCI sysupgrade image passed `sysupgrade -T`, was installed successfully, and the web interface was verified on the physical router. LuCI reports the board as **COMFAST CF-WR630AX**, target **mediatek/filogic**, kernel **6.12.55**.

## Hardware-verified fixes

The original archived support is kept intact. Hardware corrections live separately in
[`archive/cf-wr630ax-hwfix-v1.patch`](../archive/cf-wr630ax-hwfix-v1.patch).

Verified corrections include:

- GPIO 35 → 5 GHz LED
- GPIO 34 → 2.4 GHz LED
- GPIO 8 → Mesh LED
- GPIO 13 → WAN LED
- GPIO 1 → WPS/Mesh button using `KEY_WPS_BUTTON`
- WAN LED bound to `eth1` link/activity
- Wi-Fi MACs moved from a runtime hotplug workaround to per-band NVMEM cells

The Factory data measured on the test unit confirms two distinct per-band MAC cells:

| Radio | Factory offset | Runtime result |
|---|---:|---|
| `phy0` | `0x0004` | exact stored address used |
| `phy1` | `0x8000` | exact stored address used |

Exact device MAC addresses are intentionally omitted from the public wiki. The old runtime workaround incremented the address stored at `0x8000`; the NVMEM fix instead uses the stored secondary address directly and remains correct after permanent installation.

## Verified installation path

```text
archived PR
    ↓
reproducible historical build
    ↓
hardware-verified fixes
    ↓
initramfs RAM boot over TFTP
    ↓
verify GPIO / Ethernet / Wi-Fi / MAC layout
    ↓
build full images
    ↓
backup BL2 + env + Factory + FIP + OEM UBI
    ↓
review nand/sysupgrade path
    ↓
sysupgrade -T
    ↓
permanent sysupgrade to UBI
    ↓
normal reboot + cold boot
    ↓
verify protected partitions remain byte-identical
```

## Current OpenWrt main port

A first port to current OpenWrt `main` has now built successfully and booted on the physical router entirely from initramfs/RAM. Kernel 6.18.52, NMBM/UBI attach, LAN1–3, WAN, both Wi-Fi radios, per-band NVMEM MAC assignment, all four front-panel LEDs and the WPS/Mesh button were hardware-verified.

See [[Current-main-verification]] for the sanitized boot and hardware-test logs.

Permanent flashing of the current-main port has **not** yet been tested.

## Snapshot package warning

This project intentionally reproduces an older OpenWrt snapshot using pinned source/feed commits. The generated `/etc/apk/repositories.d/distfeeds.list` points at rolling `downloads.openwrt.org/snapshots/` repositories, which later moved to newer package ABIs.

Do **not** force-install current rolling snapshot packages into this historical image. Matching extra packages or kernel modules should be built from the same pinned source/feed set, or the device should be ported to current OpenWrt main.

## Important: CF-WR630AX is not CF-WR632AX firmware

The current upstream **CF-WR632AX** support uses the same useful Wi-Fi Factory offsets (`0x4` and `0x8000`), which is useful corroboration for the NVMEM layout.

However, the devices are materially different. WR632AX has 512 MiB RAM, a different Ethernet layout, USB and a fan. **Do not flash WR632AX images on a WR630AX.**

See [[Hardware]] for the detailed layout.

## Attribution

The original device-support code is credited exactly as recorded in Git history:

- **PR submitter:** `ddf29`
- **Device-support commit author:** `dingjie <DW22965391@outlook.com>`
- **Original WR630AX commit:** `17c723ea611972b57d648dbe6e44fe46188e7d30`

The public history does not establish whether `ddf29` and `dingjie` are the same person, so this archive does not speculate.

See [[Provenance]] for the full archival record.

---

**Next:** [[Hardware]] · [[Hardware-modifications]] · [[Verification-and-safety]] · [[Current-main-verification]] · [[Provenance]]
