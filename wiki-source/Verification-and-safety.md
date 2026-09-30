# Verification and safety

The working rule for this project is: **verify in RAM first, write flash last**.

That gate has now been completed successfully on one physical CF-WR630AX.

## What has been verified

### Boot path

- UART console works bidirectionally.
- U-Boot TFTP works.
- OpenWrt FIT metadata and hashes validate in U-Boot.
- Initramfs boots entirely from DRAM.
- Linux identifies the board as COMFAST CF-WR630AX.
- Permanent OpenWrt installation boots from NAND/UBI.
- A later cold boot with the enclosure assembled and UART disconnected also completed normally.

### Storage

The fixed partition layout remains:

```text
mtd0 00100000 "BL2"
mtd1 00080000 "u-boot-env"
mtd2 00200000 "Factory"
mtd3 00200000 "FIP"
mtd4 04000000 "ubi"
```

After sysupgrade, UBI contains three healthy dynamic volumes:

```text
kernel      36 LEBs   4571136 bytes
rootfs      36 LEBs   4571136 bytes
rootfs_data 415 LEBs 52695040 bytes
```

The post-install UBI state reported zero bad physical eraseblocks.

### Protected partitions

Independent pre-install backups were copied off-device and checksummed. After permanent sysupgrade, direct SHA256 reads from the four protected MTD partitions still matched those backups exactly:

```text
BL2
bfe6ef304f6a9b5e4f01f3e4ece18926ee9b1cb3f4a7f15c55fd24329176289f

u-boot-env
9d280971245e94e8508a56522b75076c3a6150468c7f290783c521df64de3057

Factory
bc1deae99f3509ec4f93eb45b65d970cef18f569efd22772ca58bfda26d4c545

FIP
852bbc73d48c9ce246846f45e61aba267a6aab88640ccd5dd6fc8ff9deaba7af
```

This verifies that the tested sysupgrade path changed the UBI system area without modifying BL2, u-boot-env, Factory or FIP.

### Network

- MT7531 switch initializes.
- LAN links work.
- WAN `eth1` works at 1 Gbit/s full duplex.
- LAN traffic to OpenWrt has been tested over SSH/ping.
- WAN was re-verified after permanent installation with `carrier=1`, `speed=1000`, `duplex=full`.

### Wi-Fi

- 2.4 GHz radio works.
- 5 GHz radio works.
- The board EEPROM/calibration area is readable from Factory.
- The primary and secondary Wi-Fi MAC locations have been verified directly.
- Per-band NVMEM MAC assignment is verified in initramfs and after permanent NAND installation.

Runtime result:

```text
phy0 40:a5:ef:45:cb:41
phy1 40:a5:ef:45:cb:42
```

### LEDs and buttons

Installed-image sysfs names:

```text
blue:mesh
blue:wan
blue:wlan-2ghz
blue:wlan-5ghz
mt76-phy0
mt76-phy1
```

GPIO state confirms:

```text
gpio-512 reset  input high IRQ ACTIVE LOW
gpio-513 wps    input high IRQ ACTIVE LOW
```

Physical LED mapping, WAN activity LED and WPS/Mesh button hotplug events have all been verified.

## Verified initramfs build #4

```text
openwrt-mediatek-filogic-comfast_cf-wr630ax-initramfs-kernel.bin
8746048 bytes (0x857440)
SHA256 9ceca37d2188f1e785d952a2cbb47d8e1b8d993469488b6c8fcd8bab4a18708b
```

U-Boot `iminfo` verified all FIT hashes before boot.

## Verified permanent full build

```text
factory.bin
10354688 bytes
SHA256 ac8606bf5f548bb26ab3b62112bc73c8c1e8bade2506cdb4d63c94794bd4c6f5

sysupgrade.bin
9052439 bytes
SHA256 7ad1a79edf6d419594e837d900e16e00eed81d55e27dc583853759d693fc84be
```

The sysupgrade tar contained `CONTROL`, `kernel` and `root`; `sysupgrade -T` returned 0 before installation.

## Verified LuCI build #1

GitHub Actions run **36767167724** completed successfully with the same pinned OpenWrt base, feeds and hardware-fix patch, plus `CONFIG_PACKAGE_luci=y`.

```text
factory.bin
10878976 bytes
SHA256 86911460d89a00b2b73c17a4c67c51284bb0c0ed78d645e58bcc38196d3448b6

sysupgrade.bin
9502999 bytes
SHA256 0ccb08a90c756ed10df3ba317233e69fafb4203d11a1e7afabb062fb093ea1aa
```

The sysupgrade image passed `sysupgrade -T`, was installed successfully, and LuCI was verified operational on the physical router.

## Completed installation gate

- [x] UART recovery path verified
- [x] U-Boot TFTP boot verified
- [x] Historical support builds reproducibly
- [x] Ethernet verified
- [x] Both Wi-Fi radios verified
- [x] LED mapping verified
- [x] WPS/Mesh button verified
- [x] Factory Wi-Fi MAC offsets verified
- [x] NVMEM MAC fix verified in fresh initramfs
- [x] Full factory/sysupgrade images built with all fixes
- [x] BL2 backup copied off-device and checksummed
- [x] u-boot-env backup copied off-device and checksummed
- [x] Factory backup copied off-device and checksummed twice
- [x] FIP backup copied off-device and checksummed
- [x] OEM UBI backup copied off-device and checksummed
- [x] Exact platform/nand install behavior reviewed
- [x] `sysupgrade -T` passed
- [x] Permanent NAND installation completed
- [x] Protected MTD partitions verified byte-identical afterward
- [x] Normal reboot verified
- [x] Cold boot without UART verified
- [x] LuCI image verified

## Package ABI warning

The installed firmware is a historical reproducible snapshot. Its distfeeds point to rolling OpenWrt snapshot repositories, but those repositories later moved to newer `libubox`, `libubus` and related ABIs.

An attempted `apk add luci` correctly stopped with dependency conflicts before changing the system.

Do not use `apk --force` or a general rolling-snapshot upgrade on this build. Extra userspace packages and especially `kmod-*` packages should be built against the exact same pinned source/feed set, or the WR630AX support should be ported to current OpenWrt main.

## Recovery assets

The stock bootloader provides:

- interactive UART console
- TFTP image loading
- direct FIT `bootm`
- U-Boot boot menu
- Web failsafe entry

The OEM backups provide an additional recovery reference, including two identical independent reads of the unique Factory partition.

## Factory partition vs OpenWrt factory image

These names are easy to confuse:

- **NAND `Factory` partition** → calibration/MAC data; preserve it.
- **OpenWrt `factory.bin`** → an installation image format.

They are completely different things.
