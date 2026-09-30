# COMFAST CF-WR630AX — OpenWrt hardware verification

![Initramfs build](https://github.com/stelin66/openwrt-cf-wr630ax-archive/actions/workflows/build-cf-wr630ax-initramfs.yml/badge.svg)

> [!WARNING]
> **Experimental support. Do not permanently flash this device yet.**
>
> The current work is being validated from RAM using U-Boot/TFTP. The NAND **Factory** partition contains calibration data and MAC addresses and must not be erased or overwritten.

This wiki documents an independent hardware-verification effort for the **COMFAST CF-WR630AX AX3000**, based on the archived OpenWrt support from [PR #20654](https://github.com/openwrt/openwrt/pull/20654).

The goal is simple: preserve the original work, verify it against real hardware, fix only what measurements show is wrong, and keep a safe recovery path before any permanent installation is attempted.

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
| WAN | ✅ | MT7981 PHY link verified at 1 Gbit/s |
| 2.4 GHz Wi-Fi | ✅ | AP operation verified |
| 5 GHz Wi-Fi | ✅ | AP operation verified |
| LEDs | ✅ | Physical GPIO mapping verified |
| WPS/Mesh button | ✅ | GPIO level and pressed/released hotplug events verified |
| Wi-Fi MAC layout | ✅ | Factory offsets verified directly on hardware |
| NVMEM Wi-Fi MAC fix | ✅ | Verified in initramfs build #4 on hardware |
| Permanent NAND installation | ⛔ | Intentionally not attempted yet |

## Latest verified initramfs

GitHub Actions **build #4** completed successfully and was booted from RAM on the physical router.

```text
Image:
openwrt-mediatek-filogic-comfast_cf-wr630ax-initramfs-kernel.bin

Size:
8746048 bytes (0x857440)

SHA256:
9ceca37d2188f1e785d952a2cbb47d8e1b8d993469488b6c8fcd8bab4a18708b
```

U-Boot `iminfo` verified the kernel, initrd and FDT hashes before boot.

The key result from the NVMEM test was:

```text
phy0 40:a5:ef:45:cb:41
phy1 40:a5:ef:45:cb:42
```

Those values match the addresses stored in Factory at offsets `0x4` and `0x8000`.

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

The Factory data measured on the test unit is:

| Radio | Factory offset | Stored/tested address |
|---|---:|---|
| `phy0` | `0x0004` | `40:a5:ef:45:cb:41` |
| `phy1` | `0x8000` | `40:a5:ef:45:cb:42` |

The old runtime workaround incremented the MAC at `0x8000`, producing `...:43`. The NVMEM fix now uses the stored secondary address directly, and this has been verified on hardware.

## Safe test path

The project currently follows this sequence:

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
only then consider permanent installation
```

No NAND write is required for the current validation work.

## Important: CF-WR630AX is not CF-WR632AX firmware

The current upstream **CF-WR632AX** support uses the same useful Wi-Fi Factory offsets (`0x4` and `0x8000`), which strongly suggests shared COMFAST/MediaTek design conventions.

However, the devices are materially different. Upstream WR632AX hardware has 512 MiB RAM, a different Ethernet layout, USB and a fan. **Do not flash WR632AX images on a WR630AX.**

See [[Hardware]] for the detailed layout.

## Attribution

The original device-support code is credited exactly as recorded in Git history:

- **PR submitter:** `ddf29`
- **Device-support commit author:** `dingjie <DW22965391@outlook.com>`
- **Original WR630AX commit:** `17c723ea611972b57d648dbe6e44fe46188e7d30`

The public history does not establish whether `ddf29` and `dingjie` are the same person, so this archive does not speculate.

See [[Provenance]] for the full archival record.

---

**Next:** [[Hardware]] · [[Hardware-modifications]] · [[Verification-and-safety]] · [[Provenance]]
