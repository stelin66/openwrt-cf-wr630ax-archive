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

On the tested unit:

```text
0x0004 → 40:a5:ef:45:cb:41
0x8000 → 40:a5:ef:45:cb:42
```

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

The NVMEM implementation was tested in initramfs build #4. After booting the image from RAM, Linux reported:

```text
phy0 40:a5:ef:45:cb:41
phy1 40:a5:ef:45:cb:42
```

This is an exact match with the two Factory values above.

The original support used a runtime hotplug rule for `phy1` that read `Factory + 0x8000` and then added one to the address. On this device that produced `40:a5:ef:45:cb:43`, which is not the value stored in Factory. The per-band NVMEM definition removes that workaround and restores the stored `...:42` address.

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
