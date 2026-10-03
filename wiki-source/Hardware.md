# Hardware

This page records the hardware layout that has been observed or verified on the COMFAST CF-WR630AX test unit.

## Core platform

| Component | Detail |
|---|---|
| SoC | MediaTek MT7981B |
| CPU | 2 × ARM Cortex-A53 @ 1.3 GHz |
| RAM | 256 MiB DDR3 |
| SPI-NAND | 128 MiB Winbond |
| Ethernet switch | MediaTek MT7531 |
| WAN PHY | MT7981 internal Gigabit PHY |
| Wi-Fi | Integrated MediaTek 2.4/5 GHz platform |
| UART | 3.3 V TTL, 115200 8N1 |

## NAND layout

The stock U-Boot environment reports:

```text
mtdparts=nmbm0:1024k(bl2),512k(u-boot-env),2048k(factory),2048k(fip),65536k(ubi)
```

Corresponding layout:

| Offset | Size | Partition | Policy |
|---:|---:|---|---|
| `0x000000` | `0x100000` | BL2 | read-only during testing |
| `0x100000` | `0x080000` | u-boot-env | read-only during testing |
| `0x180000` | `0x200000` | Factory | **never erase/write** |
| `0x380000` | `0x200000` | FIP | read-only during testing |
| `0x580000` | 64 MiB | ubi | stock system area |

> [!CAUTION]
> The NAND partition named **Factory** is calibration/MAC storage. It is unrelated to an OpenWrt file named `factory.bin`.

After permanent OpenWrt sysupgrade, `/proc/mtd` retained this exact fixed-partition layout. Direct SHA256 reads also confirmed that BL2, u-boot-env, Factory and FIP were unchanged.

The resulting OpenWrt UBI layout on the verified unit is:

| Volume | Type | Size |
|---|---|---:|
| kernel | dynamic | 36 LEB / 4,571,136 bytes |
| rootfs | dynamic | 36 LEB / 4,571,136 bytes |
| rootfs_data | dynamic | 415 LEB / 52,695,040 bytes |

The UBI device reported 512 total LEBs, 0 bad PEBs and 19 PEBs reserved for bad-block handling.

## Enclosure access and UART

The verified first-installation path requires access to the stock U-Boot serial console, so the enclosure must be opened.

The underside of the enclosure has four recessed screws. After removing the bottom cover, the UART header is visible on the PCB next to the heatsink.

The PCB silkscreen labels the four UART pads:

```text
VCC  GND  RX  TX
```

> [!CAUTION]
> The UART uses **3.3 V TTL signalling**, but the USB-UART adapter must **not** power the router.
> Connect **GND, RX and TX only**. Leave **VCC completely disconnected**.

USB-UART wiring:

```text
Router TX  -> USB-UART RX
Router RX  -> USB-UART TX
Router GND <-> USB-UART GND
VCC        -> DO NOT CONNECT
```

Serial settings:

```text
115200 baud
8 data bits
no parity
1 stop bit
```

The router is powered from its normal DC power supply while the USB-UART adapter provides only the serial connection.

The tested installation path uses this UART connection to interrupt U-Boot autoboot, load the OpenWrt initramfs image over TFTP, and boot OpenWrt entirely from RAM before any NAND write is performed.

Direct installation from the stock COMFAST web interface has **not** been verified.

## U-Boot

Observed bootloader:

```text
BL2 v2.9
U-Boot 2023.10-rc4
UART: 115200 8N1
```

Useful environment values:

```text
ipaddr=192.168.1.1
serverip=192.168.1.10
loadaddr=0x46000000
```

Verified commands include `tftpboot`, `iminfo`, `bootm` and `mtd`.

The current test method loads the OpenWrt initramfs FIT image into DRAM and boots it with:

```text
bootm 0x46000000
```

This leaves NAND untouched.

## Ethernet

Verified topology:

- `eth0` → LAN side / MT7531 CPU link
- `eth1` → WAN / MT7981 internal PHY
- `lan1`, `lan2`, `lan3` → MT7531 DSA ports

The internal switch CPU link operates as a fixed 2.5G link; the external LAN ports are Gigabit.

## GPIO mapping

The following mappings were verified on hardware:

| GPIO | Function | Active level |
|---:|---|---|
| 0 | Reset button | low |
| 1 | WPS/Mesh button | low |
| 8 | Mesh LED | low |
| 13 | WAN LED | low |
| 34 | 2.4 GHz LED | low |
| 35 | 5 GHz LED | low |

The WPS/Mesh input was verified electrically in `/sys/kernel/debug/gpio` and through OpenWrt button hotplug events:

```text
ACTION=pressed  BUTTON=wps
ACTION=released BUTTON=wps
```

## Wi-Fi MAC layout

Direct reads from the Factory partition showed:

```text
Factory + 0x0004 = primary Wi-Fi MAC
Factory + 0x8000 = secondary Wi-Fi MAC
```

On the tested unit, both offsets contained distinct valid MAC addresses. Exact device MAC addresses are intentionally omitted from the public wiki.

The hardware-fix patch models these as NVMEM `mac-base` cells and assigns them per band:

```dts
band@0 {
    reg = <0>;
    nvmem-cells = <&macaddr_factory_4 0>;
    nvmem-cell-names = "mac-address";
};

band@1 {
    reg = <1>;
    nvmem-cells = <&macaddr_factory_8000 0>;
    nvmem-cell-names = "mac-address";
};
```

### Runtime verification

The NVMEM implementation was first tested in initramfs build #4, re-verified after permanent NAND installation, and verified again on the current-main RAM port. Linux assigned each radio the exact MAC stored in its respective Factory cell.

The original support used a runtime hotplug rule for `phy1` that read `Factory + 0x8000` and then incremented that address. Hardware verification showed that this produced an address different from the value actually stored in Factory. The per-band NVMEM definition removes that workaround and uses the stored secondary address directly.

## WR632AX relationship

OpenWrt's later CF-WR632AX support uses the same two Wi-Fi MAC offsets, `0x4` and `0x8000`. That is useful evidence for a shared COMFAST/MediaTek Factory-data convention.

It is **not** evidence that the firmware images are interchangeable.

Notable WR632AX differences include:

- 512 MiB RAM
- different Ethernet topology
- 2.5G WAN
- USB
- cooling fan
- different enclosure/front-panel hardware

Treat WR630AX and WR632AX as separate devices unless a specific component/layout has been independently verified.
